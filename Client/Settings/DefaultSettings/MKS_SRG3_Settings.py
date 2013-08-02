'''
Default settings for MKG SRG3. Consult device controller for 
more information on gas type, pressure and temperature codes.
'''

MKS_SRG3_Settings = dict()
MKS_SRG3_Settings['port'] = 2	# The COMx port the gauge is connected to.
MKS_SRG3_Settings['duration_s'] = 60
MKS_SRG3_Settings['gType'] = 9	# Gas Type (Default: Air)
MKS_SRG3_Settings['pUnits'] = 3 # Pressure Units (Default: Torr)
MKS_SRG3_Settings['tUnits'] = 1 # Temperature Units (Default: Celsius)			
MKS_SRG3_Settings['takeData'] = False
MKS_SRG3_Settings['processData'] = False
MKS_SRG3_Settings['needsReset'] = True
MKS_SRG3_Settings['resetTime'] = 2
MKS_SRG3_Settings['dataFolderName'] = "MKS_SRG3_Data"
