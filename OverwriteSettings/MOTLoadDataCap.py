'''Updates default settings to allow for acquisition of MOT loading data.'''

labJackSettings = dict()
labJackSettings['activeChannels'] = [0]	# Arrays of size 1, 2 or 4 (# Valid Channels: 0-7)				
labJackSettings['sampleRatePerChannel'] = 200
labJackSettings['scanDuration'] = 20	# Seconds

PMDSettings = dict()
PMDSettings['activeChannels'] = [0]
PMDSettings['gainSettings'] = [0]	
PMDSettings['sampleRatePerChannel'] = 200	#Samples per Second
PMDSettings['scanDuration'] = 1000	# Seconds

updatePackage = {
	'LabJack': labJackSettings,
	'PMD': PMDSettings
	}