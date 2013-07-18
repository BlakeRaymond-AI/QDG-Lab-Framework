from socket import *
import pickle

#from DeviceMediators.LabJackMediator import LabJackMediator
#from DeviceMediators.PMDMediator import PMDMediator

HOST = 'LOCALHOST'
PORT = 34536
ADDR = (HOST, PORT)


class PATServer(object):
	def __init__(self):
		 self.serverSocket = socket(AF_INET, SOCK_STREAM)
		 self.serverSocket.bind(ADDR)
		 self.serverSocket.listen(5)
		 self.available = True
		 self.recieveMode = 0
		 self.deviceDict = {}
		 self.run()
	
	def run(self):
		(sessionSocket, sessionAddress) = self.serverSocket.accept()
		self.sessionSocket = sessionSocket
		self.recieveCommand()
	
	def sendMessage(self, msg):
		size = len(msg)
		size = zfill(str(size), 4)
		self.sessionSocket.send(size)
		self.sessionSocket.send(msg)
			
	def recieveMessage(self):
		sessionSocket = self.sessionSocket
		size = sessionSocket.recv(4)
		msg = sessionSocket.recv(int(size))
		self.interpretMessage(msg)
	
	def interpretMessage(self, msg):
		cmdChar = msg[0]
		msg = msg[1:]
		if cmdChar == 'c':
			self.handleCreation(msg)
		if cmdChar == 'm':
			self.handleMediatorCommand(msg)	
	
	def handleCreation(self, msg):
		deviceSettings = pickle.loads(msg)
		deviceDict = self.deviceDict
		for (key, deviceData) in deviceSettings.items():
			constructor = globals()[deviceData[0]]
			self.deviceDict[key] = constructor(deviceData[1])
	
	def handleMediatorCommand(self, msg):
		cmdDict = pickle.loads(msg)
		functionName = cmdDict['function']
		functionrArgs = cmdDict['arguments']
		fn = self.getattr(functionName)
		fn(*arguments)
	
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
	
#server = PATServer()			
			
# PROTOCOL
# 1. Start Server
# 2. Listen for socket connection.
# 3. Upon socket connection, first package sent is PixeLink values
# 	 dictionary
# 4. Subsequent packages are commands for mediator to execute.

# NOTES: Server should only be running one process at a time.

# 
# def recieved
# 	try:
# 		fn = getattr(self, name)
# 		fn()
# 	except AttributeError:
# 		print "WHOOPS"