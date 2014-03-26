from unittest import TestCase
import array
from io import BytesIO
import struct
from PrismaPlusBufferReader import PrismaPlusBufferReader, ChannelStartPacket, ChannelInformationPacket, \
    ChannelEndPacket, CycleEndPacket, ChannelAbortedPacket

import numpy as np
import matplotlib.pyplot as plt

__author__ = 'Blake'

def loadData():
    filename = 'PrismaPlusData.buf'
    ints = array.array('B')
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            ints.append(int(line))
            line = f.readline()
    return struct.pack('%sB' % len(ints), *ints)

class TestPrismaPlusBufferReader(TestCase):
    data = loadData()

    def test_parsesChannelStart(self):
        channelStartData = bytes(self.data[:14])
        buffer = BytesIO(channelStartData)
        reader = PrismaPlusBufferReader()
        packet = reader.read(buffer)[0]

        self.assertIsInstance(packet, ChannelStartPacket)
        self.assertEqual(130398063170580000, packet.timestamp)
        self.assertEqual(10, packet.maxNumberOfDataTuples)

    def test_parsesChannelInformation(self):
        channelInformationData = bytes(self.data[26:36])
        buffer = BytesIO(channelInformationData)
        reader = PrismaPlusBufferReader()
        packet = reader.read(buffer)[0]

        self.assertIsInstance(packet, ChannelInformationPacket)
        self.assertEqual(9999, packet.firstMass)

    def test_parsesChannelEnd(self):
        channelEndData = bytes(self.data[14:26])
        buffer = BytesIO(channelEndData)
        reader = PrismaPlusBufferReader()
        packet = reader.read(buffer)[0]

        self.assertIsInstance(packet, ChannelEndPacket)
        self.assertEqual(1, packet.numberOfData)
        self.assertEqual(1, len(packet.intensity))
        self.assertEqual(1, len(packet.mass))
        self.assertEqual(-1.1098653940333492e-10, packet.intensity[0])
        self.assertEqual(1024, packet.mass[0])

    def test_parsesCycleEnd(self):
        reader = PrismaPlusBufferReader()
        buffer = BytesIO(bytes(self.data))
        for _ in range(6):
            _ = reader.read(buffer)

        packet = reader.read(buffer)[0]
        self.assertIsInstance(packet, CycleEndPacket)

    def test_parsesChannelAbortedPacket(self):
        reader = PrismaPlusBufferReader()
        buffer = BytesIO(bytes(self.data))
        try:
            while True:
                packet = reader.read(buffer)[0]
                if isinstance(packet, ChannelAbortedPacket):
                    break
        except:
            self.fail()

    def test_parsesAllPackets(self):
        reader = PrismaPlusBufferReader()
        buffer = BytesIO(bytes(self.data))
        try:
            while True:
                _ = reader.read(buffer)
        except (IOError, TypeError):
            pass
        else:
            self.fail()

    def test___(self):
        reader = PrismaPlusBufferReader()
        buffer = BytesIO(bytes(self.data))
        packets = []
        while True:
            try:
                packets.append(reader.read(buffer))
            except (IOError, TypeError):
                break
        startPackets = filter(lambda packet: isinstance(packet, ChannelStartPacket) and packet.channelNumber == 0, packets)
        endPackets = filter(lambda packet: isinstance(packet, ChannelEndPacket) and packet.channelNumber == 0, packets)

        self.assertEqual(len(startPackets), len(endPackets))
        self.assertGreater(len(startPackets), 0)

        times = []
        masses = []
        intensities = []

        for packet in startPackets:
            times.append(packet.timestamp)
        for packet in endPackets:
            for mass in packet.mass:
                masses.append(mass)
            for intensity in packet.intensity:
                intensities.append(intensity)

        times = np.array(times)
        masses = np.array(masses)
        intensities = np.array(intensities)

        plt.plot(times, intensities)
        plt.show()

    def test_readAll(self):
        reader = PrismaPlusBufferReader()
        buffer = BytesIO(bytes(self.data))
        (timestamps, intensities, masses) = reader.readAll(buffer)

        intensities = intensities[:len(intensities)-1]

        sz = min([len(timestamps)] + [len(intensity) for intensity in intensities])

        plt.plot(timestamps[:sz], intensities[0][:sz])
        plt.plot(timestamps[:sz], intensities[1][:sz])
        plt.plot(timestamps[:sz], intensities[2][:sz])
        plt.plot(timestamps[:sz], intensities[3][:sz])
        plt.plot(timestamps[:sz], intensities[4][:sz])
        plt.plot(timestamps[:sz], intensities[5][:sz])
        plt.plot(timestamps[:sz], intensities[6][:sz])

        plt.legend(masses)

        plt.show()
