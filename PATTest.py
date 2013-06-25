from DefaultSettings.SettingsConsolidator import defaultSettings
from PATController import PATController


PATCtrl = PATController('testApparatus', defaultSettings)
PATCtrl.set_2D_I_2()
PATCtrl.save()


