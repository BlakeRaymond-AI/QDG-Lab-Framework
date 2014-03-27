from unittest import TestCase
from io import BytesIO
from PrismaPlusBufferReader import *

import matplotlib.pyplot as plt

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

    def test_canReadAndAppendTimestampsAndIntensities(self):
        reader = PrismaPlusBufferReader()
        buffer = BytesIO(bytes(self.data))
        reader.readAndAppend(buffer)

        times = reader.timestamps
        massIntensityTuples = reader.intensities

        self.assertEqual(1061, len(times))
        self.assertEqual(1061, len(massIntensityTuples))
        self.assertEqual({14, 16, 18, 28, 32, 40, 44}, set([pair[0] for pair in massIntensityTuples]))
        for pair in massIntensityTuples:
            self.assertAlmostEqual(0.0, pair[1], delta=2E-9)

    def test_canOrganizeTimestampsAndIntensitiesByMass(self):
        reader = PrismaPlusBufferReader()
        buffer = BytesIO(bytes(self.data))
        reader.readAndAppend(buffer)

        data = reader.getData()
        self.assertEqual({14, 16, 18, 28, 32, 40, 44}, set(data.keys()))
        for timesAndIntensities in data.values():
            self.assertGreater(len(timesAndIntensities), 0)

    def test_canPlot(self):
        reader = PrismaPlusBufferReader()
        buffer = BytesIO(bytes(self.data))
        reader.readAndAppend(buffer)

        data = reader.getData()

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
