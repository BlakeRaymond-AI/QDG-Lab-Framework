import threading
import csv
import struct
from OpenOPC import OpenOPC
import io
import time

PRISMA_ADDR = '10.1.213.41'

# If you physically replace the device, please update this line.
PRISMA_PHYSICAL_ADDR = '00-50-C2-C1-0A-26'

class DeviceStatus(object):
    CONTINUOUS_MEASURING_DATA = 0
    CHANNEL_START = 1
    CHANNEL_END = 2
    CHANNEL_ABORTED = 3
    CYCLE_END = 4
    CHANNEL_INFORMATION = 5
    MEASUREMENT_END = 6

class DataPumpMode(object):
    DATA_LOOSE = 0,
    HOLD = 1,
    HOLD_EMPTY = 2

class CycleMode(object):
    MONO = 0,
    MULTI = 1

class MeasureMode(object):
    CYCLE = 0,
    ADJ_FINE = 1,
    ADJ_COARSE = 2,
    RF_TUNE = 3,
    OFFSET = 4

class IonDetectorType(object):
    FARADAY = 0,
    SEM = 1

class RingBufferPacket(object):
    def __init__(self, buffered_reader):
        self.read_header(buffered_reader)
        self.read_body(buffered_reader)

    def read_header(self, buffered_reader):
        channel_number = buffered_reader.read(1)

        if not channel_number:
            raise IOError

        self.channel_number = ord(channel_number)

        self.data_type = ord(buffered_reader.read(1))
        self.status = ord(buffered_reader.read(1))

    def read_body(self, buffered_reader):
        if self.status == DeviceStatus.CHANNEL_START:
            numberOfData = ord(buffered_reader.read(1)) #will be 10
            self.timeStamp = struct.unpack('q', buffered_reader.read(8))
            # timeStamp is in Windows FILETIME format,
            # i.e. number of 100 ns intervals since 1 January 1601.
            self.maxNumberOfDataTuples = struct.unpack('h', buffered_reader.read(2))

        elif self.status == DeviceStatus.CHANNEL_INFORMATION:
            numberOfData = ord(buffered_reader.read(1)) #will be 6
            self.firstMass = struct.unpack('h', buffered_reader.read(2))
            self.lastMass = struct.unpack('h', buffered_reader.read(2))
            self.dwellSpeed = ord(buffered_reader.read(1))
            unitAndResolution = ord(buffered_reader.read(1))
            # extract bits 2 and 3
            self.unit = ["Ampere", "cps", "Volt", "mbar"][(unitAndResolution & (0x3 << 4)) >> 4]
            # extract bits 4 and 5
            self.resolution = [1 / 64., 1 / 32., 1 / 16., 1 / 8.][(unitAndResolution & (0x3 << 2)) >> 4]

        elif self.status == DeviceStatus.CONTINUOUS_MEASURING_DATA or \
                        self.status == DeviceStatus.CHANNEL_END:
            numberOfTuples = ord(buffered_reader.read(1))
            self.masses = []
            self.intensities = []
            self.status1 = []
            self.status2 = []
            for _ in xrange(numberOfTuples):
                self.intensities.append(struct.unpack('f', buffered_reader.read(4))[0])
                self.masses.append(struct.unpack('h', buffered_reader.read(2))[0])
                self.status1.append(ord(buffered_reader.read(1)))
                self.status2.append(ord(buffered_reader.read(1)))

