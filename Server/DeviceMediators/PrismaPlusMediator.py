from DeviceMediatorInterface import DeviceMediatorInterface
from DeviceControllers.PrismaPlusController import PrismaPlusController


class PrismaPlusMediator(DeviceMediatorInterface):
    '''
	Interface for device controllers. All devices used in the PAT apparatus
	should implement its methods, and settings dictionaries for mediators should
	include the field within __init__
	'''

    def __init__(self, dictionary, *args, **kwargs):
        DeviceMediatorInterface.__init__(self)
        self.settings = dictionary
        if 'controller' in kwargs:
            self.controller = kwargs.pop('controller')
        else:
            self.controller = PrismaPlusController(*args, **kwargs)

        self.setting_function_dict = {
            'detector_type': self.controller.set_detector_type,
            'active_channels': self.controller.set_active_channels,
            'number_of_cycles': self.controller.set_number_of_cycles,
            'data_pump_mode': self.controller.set_data_pump_mode,
            'cycle_mode': self.controller.set_cycle_mode,
            'measure_mode': self.controller.set_measure_mode,
            'begin_channel': self.controller.set_begin_channel,
            'end_channel': self.controller.set_end_channel,
            'first_masses': self.controller.set_first_masses,
            'dwell_speeds': self.controller.set_dwell_speeds,
            'mass_modes': self.controller.set_mass_modes,
            'auto_range_modes': self.controller.set_auto_range_modes,
            'detector_ranges': self.controller.set_detector_ranges,
            'detector_types': self.controller.set_detector_types
        }

        for key, value in self.settings.items():
            if key in self.setting_function_dict:
                self.setting_function_dict[key](value)



    def start(self):
        '''Initialise the device for an experimental run.'''
        self.controller.start()

    def stop(self):
        '''Stop a device after an experimental run.'''
        self.controller.stop()

    def save(self, pth):
        '''Save the data associated with the device to the pth given.'''
        self.controller.saveData(pth)

    def processExpData(self, pth):
        '''Process the data associated with the device to the pth given.'''
        raise NotImplementedError()

    def saveState(self, pth):
        '''Saves the state of the device mediator into an external file.'''
        raise NotImplementedError()

    def restoreState(self, pth):
        '''Restores the state of the device mediator from an external file.'''
        raise NotImplementedError()

    def filament_on(self):
        self.controller.filament_on()

    def filament_off(self):
        self.controller.filament_off()

    def simulation_on(self):
        self.controller.simulation_on()

    def simulation_off(self):
        self.controller.simulation_off()

    def reset_buffer(self):
        self.controller.reset_buffer()

    def read_status(self):
        return self.controller.read_status()
