'''Default settings for Stabil Ion Gauge'''

SISettings = dict()
SISettings['port'] = 0	# The COMx port the gauge is connected to.			
SISettings['duration_s'] = 10 # Duration of data collection.
SISettings['secondPerSample'] = 1	# Max of 1 second per sample

SISettings['takeData'] = False
SISettings['processData'] = False
SISettings['dataFolderName'] = "Stabil_Ion_Data"