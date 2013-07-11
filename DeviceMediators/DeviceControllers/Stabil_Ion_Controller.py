from serial import Serial
from time import sleep

class Stabil_Ion_Controller(Serial):
	def __init__(self, port = 0):
		super(Stabil_Ion_Controller, self).__init__(port = port, timeout = 0)

	def read(self, size = 1):
		data = super(Stabil_Ion_Controller, self).read(size)
		data = data[:-2]
		return data
		
	def IG1On(self):
		self.write("IG1 ON \r\n")
		self.read(32)	
	
	def IG1Off(self):
		self.write("IG1 OFF \r\n")
		self.read(32)	
	
	def IG2On(self):
		self.write("IG2 ON \r\n")
		self.read(32)
		
	def IG2ff(self):
		self.write("IG2 OFF \r\n")
		self.read(32)			
		
	def degasOn(self):
		self.write("DG ON \r\n")
		self.read(32)
		
	def getIG1Pressure(self):
		self.write("DS IG1 \r\n")
		sleep(0.1)
		data = self.read(32)
		value = float(data)
		return value
	
	def getIG2Pressure(self):
		self.write("DS IG2 \r\n")
		data = self.read(32)
		sleep(0.1)
		value = float(data)
		return value	