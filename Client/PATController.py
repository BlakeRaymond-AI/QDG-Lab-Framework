"""
PAT Experiment Controller
"""
from UTBus1 import AnalogOutput, DigitalOutput, DDS
from UTBus1 import Recipe
from UTBus1.Globals import MHz
from UTBus1_Globals import lock_DDS_params
from UTBus1.Exceptions import * # Make this explicit
from Database import experiment_devices
import math as mth
from time import time, localtime, strftime, sleep

from Settings.Settings import Settings
from Settings.SettingsConsolidator import defaultSettings, overwriteSettings
from PATClient import PATClient

class PATController(Recipe):
	def __init__(self, controllerName, settingsDict, **kw):		   
		Recipe.__init__(self,controllerName,**kw)
		self.controllerName = controllerName
		_D = experiment_devices['PAT']	# PAT Database Settings
		self.__devices = {}
		for (name,addr) in _D['DDS'].items():	# Creates DDS Functions
			self.__devices[addr] = d = DDS(address=addr)
			setattr(self,name,d)

		for (name,addr) in _D['AO'].items():	# Create AO Functions
			self.__devices[addr] = d = AnalogOutput(address=addr)
			setattr(self,name,d)

		for (name,data) in _D['DO'].items():	# Creates DO Functions
			(addr,port) = data
			if not addr in self.__devices:
				self.__devices[addr] = d = DigitalOutput(address=addr)
			setattr(self,name,self.__build_DO_method(name,addr,port))
		
		deviceSettings = settingsDict['deviceSettings']
		generalSettings = settingsDict['generalSettings']
				
		# Remove all devices that aren't taking data from the deviceSettings dict
		for key, val in deviceSettings.items():
			if not val[1]['takeData']:
				del deviceSettings[key]
		self.deviceSettings = deviceSettings
				
		# If there are no devices, there is no need for the PATClient
		if not deviceSettings:
			del generalSettings['PATClient']
				
		# Create settings objects from general settings.
		for (key, deviceData) in generalSettings.items():
			constructor = globals()[deviceData[0]]
			setattr(self, key, constructor(deviceData[1]))	
		
		# Use client to signal server to create devices.		
		if deviceSettings:
			self.PATClient.sendMessage('n' + self.controllerName)
			self.PATClient.sendCommand(settingsDict, 'i')
	
		# Save settings.
		self.settingsDict = settingsDict
		self.generalSettings = generalSettings
		self.deviceSettings = deviceSettings
	
		# Initialise trigger DO
		#self.PMD_trigger(0)
			
		# Keep track of the number of times cameras have been triggered.
		self.numPixeLinkTriggers = 0	
			
	def __build_DO_method(self,name,addr,port):
		'''Constructs Digital Output functions dynamically'''
		def DO_method(v):
			self.__devices[addr].set_bit(port,v)
		DO_method.func_name = name
		return DO_method
	
	def start(self):
		print strftime("Execution began at %H:%M on %x", localtime())
		super(PATController, self).start()
		
	def end(self):
		super(PATController, self).end()	   
		
	def startDevices(self):
		print "Starting data collection devices."
		self.PATClient.sendMediatorCommand("startDevices")
		self.PATClient.awaitConfirmation()

	def stopDevices(self):
		print "Stopping data collection devices."
		self.PATClient.sendMediatorCommand("stopDevices")
		self.PATClient.awaitConfirmation()

	def save(self):
		print "Saving data."
		self.PATClient.sendMediatorCommand("save")
		self.PATClient.awaitConfirmation()
	
	def saveTrial(self, trialName = ''):
		print "Saving trial data."
		args = (trialName,)
		self.PATClient.sendMediatorCommand("saveTrial", args)
		self.PATClient.awaitConfirmation()
		
	def reset(self):
		print "Resetting devices."
		self.numPixeLinkTriggers = 0
		self.PATClient.sendCommand(self.deviceSettings, 'r')
		self.PATClient.awaitConfirmation()
	
	def processData(self):
		print "Processing data."
		self.PATClient.sendMediatorCommand("processExpData")
		self.PATClient.awaitConfirmation()
		
	def closeClient(self):
		self.PATClient.close()
		print "PATClient closed."

	def off(self):
		self.set_2D_I_1(0)
		self.set_2D_I_2(0)
		self.set_2D_I_3(0)
		self.set_2D_I_4(0)
	
	def cable3_ttl(self,value=0):
		self.testcable3(value)

