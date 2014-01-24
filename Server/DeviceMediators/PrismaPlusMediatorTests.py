__author__ = 'Blake'

import unittest
import mock
from PrismaPlusMediator import PrismaPlusMediator

TEST_OPC_SERVER = "Matrikon.OPC.Simulation.1"

class PrismaPlusMediatorTests(unittest.TestCase):
    def test_can_construct_real_mediator(self):
        mediator = PrismaPlusMediator({}, server_name=TEST_OPC_SERVER, check_physical_address=False)
        self.assertEqual(1, mediator.controller.opc._opc.ServerState)
        mediator.controller.close()

    def test_init_calls_all_setters_from_dict(self):
        settings_dict = {
            'detector_type': 1,
            'active_channels': 2,
            'number_of_cycles': 3,
            'data_pump_mode': 4,
            'cycle_mode': 5,
            'measure_mode': 6,
            'begin_channel': 7,
            'end_channel': 8,
            'first_masses': 9,
            'dwell_speeds': 10,
            'mass_modes': 11,
            'auto_range_modes': 12,
            'detector_ranges': 13,
            'detector_types': 14
        }

        controller = mock.Mock()
        mediator = PrismaPlusMediator(settings_dict, controller=controller)

        controller.set_detector_type.assert_called_with(1)
        controller.set_active_channels.assert_called_with(2)
        controller.set_number_of_cycles.assert_called_with(3)
        controller.set_data_pump_mode.assert_called_with(4)
        controller.set_cycle_mode.assert_called_with(5)
        controller.set_measure_mode.assert_called_with(6)
        controller.set_begin_channel.assert_called_with(7)
        controller.set_end_channel.assert_called_with(8)
        controller.set_first_masses.assert_called_with(9)
        controller.set_dwell_speeds.assert_called_with(10)
        controller.set_mass_modes.assert_called_with(11)
        controller.set_auto_range_modes.assert_called_with(12)
        controller.set_detector_ranges.assert_called_with(13)
        controller.set_detector_types.assert_called_with(14)

        mediator.controller.close()

    def test_init_only_calls_setters_found_in_dict(self):
        settings_dict = {
            'detector_type': 'foo'
        }

        controller = mock.Mock()
        mediator = PrismaPlusMediator(settings_dict, controller=controller)
        controller.set_detector_type.assert_called_with('foo')

        self.assertFalse(controller.set_active_channels.called)
        self.assertFalse(controller.set_number_of_cycles.called)
        self.assertFalse(controller.set_data_pump_mode.called)
        self.assertFalse(controller.set_cycle_mode.called)
        self.assertFalse(controller.set_measure_mode.called)
        self.assertFalse(controller.set_begin_channel.called)
        self.assertFalse(controller.set_end_channel.called)
        self.assertFalse(controller.set_first_masses.called)
        self.assertFalse(controller.set_dwell_speeds.called)
        self.assertFalse(controller.set_mass_modes.called)
        self.assertFalse(controller.set_auto_range_modes.called)
        self.assertFalse(controller.set_detector_ranges.called)
        self.assertFalse(controller.set_detector_types.called)

        mediator.controller.close()

if __name__ == '__main__':
    unittest.main()

