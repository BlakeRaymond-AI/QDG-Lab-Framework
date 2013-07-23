# Victor Barua for UBC QDG Lab
# 02/05/2013
# LabJack Device Controller

from ctypes import *
import numpy as np
import csv
from threading import Thread

cDrivers = WinDLL("ljackuw.dll")

class LabJackError(Exception):
	"""Displays errors returned from c driver calls."""
	def __init__(self, errorCode):
		self.errorCode = errorCode
	
	def __str__(self):
		errorCode = c_long(self.errorCode)
		errorString = (c_char*50)()
		cDrivers.GetErrorString(errorCode, byref(errorString))
		errorString = [c for c in errorString if c != "\x00"]
		result = ''
		for c in errorString:
			result = result + c
		return repr(result)
		
class LabJackSettingsException(Exception):
	"""Displays errors related to controller settings."""
	def __init__(self, msg):
		self.msg = msg
		
	def __str__(self):
		return repr(self.msg)	

class LabJackController(object):
	"""
	LabJack Control Class. Instantiate an instance with the desired settings
	and then call collectData() on it to collect voltage data.  A subsequent
	call to save() wil then save this data. Controller can be set to trigger
	on a rising input. Uses ctypes to call LabJack c drivers so make sure 
	they're installed. Time data is recorded in seconds and voltage data in
	volts.
	
	To run in a separate thread, call start() instead of collectData(). Then
	before calling save(), call stop().
	"""
		
	def __init__(self, activeChannels = [0], sampleRatePerChannel = 200, scanDuration = 5, trigger = False, triggerChannel = 0, idnum=-1):
		"""
		Parameters:
		activeChannels: Array of size 1,2 or 4 indicating which channels 
							to collect data from.
		sampleRatePerChannel: Number of samples take per channel per second.
		scanDuration: Time over which to collect data (in seconds).
		trigger: Determines whether a trigger will be used.
		triggerChannel: Digital IO channel to use as trigger.
		idnum: Local ID of LabJack to utilize. -1 uses first available 
					LabJack.
		"""
		self.idnum = idnum
		self.activeChannels = activeChannels
		self.numChannels = len(activeChannels)
		self.scanDuration = long(scanDuration)
		aggSampleRate = sampleRatePerChannel*len(activeChannels)
		if not (200 <= aggSampleRate <= 1200):
			msg = "The aggregate sample rate over all channels must be between 200 - 1200 samples per second. Currently %d." % aggSampleRate
			raise LabJackSettingsException(msg)
		self.sampleRatePerChannel = sampleRatePerChannel
		self.data = []
		if trigger:
			self.LJThread = TriggerThread(self, self.triggerChannel)
		else:
			self.LJThread = DataCollectionThread(self)
		
	def ErrorHandler(self, errorCode):
		"""
		Checks the error code returned by cDriver function calls and
		raises an exception if necessary.
		"""
		if (errorCode != 0): raise LabJackError(errorCode)
	
	def start(self):
		"""Starts the thread in charge of collecting data."""
		self.LJThread.start()
		
	def stop(self):
		"""Waits until data collection is complete before proceeding."""
		self.LJThread.join()
		
	def collectData(self):
		"""Initiates data collection."""
		data = []
		self.startStream()
		for r in np.arange(self.scanDuration): # 1 second per read.
			data.append(self.readStream())
		self.endStream()
		self.data = data	
	
	def save(self, fname = 'LabJackData.csv'):
		"""Saves data collected by collectData call."""
		channelDataFull = [[]]*self.numChannels
		data = self.data	
		# data is an array of 4096 by 4 arrays.
		for dataArray in data:
			for scan in dataArray:
				for i in range(self.numChannels):
					channelDataFull[i].append(scan[i])	
		channelDataFiltered = []		
		for ch in channelDataFull:
			channelDataFiltered.append([c for c in ch if c < 9999.])
		time = np.arange(len(channelDataFiltered[0])) / float(self.sampleRatePerChannel)
		data = [time]
		labels = ["Time (s)"]
		for ch in channelDataFiltered:
			data.append(ch)			
		for ch in (self.activeChannels):
			labels.append("Channel " + str(ch) + " (V)")
		self.data = data
		self.labels = labels
		self.outputter(data, labels, fname)

	def plotData(self, fname = 'LabJackDataPlot.png'):
		'''Plots the data collected by the LabJack.'''
		import matplotlib.pyplot as plt
		data = self.data
		labels = self.labels
		time = data[0]
		for i in range(1, len(data)):
			lbl = labels[i]
			plt.plot(time, data[i], label = lbl)
		plt.xlabel('Time (s)')
		plt.ylabel('Voltage (V)')
		plt.legend()
		plt.savefig(fname)
		
	def outputter(self, dataArray, labelArray, fileName):
		"""Formats data collected by LabJack into an appropriates CSV format"""
		csvFile =  open(fileName, 'wb')
		try:
			fileWriter = csv.writer(csvFile, delimiter=',')
			fileWriter.writerow(labelArray)
			for i in range(len(dataArray[0])):	# Num of data points.
				output = [];
				for j in range(len(dataArray)): # Num of distinct data types.
					output.append(dataArray[j][i])
				fileWriter.writerow(output);				
		finally:
			csvFile.close()
			
	def readDigitalIn(self, channel):
		"""Read the values of one of the digital inputs"""	
		idnum = c_long(self.idnum)
		demo = c_long(0)
		state = c_long(0)
		errorCode = cDrivers.EDigitalIn(byref(idnum), demo, c_long(channel), c_long(0), byref(state))
		self.ErrorHandler(errorCode)
		return state.value  	

	def startStream(self):
		"""Opens a stream to begin analog data collection on a LabJack."""
		# Important Settings Variables
		idnum = c_long(self.idnum)
		numChannels = c_long(self.numChannels)
		channels = (c_long * numChannels.value)()
		for i in range(numChannels.value):
			channels[i] = self.activeChannels[i]
		sampleRatePerChannel = c_float(self.sampleRatePerChannel)
		
		# Function Filler
		demo = c_long(0) 
		stateIOin = c_long(0)
		updateIO = c_long(0) 
		ledOn = c_long(1)
		gains = (c_long * numChannels.value)()
		disableCal = c_long(0)
		reserved1 = c_long(0)
		readCount = c_long(0)
		
		errorCode = cDrivers.AIStreamStart(byref(idnum), demo, stateIOin, updateIO, ledOn, numChannels, byref(channels), byref(gains), byref(sampleRatePerChannel), disableCal, reserved1, readCount)
		self.ErrorHandler(errorCode)
		
		print "LabJack Stream Opened"		
		self.idnum = idnum.value		# Update idnum to local id.
		self.sampleRatePerChannel = int(sampleRatePerChannel.value)	# Update scan rate to that given by LabJack.	

	def readStream(self):
		"""Retrieve data from running LabJack stream."""
		# Important Settings Variables
		localID = c_long(self.idnum)
		numScans = c_long(self.sampleRatePerChannel)	# Pull data once every second.
		timeout = c_long(3)
		
		# Function Filler
		voltages = ((c_float*4)*4096)()
		stateIOout = (c_long*4096)()
		reserved = c_long(0)
		ljScanBacklog = c_long(0)
		overVoltage = c_long(0)
			
		errorCode = cDrivers.AIStreamRead(localID, numScans, timeout, byref(voltages), byref(stateIOout), byref(reserved), byref(ljScanBacklog), byref(overVoltage))
		self.ErrorHandler(errorCode)
		return voltages

	def endStream(self):
		"""Closes the LabJack stream."""
		localID = c_long(self.idnum)
		errorCode = cDrivers.AIStreamClear(localID)
		self.ErrorHandler(errorCode)
		print "LabJack Stream Closed"
		
	def setSoftTrigger(self, channel):
		"""Causes LabJack to utilize trigger."""
		while (readDigitalIn(channel) == 0):
			pass				
			
class TriggerThread(Thread):
	"""
	Trigger threads will wait for the channel set in setTrigger to go high
	before beginning data collection. Note that there is a relatively large
	delay between triggering and data collection.f
	"""

	def __init__(self, LJController, triggerChannel):
		Thread.__init__(self)
		self.LJC = LJController 
		self.triggerChannel = triggerChannel
		
	def run(self):
		LJC = self.LJC
		LJC.setSoftTrig(triggerChannel)
		LJC.collectData()
		
class DataCollectionThread(Thread):
	"""Data collection threads collect data."""
	
	def __init__(self, LJController):
		Thread.__init__(self)
		self.LJC = LJController 
		
	def run(self):
		self.LJC.collectData()

if __name__ == '__main__':			
	# Creates a default LabJackController to collect and save data.
	LJC = LabJackController()
	LJC.collectData()
	LJC.save()
	
# Using LabJackController with start and stop.
# 	LJC = LabJackController()
# 	LJC.start()
# 	print "OTHER CODE HERE"
# 	LJC.stop()
# 	LJC.save()	
	