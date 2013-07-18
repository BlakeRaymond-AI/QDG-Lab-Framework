# '''Default settings for LabJack'''
# 
# labJackSettings = dict()
# labJackSettings['activeChannels'] = [0]	# Array of size 1, 2 or 4 (# Valid Channels: 0-7)				
# labJackSettings['sampleRatePerChannel'] = 100	# Samples per channel per second. Aggregate
# 												# rate should not exceed 1200.
# labJackSettings['scanDuration'] = 10	# Seconds
# labJackSettings['trigger'] = False		# Use trigger.
# labJackSettings['triggerChannel'] = 0	# Channel to use as trigger input.
# 
# labJackSettings['takeData'] = False
# labJackSettings['processData'] = False
# labJackSettings['dataFolderName'] = "LabJackData"
 # ----------------------------------- 
# '''Default settings for Stabil Ion Gauge'''
# 
# SRG3Settings = dict()
# SRG3Settings['port'] = 0	# The COMx port the gauge is connected to.			
# SRG3Settings['duration_s'] = 10 # Duration of data collection.
# SRG3Settings['secondPerSample'] = 1	# Max of 1 second per sample
# 
# SRG3Settings['takeData'] = False
# SRG3Settings['processData'] = False
# SRG3Settings['dataFolderName'] = "MKS_SRG3_Data"
 # ----------------------------------- 
# '''Default PAT Settings'''
# 
# PATSettings = dict()
# # Coil current in Amperes
# PATSettings['2D_I_1'] = 0.5
# PATSettings['2D_I_2'] = 0.5
# PATSettings['2D_I_3'] = 0.5
# PATSettings['2D_I_4'] = 0.5
# PATSettings['3D_coils_I'] = 0.5
# 
# # Pump detuning in MHz
# PATSettings['2DRb_pump_detuning'] = 12 
# PATSettings['3DRb_pump_detuning'] = 12
# PATSettings['Rb_repump_detuning'] = 12 
# PATSettings['Rb_push_detuning'] = 20 
# 
# # Pump amplitude in ...
# PATSettings['2DRb_pump_amplitude'] = 0.8
# PATSettings['3DRb_pump_amplitude'] = 0.8     
# PATSettings['Rb_repump_amplitude'] = 0.8   
# PATSettings['Rb_push_amplitude'] = 0.8 
 # ----------------------------------- 
# '''
# Default settings for PMD. Consult PMD API Specification for voltage range
# and trigger specifications. Device model is PMD-1208FS (USB-1208FS in manual). 
# '''
# 
# PMDSettings = dict()
# PMDSettings['activeChannels'] = [0]	# Channels to sample.
# PMDSettings['gainSettings'] = [0]	# Gain to use on each channel. Should have same
# 									# size as activeChannels array.
# PMDSettings['sampleRatePerChannel'] = 200	# Samples per channel per second. Aggregate
# 											# rate should not exceed 40000.
# PMDSettings['scanDuration'] = 10	# Seconds
# PMDSettings['vRange'] = 'BIP10VOLTS'	# Voltage range being measured.
# PMDSettings['trigType'] = 'TRIG_POS_EDGE'	# Trigger type to use
# PMDSettings['boardNum'] = 0
# 
# PMDSettings['takeData'] = False
# PMDSettings['processData'] = False
# PMDSettings['dataFolderName'] = "PMDData"
 # ----------------------------------- 
# '''Default SaveController Settings'''
# 
# saveSettings = dict()
# saveSettings['basePath'] = 'C:\PAT\PATData'
# saveSettings['timeSuffix'] = ''
 # ----------------------------------- 
# '''Default settings for Stabil Ion Gauge'''
# 
# SISettings = dict()
# SISettings['port'] = 0	# The COMx port the gauge is connected to.			
# SISettings['duration_s'] = 10 # Duration of data collection.
# SISettings['secondPerSample'] = 1	# Max of 1 second per sample
# 
# SISettings['takeData'] = False
# SISettings['processData'] = False
# SISettings['dataFolderName'] = "Stabil_Ion_Data"
 # ----------------------------------- 
