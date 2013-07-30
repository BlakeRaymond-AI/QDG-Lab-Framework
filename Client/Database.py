'''
This is a database of devices. The name of each device is unique in 
the QDG Lab.

experiment_devices maps experiment name to a dict that contains
all the devices used by that experiment. The devices fall in one 
of the following categories: 
  - DDS : address
  - DO (DigitalOutput) : (address,port)
  - AO (AnalogOutput) : address

The specialized Recipe has an instance with the same name for 
all the DDS and AO devices. The DO devices become functions which
accept a single argument treated as a bool (0 or 1). 

'''
__all__ = ['experiment_devices']

__MAT_devices = {
    'DDS' : {
        'Rb_pump' : 136, #original is 136
        'Rb_repump' : 124,#original is 124
        'MAT_antenna': 132,
        'Rb_zeeman_pump':112,
    },
    
    'DO' : {
        'testcable3' : (254,8),
        'mat_coil_enable' : (254,15),
        'mat_scope_trig' : (254,13),
        'mat_sorensen_trig' : (254,12),
        'mat_main_shutter' : (254,7),
        'mat_abs_shutter' : (254,6),
        'mat_pixelink_trig': (254, 5),
        'mat_87Rb_cooling_shutter': (254, 0),
        'mat_87Rb_repump_shutter' : (254, 1),
        'mat_85Rb_repump_shutter' : (254, 2),
        'mat_85Rb_cooling_shutter' : (254, 3),
    },
    
    'AO' : {
        'test_AO' : 192,  # used for direct molecule frequency control of TiS
        'mat_coil' : 199,
        'FLI_trig' : 198,
        'Zeeman_coil':197,
        'Comp_coil_y':195,
        'Comp_coil_z':196,
        'Temp_MAT_Coils': 207,
        'RF_antenna_voltage_freq': 200,
        'RF_antenna_voltage_imp_match': 201,
    },
}
__MOL_devices = {
    'DDS' : {
        'Li_pump' : 152,
        'Li_repump' : 156,
        'Rb_pump' : 20,
    },
    
    'DO' : {
        'Rb_pump_shutter' : (251,3),
        'Li_pump_shutter' : (251,2),
        'Li_repump_shutter' : (251,1),
        'mot_shutter' : (251,15),
        'mot_coil_polarity' : (252,9,),
        'mot_coil_enable' : (252,9),
        'tweezer_enable' : (251,0),
        'camera_trigger' : (252,15),
        'Rb_repump_enable' : (252,10),
        'apogee_trigger' : (251,7),
        'Li_pump_abs_shutter1' : (251,4),
        'Li_pump_abs_shutter2' : (251,5),
        'Utility_trigger' : (251,6),
    },
    
    'AO' : {
        'mot_coil' : 231,
        'comp_coil_x' : 230,
        'comp_coil_y' : 229,
        'comp_coil_z' : 228,
        'EO_pump' : 224,
        'EO_repump' : 225,
    },
}

__PAT_devices = {
    'DDS' : {
        'Rb_2Dpump' : 140,
        'Rb_3Dpump' : 24,
        'Rb_repump' : 116,
        'Rb_push': 92,
		'optical_pump' : 188,
    },
    
    'DO' : {
        'pat_scope_trig' : (253,8),
		'MOT2D_shutter_west': (253,2),
        'MOT2D_shutter_east':(253,1),
        'MOT3D_pump_shutter':(253,3),
        'MOT3D_repump_shutter':(253,4),
        'push_shutter':(253,5),
		'pixelink_trigger' : (253, 15),
		'PMD_trigger' : (253, 16)
    },
    
    'AO' : {
        'MOT_2Dcoil_1' : 200, 
        'MOT_2Dcoil_2' : 201,
        'MOT_2Dcoil_3' : 202,
        'MOT_2Dcoil_4' : 203,
        'MOT_3Dcoils' : 196,
		'Comp_Zcoils': 207,
    },
}

experiment_devices = {
    'MAT' : __MAT_devices,
    'MOL' : __MOL_devices,
    'PAT' : __PAT_devices,
}

