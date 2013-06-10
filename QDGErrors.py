class PATError(Exception):
	def __str__(self):
		return repr('An error has occured with the PAT apparatus')
	
class NonExistentValueError(PATError):
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