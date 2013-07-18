from DeviceMediatorInterface import DeviceMediatorInterface
from DeviceControllers.LabJackController import LabJackController

from os import path

class LabJackMediator(DeviceMediatorInterface):
	"""
	Mediator for LabJackController specific to the QDG Framework
	""" 
	
	def __init__(self, dictionary):
		for (k, v) in dictionary.items():
			setattr(self, k, v)	
		self.controller = LabJackController(self.activeChannels,
											self.sampleRatePerChannel, 
											self.scanDuration, 
											self.trigger, 
											self.triggerChannel)
		
	def start(self):
		print "Starting Lab Jack data collection thread."
		self.controller.start()
		
	def stop(self):
		print "Waiting for Lab Jack to finish collecting data."
		self.controller.stop()
		print "Lab Jack Done"

	def save(self, pth):
		fname = path.join(pth, 'LabJackData.csv')
		self.controller.save(fname)
		
	def processData(self, pth):
		pass
		
	
					
	