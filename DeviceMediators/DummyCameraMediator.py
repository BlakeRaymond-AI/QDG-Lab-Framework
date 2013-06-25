from os import path
from DeviceControllers.DummyCameraController import CameraController

class CameraMediator(object):
	
	def __init__(self, dictionary):
		self.settings = dictionary
		self.takeData = dictionary['takeData']
		self.controller = CameraController(dictionary)
		
	def save(self, fname):
		self.controller.save(fname)