## ========================================================================
# PAT Coil Controls
	def set_2D_I_1(self, A = None): # Set the coil current in amperes
		if A is None: A = self.PATSettings['2D_I_1']
		print "Setting the 2D Coil 1 on to: %.6f" %A
		if mth.fabs(A) > 5.0:
			print "Current setting too high (> 5.0A). Current not set."
		else:
			self.MOT_2Dcoil_1.set_scaled_value(A/0.5) # current = 0.5 A/V

	def set_2D_I_2(self, A = None): # Set the coil current in amperes
		if A is None: A = self.PATSettings['2D_I_2']
		print "Setting the 2D Coil 1 on to: %.6f" %A
		if mth.fabs(A) > 5.0:
			print "Current setting too high (> 5.0A). Current not set."
		else:
			self.MOT_2Dcoil_2.set_scaled_value(A/0.5) # current = 0.5 A/V

	def set_2D_I_3(self, A = None): # Set the coil current in amperes
		if A is None: A = self.PATSettings['2D_I_3']
		print "Setting the 2D Coil 1 on to: %.6f" %A
		if mth.fabs(A) > 5.0:
			print "Current setting too high (> 5.0A). Current not set."
		else:
			self.MOT_2Dcoil_3.set_scaled_value(A/0.5) # current = 0.5 A/V

	def set_2D_I_4(self, A = None): # Set the coil current in amperes
		if A is None: A = self.PATSettings['2D_I_4']
		print "Setting the 2D Coil 1 on to: %.6f" %A
		if mth.fabs(A) > 5.0:
			print "Current setting too high (> 5.0A). Current not set."
		else:
			self.MOT_2Dcoil_4.set_scaled_value(A/0.5) # current = 0.5 A/V

	def set_3D_coils_I(self, A = None): # Set the coil current in amperes
		if A is None: A = self.PATSettings['3D_coils_I']
		print "Setting the PAT Coils on to: %.6f" %A
		if mth.fabs(A) > 5.0:
			print "Current setting too high (> 5.0A). Current not set."
		else:
			self.MOT_3Dcoils.set_scaled_value(A/0.5) # current = 0.5 A/V
			
	def set_Comp_Zcoils_I(self, A = None): # Set the coil current in amperes
		if A is None: A = self.PATSettings['Comp_Zcoils_I']
		print "Setting the PAT Coils on to: %.6f" %A
		if mth.fabs(A) > 5.0:
			print "Current setting too high (> 5.0A). Current not set."
		else:
			self.Comp_Zcoils.set_scaled_value(A/0.5) # current = 0.5 A/V

	def set_2D_coils(self, I1, I2, I3, I4):
		self.set_2D_I_1(I1)
		self.set_2D_I_2(I2)
		self.set_2D_I_3(I3)
		self.set_2D_I_4(I4)
		

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PAT Laser Controls

	def set_2DRb_pump_amplitude(self, amplitude = None):
		if amplitude is None: amplitude = self.PATSettings['2DRb_pump_amplitude']
		if amplitude > 1.0:
			print "AOM amplitude too high (>1.0). Setting amplitude to 1.0"
			amplitude = 1.0
		self.Rb_2Dpump.set_amplitude(amplitude)
		print "2D Rb Pump amplitude set to %.3f" %amplitude
	
	def set_2DRb_pump_detuning(self, detuning = None):	# The usual detuning is -12 MHz
		if detuning is None: detuning = self.PATSettings['2DRb_pump_detuning']
		if mth.fabs(detuning) < 66.0:
			DDS_freq = 90.0 - detuning/2.0
			self.Rb_2Dpump.single_tone(DDS_freq*MHz)
			print 'setting 2D pump AOM to %.6f'%detuning
		else:
			print 'Error: 2D Pump detuning frequency greater than 60 MHz.'

	def set_3DRb_pump_amplitude(self, amplitude = None):
		if amplitude is None: amplitude = self.PATSettings['3DRb_pump_amplitude']
		if amplitude > 1.0:
			print "3D Pump amplitude too high (> 1.0). Setting amplitude to 1.0"
			amplitude = 1.0
		print 'setting 3D pump amplitude to %.3f'%amplitude
		self.Rb_3Dpump.set_amplitude(amplitude)

	def set_3DRb_pump_detuning(self, detuning = None):	# The usual detuning is -12 MHz
		if detuning is None: detuning = self.PATSettings['3DRb_pump_detuning']
		if mth.fabs(detuning) < 66.0:
			DDS_freq = 90.0 - detuning/2.0
			self.Rb_3Dpump.single_tone(DDS_freq*MHz)
			print 'setting 3D pump AOM to %.6f'%detuning
		else:
			print 'Error: 3D Pump detuning frequency greater than 60 MHz.'

	def set_Rb_repump_amplitude(self, amplitude = None):
		if amplitude is None: amplitude = self.PATSettings['Rb_repump_amplitude']
		if amplitude > 1.0:
			print "Repump amplitude too high (> 1.0). Setting repump amplitude to 1.0"
			amplitude = 1.0
		print 'setting repump amplitude to %.3f'%amplitude
		self.Rb_repump.set_amplitude(amplitude)

	def set_Rb_repump_detuning(self, detuning = None):
		if detuning is None: detuning = self.PATSettings['Rb_repump_detuning']
		if mth.fabs(detuning) < 64.0:
			DDS_freq = 90.0 - detuning/2.0
			self.Rb_repump.single_tone(DDS_freq*MHz)
			print 'setting repump AOM to %.6f'%detuning
		else:
			print 'Error: Repump detuning frequency greater than 60 MHz.'

	def set_Rb_push_amplitude(self, amplitude = None):
		if amplitude is None: amplitude = self.PATSettings['Rb_push_amplitude']
		if amplitude > 1.0:
			print "Push amplitude too high (> 1.0). Setting repump amplitude to 1.0"
			amplitude = 1.0
		print 'setting push amplitude to %.3f'%amplitude
		self.Rb_push.set_amplitude(amplitude)

	def set_Rb_push_detuning(self, detuning = None):
		if detuning is None: detuning = self.PATSettings['Rb_push_detuning']
		if mth.fabs(detuning) < 64.0:
			DDS_freq = 90.0 + detuning/2.0
			self.Rb_push.single_tone(DDS_freq*MHz)
			print 'setting push AOM to %.6f'%detuning
		else:
			print 'Error: Push detuning frequency greater than 60 MHz.'

	def set_optical_pump_amplitude(self, amplitude = None):
		if amplitude is None: amplitude = self.PATSettings['optical_pump_amplitude']
		if amplitude > 1.0:
			print "Push amplitude too high (> 1.0). Setting repump amplitude to 1.0"
			amplitude = 1.0
		print 'setting push amplitude to %.3f'%amplitude
		self.optical_pump.set_amplitude(amplitude)

	def set_optical_pump_detuning(self, detuning = None):
		if detuning is None: detuning = self.PATSettings['optical_pump_detuning']
		if mth.fabs(detuning) < 64.0:
			DDS_freq = 90.0 + detuning/2.0
			self.optical_pump.single_tone(DDS_freq*MHz)
			print 'setting push AOM to %.6f'%detuning
		else:
			print 'Error: Push detuning frequency greater than 60 MHz.'

	def pat_lasers_on(self):
	   # self.set_2DRb_pump_amplitude(0.5)
		self.set_3DRb_pump_amplitude(0.8)
		self.set_Rb_repump_amplitude(0.8)
	   # self.set_Rb_push_amplitude(0.6)
		print 'lasers on'

	def pat_3DMOT_lasers_on(self):
		self.set_3DRb_pump_amplitude(0.8)
		self.set_Rb_repump_amplitude(0.8)
		print 'lasers on'

	def pat_3DMOT_lasers_off(self):
		self.set_3DRb_pump_amplitude(0.0)
		self.set_Rb_repump_amplitude(0.0)
		print 'lasers on'

	def pat_lasers_off(self):
		self.set_2DRb_pump_amplitude(0.0)
		self.set_3DRb_pump_amplitude(0.0)
		self.set_Rb_repump_amplitude(0.0)
		self.set_Rb_push_amplitude(0.0)

	def pat_2DMOT_off(self):
		self.set_2DRb_pump_amplitude(0.0)
		self.set_Rb_push_amplitude(0.0)
		self.set_2D_I_1(0.0)
		self.set_2D_I_2(0.0)
		self.set_2D_I_3(0.0)
		self.set_2D_I_4(0.0)

	def pat_2DMOT_lasers_off(self):
		self.set_2DRb_pump_amplitude(0.0)
		self.set_Rb_push_amplitude(0.0)

	def pat_2DMOT_lasers_on(self):
		self.set_2DRb_pump_amplitude(0.5)
		self.set_Rb_push_amplitude(0.6)

	def pat_2DMOT_Bfield_off(self):
		self.set_2D_I_1(0.0)
		self.set_2D_I_2(0.0)
		self.set_2D_I_3(0.0)
		self.set_2D_I_4(0.0)

	def pat_2DMOT_on(self):
		self.set_2DRb_pump_amplitude(0.8)
		self.set_Rb_push_amplitude(0.6)
		self.set_2D_I_1(3.9)
		self.set_2D_I_2(5.0)
		self.set_2D_I_3(-5.0)
		self.set_2D_I_4(4.4)

	def pat_2DMOT_Bfield_on(self):
		self.set_2D_I_1(3.9)
		self.set_2D_I_2(5.0)
		self.set_2D_I_3(-5.0)
		self.set_2D_I_4(4.4)
		
