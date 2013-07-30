from DeviceControllers.PixeLinkController.CameraController import CameraController as Pixelink_Controller
from DeviceControllers.PixeLinkController.frame_handler_basic import FramesHandler

class PixeLinkMediator(object):
	
	def __init__(self, dictionary):
		for (k, v) in dictionary.items():
			setattr(self, k, v)
		self.controller = Pixelink_Controller()
		if self.useROICenter:
			self.setROICenter()
		self.checkROI()
		ROI = self.ROI()
		self.controller.set_roi(*ROI)
		self.controller.set_exposure_time_ms(self.expTime_ms)
		self.controller.set_gain(self.gain)
		self.controller.set_external_trigger()
		
		self._imagelist = []
		self.framesHandler = FramesHandler()
	
	def setNumberOfImages(self, numberOfImages):
		self.numberOfImages = numberOfImages
				
	def start(self):
		self.framesHandler.N = self.numberOfImages
		self.controller.start(self.numberOfImages, self.framesHandler)
		print "PixeLink camera set. Waiting for %d triggers." % self.numberOfImages
		
	def stop(self):
		print "Waiting for PixeLink Camera to finish."
		self.controller.T.join()
		print "PixeLink Done"
		
	def save(self, path):
		self.framesHandler.save_frames(folder = path, data = False) 
		
	def processExpData(self, pth):
		pass
	
	def setROICenter(self):
		cx, cy, w, h = self.ROI_center[0], self.ROI_center[1], self.ROI_width, self.ROI_height
		self.ROI_left = cx - w/2
		self.ROI_top = cy - h/2
		self.ROI_width = w
		self.ROI_height = h
		
	def ROI(self):
		ROI = (self.ROI_left, self.ROI_top, self.ROI_width, self.ROI_height)
		return ROI	
		
	def checkROI(self):
		left = self.ROI_left
		if left < 0:
			left = 0
		elif left > 1272:
			left = 1272
		self.ROI_left = int(left/8)*8
		
		top = self.ROI_top
		if top < 0:
			top = 0
		elif top > 1016:
			top = 1016
		self.ROI_top = top
		
		width = self.ROI_width
		if width < 8:
			width = 8
		elif width > 1280 - left:
			width = 1280 - left
		self.ROI_width = int(width/8)*8
		
		height = self.ROI_height
		if height < 8:
			height = 8
		if height > 1024 - top:
			rop = 1024 - top
		self.ROI_top = int(top/8)*8