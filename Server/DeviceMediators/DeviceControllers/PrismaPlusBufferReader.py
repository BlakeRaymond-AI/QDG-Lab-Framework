import struct
import array

__author__ = 'Blake'

def readInt8(buffer):
    return ord(buffer.read(1))

def readInt16(buffer):
    return struct.unpack('h', buffer.read(2))[0]

def readInt32(buffer):
    return struct.unpack('i', buffer.read(4))[0]

def readInt64(buffer):
    return struct.unpack('q', buffer.read(8))[0]

def readFloat(buffer):
    return struct.unpack('f', buffer.read(4))[0]

class ChannelStartPacket:
    def __init__(self, buffer, channelNumber):
        self.channelNumber = channelNumber
        self.timestamp = readInt64(buffer)
        self.maxNumberOfDataTuples = readInt16(buffer)

class ChannelInformationPacket:
    def __init__(self, buffer, channelNumber):
        self.channelNumber = channelNumber
        self.firstMass = readInt16(buffer)
        self.lastMass = readInt16(buffer)
        self.dwellSpeed = readInt8(buffer)
        measurementUnitAndResolution = buffer.read(1)
        self.unit = measurementUnitAndResolution & 0b00110000
        self.massResolution = measurementUnitAndResolution & 0b00001100

class ChannelAbortedPacket:
    def __init__(self, channelNumber):
        self.channelNumber = channelNumber

class ChannelEndPacket:
    def __init__(self, buffer, numberOfData, channelNumber):
        self.channelNumber = channelNumber
        self.numberOfData = numberOfData
        self.intensity = array.array('f')
        self.mass = array.array('i')
        for _ in range(numberOfData):
            self.intensity.append(readFloat(buffer))
            self.mass.append(readInt16(buffer)/32)
            _ = buffer.read(2)

class CycleEndPacket:
    def __init__(self, channelNumber):
        self.channelNumber = channelNumber

MEASURING_DATA = 0
CHANNEL_START = 1
CHANNEL_END = 2
CHANNEL_ABORTED = 3
CYCLE_END = 4
CHANNEL_INFORMATION = 5
MEASUREMENT_END = 6

class PrismaPlusBufferReader:
    def __init__(self):
        self.intensities = []
        self.timestamps = []

    def read(self, buffer):
        channelNumber = readInt8(buffer)
        dataType = readInt8(buffer)
        status = readInt8(buffer)
        numberOfData = readInt8(buffer)

        if status == CHANNEL_START:
            return ChannelStartPacket(buffer, channelNumber)
        elif status == CHANNEL_INFORMATION:
            return ChannelInformationPacket(buffer, channelNumber)
        elif status == CHANNEL_END:
            return ChannelEndPacket(buffer, numberOfData, channelNumber)
        elif status == CYCLE_END:
            return CycleEndPacket(channelNumber)
        elif status == CHANNEL_ABORTED:
            return ChannelAbortedPacket(channelNumber)
        else:
            raise RuntimeError('Unknown status %s' % status)

    def readAndAppend(self, buffer):
        while True:
            try:
                packet = self.read(buffer)
                if isinstance(packet, ChannelStartPacket):
                    self.timestamps.append(packet.timestamp)
                elif isinstance(packet, ChannelEndPacket):
                    self.intensities.extend(zip(packet.mass, packet.intensity))
            except TypeError:
                break

    def getData(self):
        if not self.intensities:
            return {}
        dataByMass = {}
        timestamps = self.timestamps
        unzippedMassesAndIntensities = zip(*self.intensities)
        masses = unzippedMassesAndIntensities[0]
        intensities = unzippedMassesAndIntensities[1]
        for timestamp, mass, intensity in zip(timestamps, masses, intensities):
            if not mass in dataByMass:
                dataByMass[mass] = []
            dataByMass[mass].append((timestamp, intensity))
        return dataByMass
