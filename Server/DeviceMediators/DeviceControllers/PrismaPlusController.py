import socket
import time
from threading import Thread
import csv
import os
import struct
from OpenOPC import OpenOPC

PRISMA_ADDR = '10.1.213.41'

# If you physically replace the device, please uintensitiese this line.
PRISMA_PHYSICAL_ADDR = '00-50-C2-C1-0A-26'

class PrismaPlusController(object):
	"""
	Pfeiffer Vacuum PrismaPlus (TM) QMG 220 mass spectrometer control class
	TODO:
	1) implement this thing
	2) import this in the PATServer file
	3) implement the settings file
	"""
	def __init__(self):
		self.PPThread = DataCollectionThread(self)
		# set up the OPC client. The PrismaPlus server is a DA server
		# so we use the Graybox OPC DA Wrapper to connect
		# The OPC client is running in DCOM mode (Windows only).
		# Refer to OpenOPC documentation for UNIX-like systems.
		self.opc = OpenOPC.client(opc_class="Graybox.OPC.DAWrapper")
		self.opc.connect("QMG220-DA")
		physicalAddr = self.opc.read('General.LanConfiguration.PhysicalAddress')
		# check if the connection was successful and to the correct device
		# (and not to, say, one of the simulated devices running on the PC)
		try:
			assert physicalAddr[0] == PRISMA_PHYSICAL_ADDR
		except AssertionError:
			raise AssertionError("Physical address of the residual gas analyser\
				is different than expected.")

	def write(self, msg):
		msg = msg + "\r"
		super(PrismaPlusController, self).write(msg)

	def start(self):
		'''Starts the data collection thread.'''
		self.PPCThread.start()

	def stop(self):
		"""
		Waits until data collection is complete before proceeding.
		Returns boolean value indicating whether data collection failed.
		"""
		self.PPCThread.join()
		self.opc.close()
		self.close()
		return self.PPCThread

	def collectData(self):
		"""Initiates data collection."""
		""" Data collection is documented in 7.3 of PrismaPlusComm.pdf """
		""" 
		Warning: I have not finished writing this function yet so it may not 
		be implemented correctly.
		"""
		self.masses = []
		self.intensities = []
		self.massRange = self.opc.read('Hardware.MassRange')[0]
		while True:
			packet = self.opc.read('General.DataPump.Data')
			dataBinary = packet[0]
			dataInt = [ord(d) for d in dataBinary]
			channelNumber = dataInt[0]
			dataType = dataInt[1]
			status = dataInt[2]
			if status > 1:
				break
			if status == 1:
				# CHANNEL START
				numberOfData = dataInt[3]
				timeStamp = struct.unpack('q',dataBinary[4:12])
				# timeStamp is in Windows FILETIME format,
				# i.e. number of 100 ns intervals since 1 January 1601.
				maxNumberOfDataTuples = struct.unpack('h',dataBinary[12:14])
			elif status == 5:
				# CHANNEL INFORMATION
				numberOfData = dataInt[3]
				firstMass = struct.unpack('h',dataBinary[4:6])
				lastMass = struct.unpack('h',dataBinary[6:8])
				dwellSpeed = dataInt[8]
				unitAndResolution = dataInt[9]
				# extract bits 2 and 3
				unit = ["Ampere", "cps", "Volt", "mbar"][(unitAndResolution & (0x3<<4)) >> 4]
				# extract bits 4 and 5
				resolution = [1/64, 1/32, 1/16, 1/8][(unitAndResolution & (0x3<<2)) >> 4]
			elif status == 0 || status == 2:
				# MEASURING DATA or CHANNEL END
				numberOfTuples = dataInt[3]
				pointer = 4
				for dataTuple in range(numberOfTuples):
					intensity = struct.unpack('f',dataBinary[pointer:(pointer+4)])[0]
					mass = dataInt[(pointer+4):(pointer+6)]
					status = dataInt[pointer+6]
					status2 = dataInt[pointer+7]
					pointer += 8
					self.masses.append(mass)
					self.intensities.append(intensity)
			else:
				break;
			
	def saveData(self, fname = "PrismaPlus_RGA_Data.csv"):
		'''Save the data collected by the gauge.'''
		csvFile = open(fname, 'wb')
		masses = self.masses
		intensities = self.intensities
		filewriter = csv.writer(csvFile, delimiter = ',')
		filewriter.writerow(["Mass (amu)", "Reading"])
		for i in range(len(masses)):
			output = [masses[i], intensities[i]]
			filewriter.writerow(output)
		csvFile.close()
		
	def plotData(self, fname = "PrismaPlus_RGA_Plot.png"):
		'''Plots the data collected by the gauge.'''
		import matplotlib.pyplot as plt
		plt.clf()
		masses = self.masses
		intensities = self.intensities
		plt.plot(masses, intensities, ls = 'None', marker = '.')
		plt.xlabel('Mass (amu)')
		plt.ylabel('Reading')
		plt.savefig(fname)		
		plt.clf()	

class DataCollectionThread(Thread):
	"""Data collection threads collect data."""
	def __init__(self, PPController):
		Thread.__init__(self)
		self.PPC = PPController
		self.failed = False

	def run(self):
		try:
			self.PPC.collectData()
		except:
			self.failed = True
			raise
			
if __name__ == '__main__':
	PPC = PrismaPlusController()
	PPC.collectData()
	PPC.saveData()
	PPC.plotData()
	PPC.close()
