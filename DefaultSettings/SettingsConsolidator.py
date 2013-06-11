from cameraSettings import cameraSettings
from scopeSettings import scopeSettings
from coilSettings import coilSettings
from PATSettings import PATSettings
from saveSettings import saveSettings

# Store all settings dicts associated with devices in this dictionary. Data
# format is (Constructor Name, Initialisation Settings). 
deviceSettings = {
	'CamController' : ('CameraController', cameraSettings),
	'ScopeController' : ('ScopeController', scopeSettings)
}

# Store all other settings dicts in this dictionary
generalSettings = {
	'PATSettings' : ('Settings', PATSettings),
	'SaveController' : ('SaveController', saveSettings),
	
	'coilSetting' : ('Settings', coilSettings)
}

defaultSettings = { 
	'deviceSettings' : deviceSettings,
	'generalSettings' : generalSettings
}