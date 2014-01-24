'key:PrismaPlus'
'''Default settings for the PrismaPlus RGA'''
PrismaPlusSettings = dict()
PrismaPlusSettings['data_pump_mode'] = 0 # DATA-LOOSE
PrismaPlusSettings['begin_channel']= 0
PrismaPlusSettings['end_channel'] = 6
PrismaPlusSettings['first_masses'] = [14,16,18,28,32,40,44]
PrismaPlusSettings['dwell_speeds'] = [5]*7
PrismaPlusSettings['mass_modes'] = [0]*7
PrismaPlusSettings['auto_range_modes'] = [0]*7
PrismaPlusSettings['detector_ranges'] = [0]*7
PrismaPlusSettings['detector_types'] = [0]*7
PrismaPlusSettings['cycle_mode'] = 1 # MULTI
PrismaPlusSettings['measure_mode'] = 0 # CYCLE
PrismaPlusSettings['number_of_cycles'] = 0 # Repeat endlessly
