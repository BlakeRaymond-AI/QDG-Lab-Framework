from Settings import Settings
from Settings.labJackSettings import labJackSettings
from Settings.PATSettings import PATSettings
from Settings.PMDSettings import PMDSettings
from Settings.Stabil_Ion_Settings import Stabil_Ion_Settings
from Settings.saveSettings import saveSettings	

# Store all settings dicts associated with devices in this dictionary. Data
# format is:
# 'Device Name in PAT Controller': (Constructor Name, Initialisation Settings). 
deviceSettings = {
	'PMD' : ('PMDMediator', PMDSettings),
#	'LabJack': ('LabJackMediator', labJackSettings),
	'SI' : ('Stabil_Ion_Mediator', Stabil_Ion_Settings)
}

# Store all other settings dicts in this dictionary
generalSettings = {
	'PATSettings' : ('Settings', PATSettings),
	'SaveController' : ('SaveController', saveSettings),
}

# In general the code below does not need to be modified.
### ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ###
# Converts dictionaries into Settings to promote immutability.
for (key, (constructor, settings)) in deviceSettings.items():
	deviceSettings[key] = (constructor, Settings(settings))
for (key, (constructor, settings)) in generalSettings.items():
	generalSettings[key] = (constructor, Settings(settings))
deviceSettings = Settings(deviceSettings)
generalSettings = Settings(generalSettings)

defaultSettings = { 
	'deviceSettings' : deviceSettings,
	'generalSettings' : generalSettings
}

defaultSettings = Settings(defaultSettings)

def overwriteSettings(default, updatePackage):
	'''
	Overwrites the settings in the default settings dictionary with the
	updated ones.
	'''
	deviceSettings = default['deviceSettings']
	generalSettings = default['generalSettings']
	
	for key, updatedSettings in updatePackage.items():
		if key in deviceSettings:
			deviceSettings[key][1].update(updatedSettings)
		if key in generalSettings:
			generalSettings[key][1].update(updatedSettings)
	
	return default
		
	
	
		



