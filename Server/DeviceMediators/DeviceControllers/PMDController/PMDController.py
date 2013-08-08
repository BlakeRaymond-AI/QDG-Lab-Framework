from ctypes import *
from ctypes.wintypes import *

from PMDTypes import TrigType, Options, Range
from threading import Thread
from math import ceil
from time import time
import numpy as np
import csv

driver = WinDLL('cbw32')
						
class PMDError(Exception):
	'''For errors returned from c driver calls.'''
	def __init__(self, errCode):
		self.errCode = errCode
		errStr = (c_char*256)()
		driver.cbGetErrMsg(c_int(errCode), byref(errStr))
		self.msg = errStr.value
		print "Error Code: ", self.errCode
		
	def __str__(self,):
		return repr(self.msg)

class PMDSettingsException(Exception):
	'''For errors related to controller settings.'''
	def __init__(self, msg):
		self.msg = msg
		
	def __str__(self):
		return repr(self.msg)				
				
class PMDController(object):
	'''
	PMD Controller Class. Instantiate an instance with the desired settings
	
	'''
	
	def __init__(self, activeChannels = [0],
						gainSettings = [0],
						sampleRatePerChannel=5000, 
						scanDuration = 5.0,
						vRange = 'BIP10VOLTS',
						trigger = False,
						trigType = 'TRIG_POS_EDGE',
						boardNum = 0):
		'''
		Parameters:
		activeChannels:	Array of channels from which to record data.
		gainSettings: Array of gain settings for each of the channels.
		sampleRatePerChannel: Sample rate per channel.
		scanDuration: Duration of scan in seconds.
		vRange: Voltage range identifier code from PMDTypes.
		trigger: Boolean to indicate whether a trigger should be used or not.
		trigType: Trigger type identifier code to use from PMDTypes.
		boardNum: Board number registered through InstaCal program.
		
		Notes:
		- activeChannels and gainSettings must have the same size.
		'''				
		print "!!!!!!!!!!!!! TRIGGER:", trigger				
 		self.boardNum = boardNum
		vRange = Range[vRange]
		trigType = TrigType[trigType]
		if len(activeChannels) != len(gainSettings):
			raise PMDSettingsException("The activeChannels and gainSettings arrays must have the same size.")
		self.activeChannels = activeChannels
		self.gainSettings = gainSettings
		self.numOfChannels = len(activeChannels)
		if (self.numOfChannels * sampleRatePerChannel > 50000):
			msg = "The aggregate sample rate over all channels must be less than 50000 samples per second. Currently %d." % self.numOfChannels * sampleRatePerChannel > 50000
			raise PMDSettingsException(msg)
		self.sampleRatePerChannel = sampleRatePerChannel
		self.totalSampleRate = sampleRatePerChannel * self.numOfChannels
		self.scanDuration = scanDuration
		self.trigger = trigger
		self.trigType = TrigType['TRIG_POS_EDGE']
		self.vRange = vRange
		self.PMDThread = PMDThread(self)
		
		# Force manual handling of errors.
		self.handleError(driver.cbErrHandling(0, 0))
	
	def handleError(self, errCode):
		'''Handles error codes returned from the Universal Library API'''
		if errCode:
			raise PMDError(errCode)

	def start(self):
		'''Starts the thread in charge of collecting data.'''
		self.PMDThread.start()
		
	def stop(self):
		"""
		Waits until data collection is complete before proceeding. Returns
		boolean indicating whether data collection failed.
		"""
		self.PMDThread.join()
		return self.PMDThread.failed

	def saveData(self, fname= 'PMDData.csv'):
		'''Saves the data collected by the PMD.'''
		data = self.data
		csvFile = open(fname, 'wb')
		labels = ['Time']
		for ch in self.activeChannels:
			labels.append(''.join(['Channels: ', str(ch)]))
		try:
			filewriter = csv.writer(csvFile, delimiter=',')
			filewriter.writerow(['Start Time (No Trigger):', self.tStart])
			filewriter.writerow(labels)
			for i in range(len(data[0])):
				output = []
				for j in range(len(data)):
					output.append(data[j][i])
				filewriter.writerow(output)
		finally:
			csvFile.close()  	

	def collectData(self):
		'''Sets up raw data collection and executes on trigger.'''
		self.setChannels()
		self.setDigitalTrigger()
		self.setStream()

	def processData(self):
		'''Processes the raw data.'''
		self.retrieveData()
		self.convertData()
		self.splitChannels()

	def setDigitalTrigger(self):
		'''Sets the digital trigger types based on the trigType input.'''
		self.handleError(driver.cbSetTrigger(self.boardNum, self.trigType, 0, 3000))
	
	def setChannels(self):
		'''Sets the channels over which data will be taken.'''
		numOfChannels = self.numOfChannels
		chanArr = (c_ushort*numOfChannels)()
		gainArr = (c_ushort*numOfChannels)()
		for i in range(numOfChannels):
			chanArr[i] = self.activeChannels[i] 
			gainArr[i] = self.gainSettings[i]
		self.handleError(driver.cbALoadQueue(self.boardNum, chanArr, gainArr, numOfChannels))
	
	def setStream(self):
		'''Sets the scan which will be initiated upon triggering.'''
		numOfSamples = int(ceil(self.totalSampleRate * self.scanDuration))
		self.numOfSamples = numOfSamples
		numOfSamples = c_long(numOfSamples)
		winBufferHandle = driver.cbWinBufAlloc(numOfSamples)
		self.winBufferHandle = winBufferHandle
		if (winBufferHandle == 0):
			print "!!!!! BUFFER NOT ALLOCATED !!!!!"
		sampleRatePerChannel = c_long(self.totalSampleRate / self.numOfChannels)
		options = Options['BLOCKIO'] | Options['CONVERTDATA']
		if self.trigger:
			print options
			options = options | Options['EXTTRIGGER']
			print options
		self.tStart = time()
		self.handleError(driver.cbAInScan(self.boardNum, 0, 0, numOfSamples, byref(sampleRatePerChannel), self.vRange[0], winBufferHandle, options))
		self.sampleRatePerChannel = sampleRatePerChannel.value	
			
	def retrieveData(self):
		'''
		Retrieves the data from the windows buffer to which it is allocated
		during the scan.
		'''
		numOfSamples = self.numOfSamples
		buffer = (c_ushort*numOfSamples)()
		self.handleError(driver.cbWinBufToArray(self.winBufferHandle, byref(buffer), 0, c_long(numOfSamples)))
		self.data = buffer[:]	
	
	def convertData(self):
		'''
		Converts digital values obtained in scan to corresponding analog
		values.
		'''
		vLow = self.vRange[1]
		vHigh = self.vRange[2]
		vIncrement = (vHigh-vLow)/(2.**12)
		data = self.data
		for i in range(self.numOfSamples):
			data[i] = vLow + data[i]*vIncrement
			
	def splitChannels(self):
		'''
		Splits the retrieved data into its corresponding channels and determines
		the time at which each sample occurred.
		'''
		allData = self.data
		numOfChannels = self.numOfChannels
		data = [[]]*numOfChannels
		for i in range(numOfChannels):
			data[i] = allData[i::numOfChannels]
		tDat = np.arange(len(data[0]))/float(self.sampleRatePerChannel)
		self.data = [tDat] + data
		
	def analogIn(self, channel):
		'''Determines the voltage input for the specified analog channel.'''
		voltage = c_ushort(0)
		self.handleError(driver.cbAIn(self.boardNum, channel, self.vRange[0], byref(voltage)))
		voltage = self.vRange[1] + (self.vRange[2]-self.vRange[1])/(2.**12) * voltage.value
		return voltage	
	
	def plotData(self, fname = 'PMDDataPlot.png'):
		'''Plots the data collected by the PMD.'''
		import matplotlib.pyplot as plt
		plt.clf()
		data = self.data
		tDat = data[0]
		for i in range(1, len(data)):
			lbl = "Channel " + str(self.activeChannels[i-1])
			plt.plot(tDat, data[i], label = lbl, ls = 'None', marker = '.')
		plt.xlabel('Time (s)')
		plt.ylabel('Voltage (V)')
		plt.legend()
		plt.savefig(fname)
		plt.clf()
		
class PMDThread(Thread):
	'''Thread for data collection.'''
	
	def __init__(self, PMDController):
		Thread.__init__(self)
		self.PMDC = PMDController
		self.failed = False
	
	def run(self):
		try:
			self.PMDC.collectData()
			self.PMDC.processData()
		except:
			self.failed = True
			raise

if __name__ == '__main__':	
	PMDC = PMDController()
	PMDC.collectData()
	PMDC.processData()
	PMDC.saveData()
	