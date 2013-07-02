from Settings import Settings
from coilSettings import coilSettings
from labJackSettings import labJackSettings
from PATSettings import PATSettings
from PMDSettings import PMDSettings
from saveSettings import saveSettings	

# Store all settings dicts associated with devices in this dictionary. Data
# format is (Constructor Name, Initialisation Settings). 
deviceSettings = {
	'PMD' : ('PMDMediator', PMDSettings),
	'LabJack': ('LabJackMediator', labJackSettings),
}

# Store all other settings dicts in this dictionary
generalSettings = {
	'PATSettings' : ('Settings', PATSettings),
	'SaveController' : ('SaveController', saveSettings),
	'coilSetting' : ('Settings', coilSettings)
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

	



