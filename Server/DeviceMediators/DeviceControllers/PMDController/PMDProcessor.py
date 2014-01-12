from numpy import genfromtxt
import matplotlib.pyplot as plt
import sys


def processData(inFile, outFile):
    t, p = genfromtxt(inFile, delimiter=',', unpack=True)

    xLbl = t[0]
    yLbl = p[0]

    t = t[1:]
    p = p[1:]

    plt.plot(t, p)
    plt.xlabel(xLbl)
    plt.ylabel(yLbl)
    plt.show()


arguments = sys.argv
inFile = arguments[1]
outFile = arguments[0]
print arguments
print inFile
print outFile
#processData(inFile, outFile)
