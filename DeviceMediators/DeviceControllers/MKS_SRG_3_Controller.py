from serial import Serial

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

class SRGSensor(Serial):
	
	def __init__(self, 	port = 0,
						gType = gasTypes['AIR'], 
						pUnits = pressureUnits['PASCAL'],
						tUnits = temperatureUnits['CELSIUS']
						):
		super(SRGSensor, self).__init__(port = port, timeout = 0)
		self.gType = gType
		self.setGasType(gType)		
		self.pUnits = pUnits
		self.setPressureUnits(pUnits)
		self.tUnits = tUnits
		self.setTemperatureUnits(tUnits)
	
	def start(self):
		self.write("sta\r")
		
	def stop(self):
		self.write("stp\r")	
	
	def waitRead(self):
		data = ""
		while data:
			data = self.read(256)
		return data
				
	def setGasType(self, gType):
		msg = "".join([str(gType), " gas\r"])
	
	def setPressureUnits(self, pUnits):
		msg = "".join([str(pUnits), " unt\r"])
		self.write(msg)
		
	def setTemperatureUnits(self, tUnits):
		msg = "".join([str(tUnits), " tsc\r"])	
	
	def setGasTemperature(self, degrees):
		msg = "".join([str(degrees), " tmp\r"]) 
		self.write(msg)
	
	def determineBackground(self, numSamples):
		if (numSamples <=1):
			print "Averaging Deactivated"
		if (numSamples > 50):
			print "Number of samples must be in range [0,50]"
		msg = "".join([str(numSamples), " bga\r"])
		self.write(msg)
		
	def getMeasurementTime(self):
		self.write("mti\r")
		
	def getPressure(self):
		self.write("val\r")
		data = self.waitRead() 	
		
	def getZeroOffset(self):
		self.write("ofs\r")
		data = self.waitRead()
		return data		

