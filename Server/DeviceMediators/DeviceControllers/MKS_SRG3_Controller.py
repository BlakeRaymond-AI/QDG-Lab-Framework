from serial import Serial
from time import sleep

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
						gType = gasTypes['AIR'], 
						pUnits = pressureUnits['TORR'],
						tUnits = temperatureUnits['CELSIUS']
						):
		super(MKS_SRG3_Controller, self).__init__(port = port, timeout = 0)
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
		
	def stop(self):
		self.write("stp")	
	
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
		return data
		
if __name__ == '__main__':
	MKS_SRG3_C = MKS_SRG3_Controller(port = 2)
	print MKS_SRG3C.getPressure()
	MKS_SRG3C.close()