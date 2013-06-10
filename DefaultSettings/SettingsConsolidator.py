from cameraSettings import cameraSettings
from coilSettings import coilSettings


# Store all settings dicts associated with devices in this dictionary. Data
# format is (Constructor Name, Initialisation Settings). 
deviceSettings = {'CamController' : ('CameraController', cameraSettings)}
# Store all other settings dicts in this dictionary
generalSettings = {'coilSetting' : coilSettings}


defaultSettings = { 
	'deviceSettings' : deviceSettings,
	'generalSettings' : generalSettings
	}
	
