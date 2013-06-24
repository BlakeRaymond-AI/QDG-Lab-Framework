from os import path

class ScopeController(object):
	
	def __init__(self, dictionary):
		self.settings = dictionary 
		
	def save(self, filePath):
		p = path.join(filePath, 'ScopeDat.txt')	
		f = open(p, 'wb')
		f.write('This is Scope Data.')
		f.close()