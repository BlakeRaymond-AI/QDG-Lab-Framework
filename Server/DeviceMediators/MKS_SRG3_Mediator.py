from DeviceMediatorInterface import DeviceMediatorInterface
from DeviceControllers.MKS_SRG3_Controller import MKS_SRG3_Controller

from os import path

class MKS_SRG3_Mediator(DeviceMediatorInterface):
	"""
	Mediator for Stabil Ion gauge specific to the QDG Framework
	""" 
	
	def __init__(self, dictionary):
		for (k, v) in dictionary.items():
			setattr(self, k, v)
		self.controller = MKS_SRG3_Controller(self.port)
		
	def start(self):
		print "Starting Stable Ion Gague data collection thread."
		self.controller.start()
		
	def stop(self):
		print "Waiting for Stabil Ion Gauge to finish collecting data."
		self.controller.stop()
		print "Stabil Ion Gauge Done"

	def save(self, pth):
		fname = path.join(pth, 'PressureData.csv')
		self.controller.save(fname)
		
	def processExpData(self, pth):
		pass
		
	
					
	