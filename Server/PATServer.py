from socket import *
import errno
import signal
import sys
import pickle
from string import zfill
from SaveController import SaveController
from time import sleep
from os import path

from DeviceMediators.LabJackMediator import LabJackMediator
from DeviceMediators.PMDMediator import PMDMediator
from DeviceMediators.Stabil_Ion_Mediator import Stabil_Ion_Mediator
from DeviceMediators.MKS_SRG3_Mediator import MKS_SRG3_Mediator
from DeviceMediators.PixeLinkMediator import PixeLinkMediator
from DeviceMediators.OptimizerMediator import OptimizerMediator

HOST = gethostbyname(gethostname())
PORT = 15964
ADDR = (HOST, PORT)
server = None
dataPath = 'C:\\PAT\\PATData'

class PATServer(object):
	def __init__(self, expPath = ''):
		self.serverSocket = socket(AF_INET, SOCK_STREAM)
		self.serverSocket.bind(ADDR)
		self.serverSocket.listen(1)
		if expPath:
			self.expPath = expPath
			self.saveControllerPath = path.join(expPath, 'SaveController.pkl') 
		else:
			self.expPath = ''
			self.saveControllerPath = ''
		self.inUse = False
		self.sessionSocket = None
		self.sessionAddress = None
		self.deviceDict = {}
		self.deviceSettings = {}
		self.clientName = ''
		global server
		server = self
		print "PAT Server Started"
		self.waitForClient()
	
	def waitForClient(self):	
		'''Allows server to pickup an incoming connection from the PAT Client.'''
		while True:
			print "---------- Waiting for PAT Client ----------"
			if self.saveControllerPath:
				print "In multi-trial mode. Experiment file is: ", self.expPath
			(sessionSocket, sessionAddress) = self.serverSocket.accept()
			self.inUse = True
			self.sessionSocket = sessionSocket
			print "---------- New Client Connected ----------"
			self.recieveMessage()
	
	def recieveMessage(self):
		'''Server will loop through this method, receiving messages from the client.'''	
		sessionSocket = self.sessionSocket
		while self.inUse:
			print "Server waiting for commands."
			try:
				size = sessionSocket.recv(4)
				if size:
					msg = sessionSocket.recv(int(size))
					self.interpretMessage(msg)
				else:
					self.handleClientClosing()
			except error, e:	# error imported from socket
				print "Connection was reset."
				if e.errno == errno.ECONNRESET:
					self.handleClientClosing()
				else:
					raise e
	
	def sendMessage(self, msg):
		'''
		Sends message based on server protocol. First sends the size of the message
		that the client should wait on, followed by the actual message.
		'''
		size = len(msg)
		size = zfill(str(size), 4)
		self.sessionSocket.send(size)
		self.sessionSocket.send(msg)

	def close(self):
		'''Closes the server.'''
		if self.sessionSocket:
			self.sessionSocket.close()
		del(self)
	
	def interpretMessage(self, msg):
		'''
		Handles messages received from the client based on the first character
		of the message.
		'''
		cmdChar = msg[0]
		msg = msg[1:]
		if cmdChar == 'm':
			self.handleMediatorCommand(msg)
		elif cmdChar == 'r':
			self.handleReset(msg)
		elif cmdChar == 'n':
			self.handleName(msg)
		elif cmdChar == 'i':
			self.handleInitialization(msg)
		elif cmdChar == 's':
			self.handleSpecificDeviceCommand(msg)
		elif cmdChar == 'c':
			self.handleClientClosing()
		elif cmdChar == 'e':
			self.handleFitnessEval()	
		elif cmdChar == 'd':
			self.handleDictionarySave(msg)			
		else:
			print "Invalid Command Char: " + cmdChar
	
	def handleInitialization(self, msg):
		settingsDict = pickle.loads(msg)
		if self.saveControllerPath:
			SCFile = open(self.saveControllerPath, 'rb')
			self.saveController = pickle.load(SCFile)
			SCFile.close()
		else:
			self.saveController = SaveController(dataPath, self.clientName)
			self.expPath = self.saveController.expPath
			settingsDict.save(self.expPath)
		self.deviceSettings = settingsDict['deviceSettings']
		for (key, deviceData) in self.deviceSettings.items():
			devPicklePath = path.join(self.expPath, key + '.pkl')
			if deviceData[1]['persistent'] and path.exists(devPicklePath):
				dFile = open(devPicklePath, 'rb')
				dev = pickle.load(dFile)
				dFile.close()
			else:
				constructor = globals()[deviceData[0]]
				dev = constructor(deviceData[1])
				dev.devPicklePath = devPicklePath
			self.deviceDict[key] = dev
		self.sendMessage("SUCCESS: Devices created.")
		print "Devices Created"
		print self.deviceDict
	
	def handleReset(self, msg):
		print "Resetting Devices"
		self.sendMessage("SUCCESS: Reset command recieved.")
		self.handleClientClosing(multiTrial = True)
		
	def handleMediatorCommand(self, msg):
		cmdDict = pickle.loads(msg)
		functionName = cmdDict['function']
		print "Mediator Command Recieved: " + functionName
		functionArgs = cmdDict['arguments']
		fn = getattr(self, functionName)
		fn(*functionArgs)
	
	def handleDictionarySave(msg):
		dictionary = pickle.loads(msg)
		fPath1 = path.join([self.saveController.trialPath, 'customDat.txt'])
		fPath2 = path.join([self.saveController.trialPath, 'customDat.pkl'])
		file1 = open(fPath1, 'wb')
		file2 = open(fPath2, 'wb')
		file1.write(str(dictionary))
		file2.write(msg)
		file1.close()
		file2.close()
	
	def handleName(self, msg):
		print "Client for %s started." % msg
		self.clientName = msg
	
	def handleSpecificDeviceCommand(self, msg):
		cmdDict = pickle.loads(msg)
		functionName = cmdDict['function']
		functionArgs = cmdDict['arguments']
		deviceName = cmdDict['deviceName']
		waitForResponse = cmdDict['waitForResponse']
		device = self.deviceDict[deviceName]
		fn = getattr(device, functionName)
		fnMsg = "%s function in %s executed." % (functionName, deviceName)
		if waitForResponse:
			msg = fn(*functionArgs)
			self.sendMessage(msg)
		else:
			fn(*functionArgs)
			self.sendMessage("SUCCESS: " + fnMsg)
		print fnMsg 
	
	def handleClientClosing(self, multiTrial = False):
		del(self.deviceDict)
		del(self.deviceSettings)
		self.deviceDict = {}
		self.deviceSettings = {}
		self.saveController = None
		if not multiTrial:
			self.inUse = False
			self.sessionSocket = None
			self.sessionAddress = None
			self.clientName = ''
			self.saveControllerPath = ''
			self.expPath = ''
			print "Client Closed"
	
	def handleFitnessEval(self):
		optimizer = self.deviceDict['Optimizer']
		optimizer.evaluateParticle(self.saveController.expPath, self.saveController.trialPath)
		print "Evaluating fitness."
	
	def startDevices(self):
		print "Starting data collection devices."
		for device in self.deviceDict.values():
			device.start()
		print "All devices started."
		self.sendMessage("SUCCESS: All devices started.")
		self.stopDevices()
			
	def stopDevices(self):
		print "Stopping devices."
		dataCollectionFailed = False
		for device in self.deviceDict.values():
			if device.stop():
				dataCollectionFailed = True
				print "Data collection by", device, "failed."
		print "All devices stopped."
		self.sendMessage("SUCCESS: All devices stopped.")
		self.sendDataCollectionStatus(dataCollectionFailed)
	
	def sendDataCollectionStatus(self, dataCollectionFailed):	
		if dataCollectionFailed:
			msg = '1'
		else:
			msg = '0'
		self.sendMessage(msg)	
		
	def save(self):
		print "Saving data."
		path = self.saveController.dataPath
		for dev in self.deviceDict.values():
			dev.save(path)
		self.sendMessage("SUCCESS: Device data saved.")

	def saveTrial(self, trialName):
		print "Saving trial data."
		trialPath = self.saveController.generateTrialPath(trialName)
		self.deviceSettings.save(trialPath)
		self.expPath = self.saveController.expPath
		for dev in self.deviceDict.values():
			dev.save(trialPath)
			if dev.persistent:
				dev.saveState(self.expPath)
		print "Trial data saved."
		SCPath = path.join(self.expPath, "SaveController.pkl")
		self.saveControllerPath = SCPath
		SCFile = open(SCPath, 'wb')
		pickle.dump(self.saveController, SCFile)
		SCFile.close()
		self.sendMessage("SUCCESS: Trial data saved.")

	def processExpData(self):
		print "Processing Data."
		path = self.saveController.dataPath
		for dev in self.deviceDict.values():
			if dev.processData:
				dev.processExpData(path)
		self.sendMessage("SUCCESS: Device data processed.")
		
def signal_handler(signal, frame):
	'''Handler designed to close server when Python instance is interrupted.'''
	print ''
	if server:
		server.close()
		print "Server Closed"
	sys.exit(0)
			
if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	server = PATServer()
	