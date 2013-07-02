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
				
		self.controller = PMDController(self.activeChannels, self.gainSettings, self.sampleRatePerChannel, self.scanDuration, self.vRange, self.trigType, self.boardNum)

	def start(self):
		self.controller.start()
		
	def stop(self):
		self.controller.stop()
		
	def save(self, pth):
		fname = path.join(pth, 'PMDData.csv')
		self.controller.saveData(fname)
		
	def processPMDData(self, pth):
		fname = path.join(pth, 'PMDDataPlot.png')
		self.controller.plotData(fname)
		
	