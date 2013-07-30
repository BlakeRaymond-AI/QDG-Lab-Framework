from Settings import Settings

from DefaultSettings.PMDSettings import PMDSettings
from DefaultSettings.LabJackSettings import LabJackSettings
from DefaultSettings.Stabil_Ion_Settings import Stabil_Ion_Settings
from DefaultSettings.MKS_SRG3_Settings import MKS_SRG3_Settings

from DefaultSettings.PixeLinkSettings import PixeLinkSettings
from DefaultSettings.PATSettings import PATSettings
from DefaultSettings.PATClientSettings import PATClientSettings	
from DefaultSettings.OptimizerSettings import OptimizerSettings

# Store all settings dicts associated with devices in this dictionary. Data
# format is:
# 'Device Name in PAT Controller': (Constructor Name, Initialisation Settings). 
deviceSettings = {
	'PMD' : ('PMDMediator', PMDSettings),
	'LabJack': ('LabJackMediator', LabJackSettings),
	'Stabil_Ion' : ('Stabil_Ion_Mediator', Stabil_Ion_Settings),
	'MKS_SRG3' : ('MKG_SRG3_Mediator', MKG_SRG3_Settings),
	'PixeLink' : ('PixeLinkMediator', PixeLinkSettings),
	'Optimizer' : ('OptimizerMediator', OptimizerSettings),
}

# Store all other settings dicts in this dictionary
generalSettings = {
	'PATSettings' : ('Settings', PATSettings),
	'PATClient' : ('PATClient', PATClientSettings),
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
		
	
	
		



