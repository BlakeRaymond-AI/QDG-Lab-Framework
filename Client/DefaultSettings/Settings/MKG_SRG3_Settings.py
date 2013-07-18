'''Default settings for Stabil Ion Gauge'''

SRG3Settings = dict()
SRG3Settings['port'] = 0	# The COMx port the gauge is connected to.			
SRG3Settings['duration_s'] = 10 # Duration of data collection.
SRG3Settings['secondPerSample'] = 1	# Max of 1 second per sample

SRG3Settings['takeData'] = False
SRG3Settings['processData'] = False
SRG3Settings['dataFolderName'] = "MKS_SRG3_Data"