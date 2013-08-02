from serial import Serial
from threading import Thread
from time import sleep, time
import csv

class Stabil_Ion_Controller(Serial):
	
	def __init__(self, port = 0, duration_s = 10, secondsPerSample = 1):
		super(Stabil_Ion_Controller, self).__init__(port = port, timeout = 0)
		self.flushInput()
		self.duration_s = duration_s
		self.secondsPerSample = secondsPerSample
		self.SIThread = DataCollectionThread(self)
		
	def read(self, size = 32):
		sleep(0.2)
		data = super(Stabil_Ion_Controller, self).read(size)
		data = data[:-2]
		return data
		
	def write(self, msg):
		msg = msg + "\r\n"	
		super(Stabil_Ion_Controller, self).write(msg)
		sleep(0.5)
	
	def start(self):
		self.SIThread.start()
		
	def stop(self):
		"""
		Waits until data collection is complete before proceeding. Returns
		boolean indicating whether data collection failed.
		"""	
		self.SIThread.join()
		self.close()
		return self.SIThread.failed
		
	def IG1On(self):
		self.write("IG1 ON")
		self.flushInput()
	
	def IG1Off(self):
		self.write("IG1 OFF")
		self.flushInput()
		
	def IG2On(self):
		self.write("IG2 ON")
		self.flushInput()
		
	def IG2ff(self):
		self.write("IG2 OFF")
		self.flushInput()
	
	def degasOn(self):
		self.write("DG ON")
		self.flushInput()
				
	def getIG1Pressure(self):
		self.write("DS IG1")
		# try:
		data = self.read()
		value = float(data)
		# except ValueError
		return value
	
	def getIG2Pressure(self):
		self.write("DS IG2")
		data = self.read()
		value = float(data)
		return value

	def collectData(self):
		duration_s = self.duration_s
		secondsPerSample = self.secondsPerSample
		tDat = []
		pDat = []
		tStart = time()
		tEnd = tStart + duration_s
		while (time() < tEnd):
			p = self.getIG1Pressure()
			t = time()
			tDat.append(t)
			pDat.append(p)
			sleep(secondsPerSample - 0.1)
		for i in range(len(tDat)):
			tDat[i] = tDat[i] - tStart
		self.tStart = tStart
		self.tDat = tDat
		self.pDat = pDat	
				
	def saveData(self, fname = "SIPressureData.csv"):		
		csvFile = open(fname, "wb")
		tDat = self.tDat
		pDat = self.pDat
		filewriter = csv.writer(csvFile, delimiter = ',')
		filewriter.writerow(['Start Time:', self.tStart])
		filewriter.writerow(["Time (s)", "Pressures (Torr)"])
		for i in range(len(tDat)):
			output = [tDat[i], pDat[i]]
			filewriter.writerow(output)
		csvFile.close()
		
	def plotData(self, fname = "SIPressurePlot.png"):
		'''Plots the data collected by the Stabil Ion gauge.'''
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
	'''Data collection threads collect data.'''
	
	def __init__(self, SIController):
		Thread.__init__(self)
		self.SIC = SIController
		self.failed = False
		
	def run(self):
		try:
			self.SIC.collectData()
		except:
			self.failed = True
			raise

if __name__ == '__main__':
	SIC = Stabil_Ion_Controller(3, 10, 1)
	SIC.collectData()
	SIC.saveData()
	SIC.plotData()
	SIC.close()
		
			