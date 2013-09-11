import socket
import time
from threading import Thread
import csv
import os
from OpenOPC import OpenOPC as opc

PRISMA_ADDR = '192.168.1.254'

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
		self.close()
		return self.PPCThread

class DataCollectionThread(Thread):
	"""Data collection threads collect data."""
	def __init__(self, PPController):
		Thread.__init__(self)
		self.PPC = PPController
		self.failed = False

	def run(self):
		try:
			self.PPC.colectData()
		except e:
			self.failed = True
			raise e