# #------------------------------------------------------------------------
# # Shutter Controls trigger controls
	def trig_scope_on(self):
		print 'Triggering scope'
		self.pat_scope_trig(1)

	def trig_scope_off(self):
		self.pat_scope_trig(0)

# #------------------------------------------------------------------------
# # Trigger Controls
# # When adding triggers, update the open and close all shutter methods.
	 
	def close_all_shutters(self):
		self.MOT2D_shutter_west_close()
		self.MOT2D_shutter_east_close()	  
		self.MOT3D_pump_shutter_close()
		self.MOT3D_repump_shutter_close()	
		self.push_shutter_close()
		
	def open_all_shutters(self):
		self.MOT2D_shutter_west_open()
		self.MOT2D_shutter_east_open()	  
		self.MOT3D_pump_shutter_open()
		self.MOT3D_repump_shutter_open()	
		self.push_shutter_open()

	def MOT2D_shutter_west_open(self):
		self.MOT2D_shutter_west(1)
	
	def MOT2D_shutter_west_close(self):
		self.MOT2D_shutter_west(0)
	
	def MOT2D_shutter_east_open(self):
		self.MOT2D_shutter_east(1)
		
	def MOT2D_shutter_east_close(self):
		self.MOT2D_shutter_east(0)
		
	def MOT3D_pump_shutter_open(self):
		self.MOT3D_pump_shutter(1)
		  
	def MOT3D_pump_shutter_close(self):
		self.MOT3D_pump_shutter(0)
		  
	def MOT3D_repump_shutter_open(self):
		self.MOT3D_repump_shutter(1)
	
	def MOT3D_repump_shutter_close(self):
		self.MOT3D_repump_shutter(0)
		
	def push_shutter_open(self):
		self.push_shutter(1)
		
	def push_shutter_close(self):
		self.push_shutter(0)

# #------------------------------------------------------------------------
# # PixeLink Controls

	def triggerPixeLink(self):
		self.numPixeLinkTriggers += 1
		self.pixelink_trigger(1)
		self.wait_us(50)
		self.pixelink_trigger(0)
		
	def setPixeLinkImageCount(self):
		self.pixelink_trigger(0)
		devName = 'PixeLink'
		fName = 'setNumberOfImages'
		args = (self.numPixeLinkTriggers,)
		self.PATClient.sendSpecificDeviceCommand(devName, fName, args)
		sleep(4.0)

# #------------------------------------------------------------------------
# # Optimizer Controls

	def getParticle(self):
		devName = 'Optimizer'
		fName = 'getParticle'
		part = self.PATClient.sendSpecificDeviceCommand(devName, fName, 
														waitForResponse = True, 
														pickledResponse = True)
		return part
		
	def evaluateFitness(self):
		devName = 'Optimizer'
		fName = 'evaluateFitness'
		self.PATClient.sendCommand({}, 'e')
		
# #------------------------------------------------------------------------
# # PMD Trigger

	def triggerPMD(self):
		self.PMD_trigger(1)
		self.wait_us(5)
		self.PMD_trigger
		
		
	
	
  
	
	
