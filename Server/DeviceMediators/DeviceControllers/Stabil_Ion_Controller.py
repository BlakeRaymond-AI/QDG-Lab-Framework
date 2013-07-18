from serial import Serial
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
		data = super(Stabil_Ion_Controller, self).read(size)
		data = data[:-2]
		return data
		
	def write(self, msg):
		msg = msg + "\r\n"	
		super.(Stabil_Ion_Controller, self).write(msg)
	
	def start(self):
		self.SIThread.run()
		
	def stop(self):
		self.SIThread.join()
		
	def IG1On(self):
		self.write("IG1 ON")
		sleep(0.5)
		self.flushInput()
	
	def IG1Off(self):
		self.write("IG1 OFF")
		sleep(0.5)
		self.flushInput()
		
	def IG2On(self):
		self.write("IG2 ON")
		sleep(0.5)
		self.flushInput()
		
	def IG2ff(self):
		self.write("IG2 OFF")
		sleep(0.5)
		self.flushInput()
	
	def degasOn(self):
		self.write("DG ON")
		sleep(0.5)
		self.flushInput()
				
	def getIG1Pressure(self):
		self.write("DS IG1")
		sleep(0.1)
		data = self.read()
		value = float(data)
		return value
	
	def getIG2Pressure(self):
		self.write("DS IG2")
		data = self.read()
		sleep(0.1)
		value = float(data)
		return value

	def collectData(self, duration_s, secondsPerSample):
		duration_s = self.duration_s
		secondsPerSample = self.secondsPerSample
		tDat = []
		pDat= []
		tStart = time()
		tEnd = tStart + duration_s
		while (time() < tEnd):
			p = self.getIG1Pressure()
			tDat.append(time())
			pDat.append(p)
			sleep(secondsPerSample - 0.1)
		for i in range(len(tDat)):
			tDat[i] = tDat[i] - tStart
		self.tDat = tDat
		self.pDat = pDat	
				
	def saveData(fname = "PressureData.csv"):		
		csvFile = open(fname, "wb")
		tDat = self.tDat
		pDat = self.pDat
		filewriter = csv.writer(csvFile, delimiter = ',')
		filewriter.writerow(["Time (s)", "Pressures (???)"])
		for i in range(len(tDat)):
			output = [tDat[i], pDat[i]]
			filewriter.writerow(output)
		csvFile.close()

class DataCollectionThread(Thread):
	"""Data collection threads collect data."""
	
	def __init__(self, SIController):
		Thread.__init__(self)
		self.SIC = SIController
		
	def run(self):
		self.SIC.collectData()
