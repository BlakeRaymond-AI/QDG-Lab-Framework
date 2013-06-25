from os import path
from DeviceControllers.DummyScopeController import ScopeController

class ScopeMediator(object):
	
	def __init__(self, dictionary):
		self.settings = dictionary
		self.takeData = dictionary['takeData']
		self.device = ScopeController(dictionary)
		
	def save(self, fname):
		self.device.save(fname)	

