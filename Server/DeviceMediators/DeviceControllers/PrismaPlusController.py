import threading
import csv
from OpenOPC import OpenOPC
import io
import time
from PrismaPlusBufferReader import PrismaPlusBufferReader
from Queue import Queue

import matplotlib.pyplot as plt


PRISMA_ADDR = '10.1.213.41'

# If you physically replace the device, please update this line.
PRISMA_PHYSICAL_ADDR = '00-50-C2-C1-0A-26'

class DeviceStatus:
    CONTINUOUS_MEASURING_DATA = 0
    CHANNEL_START = 1
    CHANNEL_END = 2
    CHANNEL_ABORTED = 3
    CYCLE_END = 4
    CHANNEL_INFORMATION = 5
    MEASUREMENT_END = 6

class DataPumpMode:
    DATA_LOOSE = 0,
    HOLD = 1,
    HOLD_EMPTY = 2

class CycleMode:
    MONO = 0,
    MULTI = 1

class MeasureMode:
    CYCLE = 0,
    ADJ_FINE = 1,
    ADJ_COARSE = 2,
    RF_TUNE = 3,
    OFFSET = 4

class IonDetectorType:
    FARADAY = 0,
    SEM = 1


class PrismaPlusController:
    """
    Pfeiffer Vacuum PrismaPlus (TM) QMG 220 mass spectrometer control class
    TODO:
    2) import this in the PATServer file
    3) implement the settings file
    """

    def __init__(self, server_name="QMG220-DA", check_physical_address=True):
        # set up the OPC client. The PrismaPlus server is a DA server
        # so we use the Graybox OPC DA Wrapper to connect
        # The OPC client is running in DCOM mode (Windows only).
        # Refer to OpenOPC documentation for UNIX-like systems.
        self.server_name = server_name
        
        self.opc = OpenOPC.client(opc_class="Graybox.OPC.DAWrapper")
        self.opc.connect(self.server_name)
        # check if the connection was successful and to the correct device
        # (and not to, say, one of the simulated devices running on the PC)
        physical_address = self.opc.read('General.LanConfiguration.PhysicalAddress')
        if not physical_address[0] == PRISMA_PHYSICAL_ADDR:
            raise AssertionError("Physical address of the residual gas analyser\
                is different than expected.")

    def write(self, msg):
        self.opc.write(msg)

    def read(self, msg):
        return self.opc.read(msg)

    def start(self):
        '''Starts the data collection thread.'''
        self.dataCollectionThread = threading.Thread(target = self.collectData)
        self.dataCollectionThread.start()

    def stop(self):
        """
		Waits until data collection is complete before proceeding.
		Returns boolean value indicating whether data collection failed.
		"""

        print "Waiting for PrismaPlus to finish collecting data"

        try:
            self.dataCollectionThread.join()
            return True
        except:
            return False

    def set_scan_duration(self, scanDuration):
        self.scanDuration = scanDuration

    def collectData(self):
        """
        Initiates data collection.
        Data collection is documented in 7.3 of PrismaPlusComm.pdf
		"""
        data_opc = OpenOPC.client(opc_class="Graybox.OPC.DAWrapper")
        data_opc.connect(self.server_name)
        
        self.bufferReader = PrismaPlusBufferReader()

        data_opc.write(('General.Cycle.Command', 1)) # Start collecting data
        startTime = time.time()

        while time.time() - startTime < self.scanDuration:
            try:
                if not data_opc.read("General.Cycle.Status")[0] == 5: # Device is not collecting data -- abort.
                    break
                packet_bytes = data_opc.read('General.DataPump.Data')[0]
                if not packet_bytes:
                    raise RuntimeError("No bytes returned from General.DataPump.Data")
                buf = io.BytesIO(bytes(packet_bytes))
                self.bufferReader.readAndAppend(buf)
            except Exception as e:
                print e
                break

        data_opc.write(('General.Cycle.Command', 2)) # Stop collecting data
        data_opc.close()

    def close(self):
        self.opc.close()

    def saveData(self, path="PrismaPlusData.csv"):
        timestamps = self.bufferReader.timestamps
        intensities = self.bufferReader.intensities
        with open(path, 'w') as f:
            csvwriter = csv.writer(f, delimiter=',')
            csvwriter.writerow("Timestamp (Windows FILETIME), Mass (AMU), Intensity (A)")
            for time, valuePair in zip(timestamps, intensities):
                csvwriter.writerow([time, valuePair[0], valuePair[1]])

    def plotData(self, path):
        data = self.bufferReader.getData()
        masses = sorted(data.keys())
        for mass in masses:
            x = [pair[0] for pair in data[mass]]
            y = [pair[1] for pair in data[mass]]
            plt.plot(x, y)
            plt.hold(True)
        plt.legend(masses)
        plt.xlabel('Windows Filetime (10 ns)')
        plt.ylabel('Intensity (A)')
        plt.savefig(path)

    def set_detector_type(self, detector_type):
        self.write(('Analyser.Detector.Type', detector_type))

    def set_active_channels(self, active_channels):
        all_channels = [0]*128
        for channel in active_channels:
            all_channels[channel] = 1
        self.write(('Channels.Parameters.General.State', all_channels))

    def set_number_of_cycles(self, cycles): #0 for endless loop
        self.write(('General.Cycle.NumberOfCycles', cycles))

    def simulation_on(self):
        self.write(('Hardware.Modules.Analyser.SI220.SimulationMode', 1))

    def simulation_off(self):
        self.write(('Hardware.Modules.Analyser.SI220.SimulationMode', 0))

    def set_data_pump_mode(self, mode):
        self.write(('General.DataPump.Mode', mode))

    def set_cycle_mode(self, mode):
        self.write(('General.Cycle.CycleMode', mode))

    def set_measure_mode(self, mode):
        self.write(('General.Cycle.MeasureMode', mode))

    def set_begin_channel(self, channel):
        self.write(('General.Cycle.BeginChannel', channel))

    def set_end_channel(self, channel):
        self.write(('General.Cycle.EndChannel', channel))

    def set_first_masses(self, first_masses):
        self.write(('Channels.Parameters.Mass.FirstMass', first_masses))

    def set_dwell_speeds(self, dwell_speeds):
        self.write(('Channels.Parameters.Mass.DwellSpeed', dwell_speeds))

    def set_mass_modes(self, mass_modes):
        self.write(('Channels.Parameters.Mass.MassMode', mass_modes))

    def set_auto_range_modes(self, range_modes):
        self.write(('Channels.Parameters.Amplifier.AutoRangeMode', range_modes))

    def set_detector_ranges(self, detector_ranges):
        self.write(('Channels.Parameters.Amplifier.DetectorRange', detector_ranges))

    def set_detector_types(self, detector_types):
        self.write(('Channels.Parameters.Detector.DetectorType', detector_types))

    def reset_buffer(self):
        self.write(('General.DataPump.Command', 1))

    def read_status(self):
        return self.opc.read('General.Cycle.Status')


if __name__ == '__main__':
    PPC = PrismaPlusController(server_name="QMG220-DA", check_physical_address=True)

    PPC.set_data_pump_mode(DataPumpMode.HOLD)
    PPC.set_first_masses([14, 16, 18, 28, 32, 40, 44])
    PPC.set_dwell_speeds([5]*7)
    PPC.set_mass_modes([0]*7)
    PPC.set_auto_range_modes([0]*7)
    PPC.set_detector_ranges([0]*7)
    PPC.set_detector_type([0]*7)

    PPC.set_cycle_mode(CycleMode.MULTI)
    PPC.set_measure_mode(MeasureMode.CYCLE)
    PPC.set_number_of_cycles(0)

    PPC.set_begin_channel(0)
    PPC.set_end_channel(6)

    PPC.start()
    time.sleep(30)
    PPC.stop()
    PPC.saveData("PrismaPlusData.csv")
    PPC.plotData("PrismaPlusPlot.png")

