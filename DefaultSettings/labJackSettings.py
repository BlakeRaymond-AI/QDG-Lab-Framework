'''Default settings for LabJack'''

labJackSettings = dict()
labJackSettings['activeChannels'] = [0]	# Array of size 1, 2 or 4 (# Valid Channels: 0-7)				
labJackSettings['sampleRatePerChannel'] = 200	# Samples per channel per second. Aggregate
												# rate should not exceed 1200.
labJackSettings['scanDuration'] = 10	# Seconds
labJackSettings['trigger'] = False		# Use trigger.
labJackSettings['triggerChannel'] = 0	# Channel to use as trigger input.

labJackSettings['takeData'] = True
labJackSettings['processData'] = False
labJackSettings['dataFolderName'] = "LabJackData"
