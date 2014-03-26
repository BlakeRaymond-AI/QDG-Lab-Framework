from unittest import TestCase
import array

__author__ = 'Blake'

def loadData():
    filename = 'PrismaPlusData.buf'
    ints = array.array('B')
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            ints.append(int(line))
            line = f.readline()
    return ints

class TestPrismaPlusController(TestCase):
    data = loadData()

    def test_loadsData(self):
        self.assertTrue(len(self.data) > 0)



