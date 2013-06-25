from DeviceMediatorInterface import DeviceMediatorInterface
from LabJackController import LabJackController

class LabJackMediator(DeviceMediatorInterface):
	"""
	Mediator for LabJackController specific to the QDG Framework
	""" 
	
	def __init__(self, dictionary):
		for (k, v) in dictionary.items():
			setattr(self, k, v)
		self.controller = LabJackController(self.activeChannels, self.scanDuration, self.trigger)
		
	def start(self):
		self.controller.start()
		
	def stop(self):
		self.controller.stop()

	def save(self, path):
		p = path.join(path, 'LabJackData.txt')
		self.controller.save(p)
					
	