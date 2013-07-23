from DeviceMediatorInterface import DeviceMediatorInterface
from DeviceControllers.PMDController.PMDController import PMDController

from os import path

class PMDMediator(DeviceMediatorInterface):
	"""
	Mediator for PMDController specific to the QDG Framework
	""" 
	
	def __init__(self, dictionary):
		for (k, v) in dictionary.items():
			setattr(self, k, v)
				
		self.controller = PMDController(self.activeChannels, 
										self.gainSettings,
										self.sampleRatePerChannel,
										self.scanDuration,
										self.vRange,
										self.trigger,
										self.trigType, 
										self.boardNum)

	def start(self):
		print "Starting PMD data collection thread."
		self.controller.start()
		
	def stop(self):
		print "Waiting for PMD to finish collecting data."
		self.controller.stop()
		print "PMD Done"
		
	def save(self, pth):
		fname = path.join(pth, 'PMDData.csv')
		self.controller.saveData(fname)
		
	def processExpData(self, pth):
		fname = path.join(pth, 'PMDDataPlot.png')
		self.controller.plotData(fname)
		
	