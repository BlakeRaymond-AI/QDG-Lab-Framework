from DefaultSettings.SettingsConsolidator import defaultSettings, overwriteSettings
from OverwriteSettings.MOTLoadDataCap import updatePackage
from PATController import PATController
from time import sleep

updatedSettings = overwriteSettings(defaultSettings, updatePackage)

PATCtrl = PATController('testApparatus', updatedSettings)
# PATCtrl.start()

print PATCtrl.deviceDict["LabJack"].activeChannels

PATCtrl.set_2D_I_1(3.9)
PATCtrl.set_2D_I_2(5.0)
PATCtrl.set_2D_I_3(-5.0)
PATCtrl.set_2D_I_4(4.4)

PATCtrl.close_all_shutters()

PATCtrl.set_3D_coils_I(1.2)

PATCtrl.set_3DRb_pump_amplitude(0.8)
PATCtrl.set_3DRb_pump_detuning(12)

PATCtrl.set_2DRb_pump_amplitude(0.8)
PATCtrl.set_2DRb_pump_detuning(12)

PATCtrl.set_Rb_repump_amplitude(0.8)
PATCtrl.set_Rb_repump_detuning(5)

PATCtrl.set_Rb_push_amplitude(0.6)
PATCtrl.set_Rb_push_detuning(12)


PATCtrl.wait_s(1)
PATCtrl.open_all_shutters()

PATCtrl.wait_s(300)


PATCtrl.MOT2D_shutter_west_close()
PATCtrl.wait_us(300)
PATCtrl.push_shutter_close()
PATCtrl.wait_us(200)
PATCtrl.MOT2D_shutter_east_close()	  
PATCtrl.wait_ms(2.4)
PATCtrl.pat_2DMOT_off()

PATCtrl.wait_s(200)
PATCtrl.close_all_shutters()


PATCtrl.startDevices()
PATCtrl.end()
PATCtrl.stopDevices()
PATCtrl.saveTrial()

