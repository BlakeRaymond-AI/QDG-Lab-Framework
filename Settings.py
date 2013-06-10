from QDGErrors import NonExistentValueError


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