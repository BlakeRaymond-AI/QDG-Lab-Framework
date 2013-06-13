from pprint import PrettyPrinter
from os import path
from pickle import dump

class NonExistentValueError(Exception):
	'''
	Raised by Settings object when modification of an attribute that is not
	associated with it is attempted
	'''
	
	def __init__(self, attrName):
		self.attrName = attrName
		
	def __str__(self):
		msg = 'The attribute {0} does not exist within the specified settings dictionary.'
		msg = repr(msg.format(self.attrName))
		return msg
		

class Settings(dict):
	'''
	Dictionary subclass to control access and manipulation of PAT settings. 
	Values in a Settings dictionary can only be modified. New values cannot be 
	inserted.
	'''

	def __setitem__(self, key, val):
		if key in self:
			dict.__setitem__(self, key, val)
		else:
			raise NonExistentValueError(key)
			
	def __str__(self):
		pp = PrettyPrinter(indent=0)
		return pp.pformat(self)
		
	def save(self, filePath, fname = 'Settings'):
		txtPath = path.join(filePath, ''.join([fname, '.txt']))
		f = open(txtPath, 'wb')
		f.write(str(self))
		f.close()
		picklePath = path.join(filePath, ''.join([fname, '.pkl']))
		f = open(picklePath, 'wb')
		dump(self, f)
		f.close()

	
			
				
		
			