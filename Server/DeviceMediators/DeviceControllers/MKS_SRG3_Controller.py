from serial import Serial
from threading import Thread
from time import sleep, time
import csv

pressureUnits = {
	'PASCAL' : 1,
	'MBAR' : 2,
	'TORR' : 3
}

temperatureUnits = {
	'KELVIN' : 0,
	'CELSIUS' : 1
} 

gasTypes = {
	'AIR' : 9,
	'ARGON' : 10, 
	'ACETHYLENE' : 11,
	'FREON-14' : 12,
	'METHANE' : 13,
	'CARBON_DIOXIDE' : 14,
	'DEUTERIUM' : 15,
	'HYDROGEN' : 16,
	'HELIUM' : 17,
	'HYDROGEN_FLUORIDE' : 18,
	'NITROGEN' : 19,
	'NITROUS_OXIDE' : 20,
	'NEON' : 21,
	'OXYGEN' : 22,
	'SULFUR_DIOXIDE' : 23,
	'SULFUR_HEXAFLUORIDE' : 24,
	'XENON' : 25
}

class MKS_SRG3_Controller(Serial):
	'''
	MKSG SRG3 Control Class. Instantiate an instance with the desired settings
	then call collectData() to collect pressure data. A subsequent call to 
	saveData() will then save this data.
	
	To run in a separate thread, call start() instead of collectData(). Then
	before calling saveData(), call stop().
	'''
	
	
	def __init__(self, 	port = 0,
						duration_s = 10,
						measurementTime_s = 20,
						gType = gasTypes['AIR'], 
						pUnits = pressureUnits['TORR'],
						tUnits = temperatureUnits['CELSIUS']):	
		'''
		Parameters:
		port: COM port to which gauge is connected.
		duration_s: duration of data collection in seconds.
		measurementTime_s: time over which a single measurement will be made.
		gType: the types of gas being measured. See controller file for the numeric codes.
		pUnits: the pressure units used for outputs. See controller file for the numeric codes.
		tUnits: the temperature units used for inputs. See controller file for the numeric codes.
		'''
		super(MKS_SRG3_Controller, self).__init__(port = port, timeout = 0)
		self.duration_s = duration_s
		self.measurementTime_s = measurementTime_s
		self.MKSThread = DataCollectionThread(self)
		self.setMeasurementTime(measurementTime_S)
		self.gType = gType
		self.setGasType(gType)		
		self.pUnits = pUnits
		self.setPressureUnits(pUnits)
		self.pLabel = pressureUnits.keys()[pUnits-1]
		self.tUnits = tUnits
		self.tLabel = temperatureUnits.keys()[tUnits-1]
		self.setTemperatureUnits(tUnits)
		self.write("sta")

	def write(self, msg):
		'''Writes a message to gauge with the correct terminating characters.'''
		msg = msg + "\r"
		super(MKS_SRG3_Controller, self).write(msg)
		sleep(0.5)
		
	def close(self):
		'''Returns control to gauge and closes port connection.'''
		self.write("rtl")
		super(MKS_SRG3_Controller, self).close()
		
	def start(self):
		'''Starts the data collection thread.'''
		self.MKSThread.start()
		
	def stop(self):
		''' Waits for the data collection thread to join then closes the connection.'''
		self.MKSThread.join()
		self.close()
	
	def waitRead(self):
		'''Waits for 2 seconds before reading.'''
		sleep(2.)
		data = self.read(256)
		return data
				
	def setGasType(self, gType):
		'''Sets the gas type.'''
		msg = "".join([str(gType), " gas"])
	
	def setPressureUnits(self, pUnits):
		'''Sets the pressure units.'''
		msg = "".join([str(pUnits), " unt"])
		self.write(msg)
		
	def setTemperatureUnits(self, tUnits):
		'''Sets the temperature units.'''
		msg = "".join([str(tUnits), " tsc"])	
	
	def setGasTemperature(self, degrees):
		'''Sets the gas temperatures. Utilizes the units from setTemperatureUnits.'''
		msg = "".join([str(degrees), " tmp"]) 
		self.write(msg)
	
	def determineBackground(self, numSamples):
		'''Determines the background pressure.'''
		if numSamples <= 1:
			print "Averaging Deactivated"
		if numSamples > 50:
			print "Number of samples must be in range [0,50]"
		msg = "".join([str(numSamples), " bga"])
		self.write(msg)
		
	def getMeasurementTime(self):
		'''Gets the time required to make a measurement.'''
		self.write("mti")
		
	def setMeasurementTime(self, time_s):
		'''Set the time over which a single measurement will be made.'''
		if time_s < 5:
			time_s = 5
			print "!!!!! MKS SRG3 measurment time must be between 5-60 seconds."
		elif time_s > 60:
			time_s = 60
			print "!!!!! MKS SRG3 measurment time must be between 5-60 seconds."
		msg = "".join([str(time_s), " mti"])
		self.write(msg) 
		
	def getPressure(self):
		'''Read the pressure from the gauge.'''
		self.flushInput()
		self.write("val")
		data = self.waitRead()
		val = float(data[1:-3])
		return val
		
	def getZeroOffset(self):
		'''Get the current zero offset.'''
		self.write("ofs")
		data = self.waitRead()

	def timeForNextReading(self):
		'''Time until the next reading will be available.'''
		self.flushInput()
		self.write("rem")
		data = self.waitRead()
		val = float(data[1:-3])
		return val

	def collectData(self):
		'''Collect pressure data from the gauge.'''
		duration_s = self.duration_s
		tDat = []
		pDat = []
		tStart = time()
		tEnd = tStart + duration_s
		while (time() < tEnd):
			timeLeftOld = self.measurementTime_s + 5
			timeLeftNew = self.timeForNextReading()
			while (timeLeftNew < timeLeftOld):
				timeLeftOld = timeLeftNew
				timeLeftNew = self.timeForNextReading()
				sleep(timeLeftNew / 3.)
			p = self.getPressure()
			t = time()
			pDat.append(p)
			tDat.append(t)
		for i in range(len(tDat)):
			tDat[i] = tDat[i] - tStart
		self.tStart = tStart
		self.tDat = tDat
		self.pDat = pDat
		
	def saveData(self, fname = "MKSPressureData.csv"):
		'''Save the data collected by the gauge.'''
		csvFile = open(fname, 'wb')
		tDat = self.tDat
		pDat = self.pDat
		filewriter = csv.writer(csvFile, delimiter = ',')
		filewriter.writerow(['Start Time:', self.tStart])
		filewriter.writerow(["Time (s)", "Pressures (Torr)"])
		for i in range(len(tDat)):
			output = [tDat[i], pDat[i]]
			filewriter.writerow(output)
		csvFile.close()
		
	def plotData(self, fname = "MKSPressurePlot.png"):
		'''Plots the data collected by the gauge.'''
		import matplotlib.pyplot as plt
		plt.clf()
		tDat = self.tDat
		pDat = self.pDat
		plt.plot(tDat, pDat, ls = 'None', marker = '.')
		plt.xlabel('Time (s)')
		plt.ylabel('Pressure (Torr)')
		plt.savefig(fname)		
		plt.clf()	
		
class DataCollectionThread(Thread):
	"""Data collection threads collect data."""
	
	def __init__(self, MKSController):
		Thread.__init__(self)
		self.MKSC = MKSController
		
	def run(self):
		self.MKSC.collectData()	
	
if __name__ == '__main__':
	MKSC = MKS_SRG3_Controller(2, 100)
	MKSC.collectData()
	MKSC.saveData()
	MKSC.plotData()
	MKSC.close()

# Using the controller with start and stop.
#	MKSC = MKS_SRG3_Controller(2, 100)
#	MKSC.start()
# 	print "OTHER CODE HERE"
#	MKSC.stop()
#	MKSC.saveData()
#	MKSC.plotData()
#	MKSC.close()	
	