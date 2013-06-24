from os import path

class CameraController(object):
	
	def __init__(self, dictionary):
		self.settings = dictionary
		
	def save(self, filePath):
		p = path.join(filePath, 'CameraDat.txt')	
		f = open(p, 'wb')
		f.write('This is Camera Data.')
		f.close()
