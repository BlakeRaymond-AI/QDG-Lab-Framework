from socket import *
import signal
import sys
import pickle
from string import zfill

#from DeviceMediators.LabJackMediator import LabJackMediator
from DeviceMediators.PMDMediator import PMDMediator
# from DeviceMediators.Stabil_Ion_Mediator import SIMediator

HOST = gethostbyname(gethostname())
PORT = 15964
ADDR = (HOST, PORT)
server = None

def signal_handler(signal, frame):
	'''Handler designed to close server when Python instance is interrupted.'''
	print ''
	if server:
		server.close()
		print "Server Closed"
	sys.exit(0)

class PATServer(object):
	def __init__(self):
		self.serverSocket = socket(AF_INET, SOCK_STREAM)
		self.serverSocket.bind(ADDR)
		self.serverSocket.listen(5)
		self.available = True
		self.inUse = False
		self.sessionSocket = None
		self.sessionAddress = None
		self.deviceDict = {}
		global server
		server = self
		print "PAT Server Started"
		self.waitForClient()
	
	def waitForClient(self):
		'''Allows server to pickup an incoming connection from the PAT Client.'''
		print "Waiting for PAT Client."
		(sessionSocket, sessionAddress) = self.serverSocket.accept()
		self.inUse = True
		self.sessionSocket = sessionSocket
		print "---------- New Client Connected ---------"
		self.recieveMessage()
	
	def recieveMessage(self):
		'''Server will loop through this method, receiving messages from the client.'''	
		if self.inUse:
			print "Server waiting for commands."
			sessionSocket = self.sessionSocket
			size = sessionSocket.recv(4)
			msg = sessionSocket.recv(int(size))
			self.interpretMessage(msg)
			self.recieveMessage()
		else:
			self.waitForClient()
	
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
		elif cmdChar == 'i':
			self.handleInitialization(msg)
		elif cmdCHar == 's':
			self.handleSpecficiDeviceCommand(msg)
		elif cmdChar == 'c':
			self.handleClientClosing()
		elif cmdChar == 'e':
			print msg
		else:
			print "Invalid Command Char: " + cmdChar
	
	def handleInitialization(self, msg):
		deviceSettings = pickle.loads(msg)
		deviceDict = self.deviceDict
		for (key, deviceData) in deviceSettings.items():
			constructor = globals()[deviceData[0]]
			self.deviceDict[key] = constructor(deviceData[1])
		print "Devices Created"
		print deviceDict
	
	def handleMediatorCommand(self, msg):
		cmdDict = pickle.loads(msg)
		functionName = cmdDict['function']
		print "Mediator Command Recieved: " + functionName
		functionArgs = cmdDict['arguments']
		fn = getattr(self, functionName)
		fn(*functionArgs)
	
	def handleSpecificDeviceCommand(self, msg):
		cmdDict = pickel.loads(msg)
		functionName = cmdDict['function']
		functionArgs = cmdDict['arguments']
		deviceName = cmdDict['deviceName']
		device = self.deviceDict[deviceName]
		fn = getattr(device, functionName)
		fn(*functionArgs)
	
	def handleClientClosing(self):
		self.inUse = False
		self.sessionSocket = None
		self.sessionAddress = None
	
	def startDevices(self):
		print "Starting data collection devices."
		for device in self.deviceDict.values():
			device.start()
		print "All devices started."
		self.sendMessage("SUCCESS: All devices started.")
			
	def stopDevices(self):
		print "Stopping devices."
		for device in self.deviceDict.values():
			device.stop()
		print "All devices stopped"
		self.sendMessage("SUCCESS: All devices stopped.")

	def save(self, path):
		print "Saving data"
		for dev in self.deviceDict.values():
			if dev.takeData: 
				dev.save(path)
		self.sendMessage("SUCCESS: Device data saved.")
		
	def saveTrial(self, path, trialName):
		print "Saving trial data."
		for dev in self.deviceDict.values():
			if dev.takeData: 
				dev.save(path)	
		print "Trial data saved."
		self.sendMessage("SUCCESS: Trial data saved")	
	
if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	# signal.signal(signal.SIGTSTP, signal_handler)
	server = PATServer()	