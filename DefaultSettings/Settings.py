class NonExistentValueError(Exception):
	'''
	Raised by Settings object when modification of an attribute that is not
	associated with it is attempted
	'''
	
	def __init__(self, attrName, clsName):
		self.attrName = attrName
		self.clsName = clsName
		
	def __str__(self):
		msg = repr('The class {0} does not have an attribute named {1}'.format(clsName, attrName))
		return msg
		

class Settings(object):
	'''
	Settings class to control access and manipulation of PAT settings 
	dictionaries.
	'''
	
	def __init__(self, dictionary):
		for (key, value) in dictionary.items():
			setattr(self, key, value)
		
	def modify(self, key, value):
		'''Change the value of an existing setting.'''
		if hasattr(self, key):
			setattr(self, key, value)
		else:
			raise NonExistentValueError(self, key)
			
	def overwrite(self, newDict):
		for (key, value) in newDict.items():
			self.modify(key, value)			