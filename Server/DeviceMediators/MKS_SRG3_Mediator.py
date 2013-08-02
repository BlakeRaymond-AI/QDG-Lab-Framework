from DeviceMediatorInterface import DeviceMediatorInterface
from DeviceControllers.MKS_SRG3_Controller import MKS_SRG3_Controller

from os import path

class MKS_SRG3_Mediator(DeviceMediatorInterface):
	"""
	Mediator for MKS SRG3 specific to the QDG Framework
	""" 
	
	def __init__(self, dictionary):
		for (k, v) in dictionary.items():
			setattr(self, k, v)
		self.controller = MKS_SRG3_Controller(self.port,
												self.duration_s,
												self.measurementTime_s,
												self.gType, 
												self.pUnits,
												self.tUnits)
	def start(self):
		print "Starting MKS SRG3 data collection thread."
		self.controller.start()
		
	def stop(self):
		print "Waiting for MKS SRG3 to finish collecting data."
		self.controller.stop()
		print "MKS SRG3 Gauge Done"

	def save(self, pth):
		fname = path.join(pth, 'MKSData.csv')
		self.controller.saveData(fname)
		
	def processExpData(self, pth):
		fname = path.join(pth, 'MKSDataPlot.png')
		self.controller.plotData(fname)
	