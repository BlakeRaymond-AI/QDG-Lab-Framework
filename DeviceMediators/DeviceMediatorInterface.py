
class DeviceControllerInterface(object):
	'''
	Interface for device controllers. All devices used in the PAT apparatus
	should implement its methods.
	'''
	
	def save(self, path):
		'''Save the data associated with the device to the path given.'''
		raise NotImplementedError()
		
	def start(self):
		'''Initialise the device for an experimental run.'''
		raise NotImplementedError()
		
	def stop(self):
		'''Stop a device after an experimental run.'''
		raise NotImplementedError()	
 