class PrismaPlusController(object):
    """
	Pfeiffer Vacuum PrismaPlus (TM) QMG 220 mass spectrometer control class
	TODO:
	1) implement this thing
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
        if check_physical_address:
            try:
                physical_address = self.opc.read('General.LanConfiguration.PhysicalAddress')
                assert physical_address[0] == PRISMA_PHYSICAL_ADDR
            except AssertionError:
                raise AssertionError("Physical address of the residual gas analyser\
                    is different than expected.")

    def write(self, msg):
        self.opc.write(msg)

    def read(self, msg):
        return self.opc.read(msg)

    def start(self):
        '''Starts the data collection thread.'''
        self.initiate_data_collection()
        self.data_collection_thread = threading.Thread(target = self.collectData)
        self.data_collection_thread.start()

    def stop(self):
        """
		Waits until data collection is complete before proceeding.
		Returns boolean value indicating whether data collection failed.
		"""
        self.terminate_data_collection()

        exception = False
        try:
            self.data_collection_thread.join()
        except:
            exception = True

        self.close()
        return exception

    def initiate_data_collection(self):
        self.write(('General.Cycle.Command', 1))

    def terminate_data_collection(self):
        self.write(('General.Cycle.Command', 2))

    def collectData(self):
        """
        Initiates data collection.
        Data collection is documented in 7.3 of PrismaPlusComm.pdf
		Warning: I have not finished writing this function yet so it may not 
		be implemented correctly.
		"""
        self.data_opc = OpenOPC.client(opc_class="Graybox.OPC.DAWrapper")
        self.data_opc.connect(self.server_name)
        
        self.packets = []
        self.massRange = self.data_opc.read('Hardware.MassRange')[0]

        while True:
            packet_bytes = self.data_opc.read('General.DataPump.Data')[0]
            if not packet_bytes:
                print 'No data returned'
                break
            packet_bytes = bytearray(packet_bytes)
            bytes_io = io.BytesIO(packet_bytes)
            while True:
                try:
                    self.packets.append(RingBufferPacket(bytes_io))
                except IOError:
                    break

    def extract_data_from_packets(self):
        if not self.packets:
            return
        masses = []
        intensities = []
        for packet in self.packets:
            if not (packet.status == DeviceStatus.CONTINUOUS_MEASURING_DATA or
                            packet.status == DeviceStatus.CHANNEL_END):
                continue
            masses.append(*packet.masses)
            intensities.append(*packet.intensities)

        return zip(masses, intensities)

    def saveData(self, fname="PrismaPlus_RGA_Data.csv"):
        '''Save the data collected by the gauge.'''
        data = self.extract_data_from_packets()
        with open(fname, 'wb') as csvFile:
            file_writer = csv.writer(csvFile, delimiter=',')
            file_writer.writerow(["Mass (amu)", "Reading"])

            for mass, intensity in data:
                file_writer.writerow([mass, intensity])

    def plotData(self, fname="PrismaPlus_RGA_Plot.png"):
        '''Plots the data collected by the gauge.'''
        import matplotlib.pyplot as plt

        plt.clf()
        data = self.extract_data_from_packets()
        unzipped = zip(*data)
        masses = list(unzipped[0])
        intensities = list(unzipped[1])
        plt.plot(masses, intensities, ls='None', marker='.')
        plt.xlabel('Mass (amu)')
        plt.ylabel('Reading')
        plt.savefig(fname)
        plt.clf()

    def close(self):
        self.opc.close()
        if hasattr(self, 'data_opc'):
            self.data_opc.close()

    def filament_on(self):
        self.write(('Analyser.Filament.Command', 1))

    def filament_off(self):
        self.write(('Analyser.Filament.Command', 0))

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
    PPC = PrismaPlusController(server_name="QMG220-DA", check_physical_address=False)
    PPC.simulation_on()
    PPC.set_data_pump_mode(DataPumpMode.DATA_LOOSE)
    PPC.set_begin_channel(0)
    PPC.set_end_channel(6)
    PPC.set_first_masses([14,16,18,28,32,40,44])
    PPC.set_dwell_speeds([5]*7)
    PPC.set_mass_modes([0]*7)
    PPC.set_auto_range_modes([0]*7)
    PPC.set_detector_ranges([0]*7)
    PPC.set_detector_types([0]*7)
    PPC.set_cycle_mode(CycleMode.MULTI)
    PPC.set_measure_mode(MeasureMode.CYCLE)
    PPC.set_number_of_cycles(0)
    PPC.reset_buffer()
    PPC.start()
    assert PPC.read_status()[0] == 5
    PPC.stop()
    PPC.saveData()
    PPC.plotData()
    PPC.close()
    
