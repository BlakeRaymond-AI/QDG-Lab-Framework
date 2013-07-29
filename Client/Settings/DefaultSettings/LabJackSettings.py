'''Default settings for LabJack'''
LabJackSettings = dict()
LabJackSettings['activeChannels'] = [0]	# Array of size 1, 2 or 4 (# Valid Channels: 0-7)				
LabJackSettings['sampleRatePerChannel'] = 200	# Samples per channel per second. Aggregate
												# rate should be between 200 and 1200.
LabJackSettings['scanDuration'] = 10	# Seconds
LabJackSettings['trigger'] = False		# Use trigger.
LabJackSettings['triggerChannel'] = 0	# Channel to use as trigger input.
LabJackSettings['takeData'] = False
LabJackSettings['processData'] = False
LabJackSettings['dataFolderName'] = "LabJackData"
