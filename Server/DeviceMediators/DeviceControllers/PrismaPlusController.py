import threading
import csv
import struct
from OpenOPC import OpenOPC
import io

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

class RingBufferPacket(object):
    def __init__(self, buffered_reader):
        self.read_header(buffered_reader)
        self.read_body(buffered_reader)

    def read_header(self, buffered_reader):
        self.channel_number = buffered_reader.read(1)

        if self.channel_number is None:
            raise IOError

        self.data_type = buffered_reader.read(1)
        self.status = buffered_reader.read(1)

    def read_body(self, buffered_reader):
        if self.status == DeviceStatus.CHANNEL_START:
            numberOfData = buffered_reader.read(1) #will be 10
            self.timeStamp = struct.unpack('q', buffered_reader.read(8))
            # timeStamp is in Windows FILETIME format,
            # i.e. number of 100 ns intervals since 1 January 1601.
            self.maxNumberOfDataTuples = struct.unpack('h', buffered_reader.read(2))

        elif self.status == DeviceStatus.CHANNEL_INFORMATION:
            numberOfData = buffered_reader.read(1) #will be 6
            self.firstMass = struct.unpack('h', buffered_reader.read(2))
            self.lastMass = struct.unpack('h', buffered_reader.read(2))
            self.dwellSpeed = buffered_reader.read(1)
            unitAndResolution = buffered_reader.read(1)
            # extract bits 2 and 3
            self.unit = ["Ampere", "cps", "Volt", "mbar"][(unitAndResolution & (0x3 << 4)) >> 4]
            # extract bits 4 and 5
            self.resolution = [1 / 64., 1 / 32., 1 / 16., 1 / 8.][(unitAndResolution & (0x3 << 2)) >> 4]

        elif self.status == DeviceStatus.CONTINUOUS_MEASURING_DATA or \
                        self.status == DeviceStatus.CHANNEL_END:
            numberOfTuples = buffered_reader.read(1)
            self.masses = []
            self.intensities = []
            self.status1 = []
            self.status2 = []
            for _ in xrange(numberOfTuples):
                self.intensities.append(struct.unpack('f', buffered_reader.read(4))[0])
                self.masses.append(buffered_reader.read(2))
                self.status1.append(buffered_reader.read(1))
                self.status2.append(buffered_reader.read(1))

class PrismaPlusController(object):
    """
	Pfeiffer Vacuum PrismaPlus (TM) QMG 220 mass spectrometer control class
	TODO:
	1) implement this thing
	2) import this in the PATServer file
	3) implement the settings file
	"""

    def __init__(self,
                 opc_class_name="Graybox.OPC.DAWrapper",
                 server_name="QMG220-DA",
                 validate_physical_address=True):
        # set up the OPC client. The PrismaPlus server is a DA server
        # so we use the Graybox OPC DA Wrapper to connect
        # The OPC client is running in DCOM mode (Windows only).
        # Refer to OpenOPC documentation for UNIX-like systems.
        self.opc = OpenOPC.client(opc_class=opc_class_name)
        self.opc.connect(server_name)
        # check if the connection was successful and to the correct device
        # (and not to, say, one of the simulated devices running on the PC)
        if validate_physical_address:
            try:
                physical_address = self.opc.read('General.LanConfiguration.PhysicalAddress')
                assert physical_address[0] == PRISMA_PHYSICAL_ADDR
            except AssertionError:
                raise AssertionError("Physical address of the residual gas analyser\
                    is different than expected.")

    def write(self, msg):
        self.opc.write(msg)

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
        self.opc.write([
            ('Hardware.Modules.Analyser.SI220.SimulationMode', 0), #simulation off
            ('General.DataPump.Mode', DataPumpMode.HOLD), #when ring buffer full, hold data until enough free space
            #more settings will go here
            ('Analyser.Filament.Command', 1), #filament on
            ('General.Cycle.CycleMode', CycleMode.MULTI),
            ('General.Cycle.MeasureMode', MeasureMode.CYCLE),
            ('General.Cycle.NumberOfCycles', 0), #repeated endlessly
            ('General.Cycle.BeginChannel', 0),
            ('General.Cycle.EndChannel', 6),
            ('General.Cycle.Command', 1) #start measurement
        ])

    def terminate_data_collection(self):
        self.opc.write([
            ('General.Cycle.Command', 2), #stop measurement
            ('Analyser.Filament.Command', 2) #filament off
        ])

    def collectData(self):
        """
        Initiates data collection.
        Data collection is documented in 7.3 of PrismaPlusComm.pdf
		Warning: I have not finished writing this function yet so it may not 
		be implemented correctly.
		"""
        self.packets = []
        self.massRange = self.opc.read('Hardware.MassRange')[0]

        while True:
            packet_bytes = bytearray(self.opc.read('General.DataPump.Data'))
            if not packet_bytes:
                break
            bytes_io = io.BytesIO(packet_bytes)
            while True:
                try:
                    self.packets.append(RingBufferPacket(bytes_io))
                except IOError:
                    break

    #We will probably need the timestamps at some point.
    def extract_data_from_packets(self):
        if not self.packets:
            return
        masses = []
        intensities = []
        for packet in self.packets:
            if not (packet.status == DeviceStatus.CONTINUOUS_MEASURING_DATA or
                            packet.status == DeviceStatus.CHANNEL_END):
                pass
            masses.append(packet.masses)
            intensities.append(packet.intensities)

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


if __name__ == '__main__':
    PPC = PrismaPlusController(server_name="Matrikon.OPC.Simulation.1", validate_physical_address=False)
    PPC.collectData()
    PPC.saveData()
    PPC.plotData()
    PPC.close()
