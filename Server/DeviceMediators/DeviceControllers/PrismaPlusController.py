import socket
import time
from threading import Thread
import csv
import os
from OpenOPC import OpenOPC

PRISMA_ADDR = '10.1.213.41'

# If you physically replace the device, please update this line.
PRISMA_PHYSICAL_ADDR = '00-50-C2-C1-0A-26'

class PrismaPlusController(object):
	"""
	Pfeiffer Vacuum PrismaPlus (TM) QMG 220 mass spectrometer control class
	TODO:
	1) implement this thing
	2) import this in the PATServer file
	3) implement the settings file
	"""
	def __init__():
		self.prismaHost = socket.getHostByName(PRISMA_ADDR)
		self.PPThread = DataCollectionThread(self)
		# set up the OPC client. The PrismaPlus server is a DA server
		# so we use the Graybox OPC DA Wrapper to connect
		# The OPC client is running in DCOM mode (Windows only).
		# Refer to OpenOPC documentation for UNIX-like systems.
		self.opc = OpenOPC.client(opc_class="Graybox.OPC.DAWrapper")
		self.opc.connect("QMG220-DA")
		physicalAddr = opc.read('General.LanConfiguration.PhysicalAddress')
		# check if the connection was successful and to the correct device
		# (and not to, say, one of the simulated devices running on the PC)
		assert physicalAddr == PRISMA_PHYSICAL_ADDR

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
		raise NotImplementedError()
		
	# def saveData(self, fname = "PrismaPlus_RGA_Data.csv"):
		# '''Save the data collected by the gauge.'''
		# csvFile = open(fname, 'wb')
		# tDat = self.tDat
		# pDat = self.pDat
		# filewriter = csv.writer(csvFile, delimiter = ',')
		# filewriter.writerow(['Start Time:', self.tStart])
		# filewriter.writerow(["Time (s)", "Pressures (Torr)"])
		# for i in range(len(tDat)):
			# output = [tDat[i], pDat[i]]
			# filewriter.writerow(output)
		# csvFile.close()
		
	# def plotData(self, fname = "PrismaPlus_RGA_Plot.png"):
		# '''Plots the data collected by the gauge.'''
		# import matplotlib.pyplot as plt
		# plt.clf()
		# tDat = self.tDat
		# pDat = self.pDat
		# plt.plot(tDat, pDat, ls = 'None', marker = '.')
		# plt.xlabel('Time (s)')
		# plt.ylabel('Pressure (Torr)')
		# plt.savefig(fname)		
		# plt.clf()	

class DataCollectionThread(Thread):
	"""Data collection threads collect data."""
	def __init__(self, PPController):
		Thread.__init__(self)
		self.PPC = PPController
		self.failed = False

	def run(self):
		try:
			self.PPC.collectData()
		except e:
			self.failed = True
			raise e
			
if __name__ == '__main__':
	PPC = PrismaPlusController()
	PPC.collectData()
	PPC.saveData()
	PPC.plotData()
	PPC.close()
