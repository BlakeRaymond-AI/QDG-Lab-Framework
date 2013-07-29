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
	
	def __init__(self, 	port = 0,
						duration_s = 10,
						gType = gasTypes['AIR'], 
						pUnits = pressureUnits['TORR'],
						tUnits = temperatureUnits['CELSIUS']
						):
		super(MKS_SRG3_Controller, self).__init__(port = port, timeout = 0)
		self.duration_s = duration_s
		self.MKSThread = DataCollectionThread(self)
		self.gType = gType
		self.setGasType(gType)		
		self.pUnits = pUnits
		self.setPressureUnits(pUnits)
		self.tUnits = tUnits
		self.setTemperatureUnits(tUnits)

	def write(self, msg):
		msg = msg + "\r"
		super(MKS_SRG3_Controller, self).write(msg)
		sleep(0.5)
		
	def close(self):
		self.write("rtl")
		super(MKS_SRG3_Controller, self).close()
		
	def start(self):
		self.write("sta")
		self.MKSThread.start()
		
	def stop(self):
		self.MKSThread.join()
		self.write("stp")
		self.close()
	
	def waitRead(self):
		sleep(2.)
		data = self.read(256)
		return data
				
	def setGasType(self, gType):
		msg = "".join([str(gType), " gas"])
	
	def setPressureUnits(self, pUnits):
		msg = "".join([str(pUnits), " unt"])
		self.write(msg)
		
	def setTemperatureUnits(self, tUnits):
		msg = "".join([str(tUnits), " tsc"])	
	
	def setGasTemperature(self, degrees):
		msg = "".join([str(degrees), " tmp"]) 
		self.write(msg)
	
	def determineBackground(self, numSamples):
		if (numSamples <=1):
			print "Averaging Deactivated"
		if (numSamples > 50):
			print "Number of samples must be in range [0,50]"
		msg = "".join([str(numSamples), " bga"])
		self.write(msg)
		
	def getMeasurementTime(self):
		self.write("mti")
		
	def getPressure(self):
		self.flushInput()
		self.write("val")
		data = self.waitRead()
		val = float(data[1:-3])
		return val
		
	def getZeroOffset(self):
		self.write("ofs")
		data = self.waitRead()

	def timeForNextReading(self):
		self.flushInput()
		self.write("rem")
		data = self.waitRead()
		val = float(data[1:-3])
		return val

	def collectData(self):
		duration_s = self.duration_s
		tDat = []
		pDat = []
		tStart = time()
		tEnd = tStart + duration_s
		while (time() < tEnd):
			timeLeftOld = 70 # Larger than max wait time (intentional)
			timeLeftNew = self.timeForNextReading()
			while (timeLeftNew < timeLeftOld):
				timeLeftOld = timeLeftNew
				timeLeftNew = self.timeForNextReading()
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
		'''Plots the data collected by the MKS SRG3 Gauge.'''
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