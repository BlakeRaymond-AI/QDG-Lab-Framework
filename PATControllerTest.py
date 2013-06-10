from Settings import Settings
from DummyCameraController import CameraController


class PATController(object):
	
	def __init__(self, settingsDictionary):
		
		self.deviceDict = {}
		deviceSettings  = settingsDictionary.pop('deviceSettings', {})
		generalSettings = settingsDictionary.pop('generalSettings', {})
		
		
		# Create device controllers using device settings.
		for (key, deviceData) in deviceSettings.items():
			constructor = globals()[deviceData[0]]
			self.deviceDict[key] = constructor(deviceData[1])
			
		# Create settings objects from general settings.
		for (key, dictionary) in generalSettings.items():
			setattr(self, key, Settings(dictionary))
			
			
	# Changing settings during a run is bad because it won't be save in the logs.
	# Create a new PAT controller instead?	
	
	def overwriteSettings(self, dictOfDicts):
		'''
		Overwrites the current settings of the PAT Controller with those of
		dictionary of dictionaries passed in.
		'''
		for (key, dictionary) in dictOfDicts.items():
			getattr(self, key).overwrite(dictionary)
			
			
			



			