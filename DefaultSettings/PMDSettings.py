'''
Default settings for PMD. Consult PMD API Specification for voltage range
and trigger specifications. Device model is PMD-1208FS (USB-1208FS in manual). 
'''

PMDSettings = dict()
PMDSettings['activeChannels'] = [0]	# Channels to sample.
PMDSettings['gainSettings'] = [0]	# Gain to use on each channel. Should have same
									# size as activeChannels array.
PMDSettings['sampleRatePerChannel'] = 200	# Samples per channel per second. Aggregate
											# rate should not exceed 40000.
PMDSettings['scanDuration'] = 2000	# Seconds
PMDSettings['vRange'] = 'BIP10VOLTS'	# Voltage range being measured.
PMDSettings['trigType'] = 'TRIG_POS_EDGE'	# Trigger type to use
PMDSettings['boardNum'] = 0

PMDSettings['takeData'] = True
PMDSettings['processData'] = False
PMDSettings['dataFolderName'] = "PMDData"
