from socket import *
from string import zfill
import pickle
# test comment
class PATClient(object):
	def __init__(self, dictionary):
		for (key, value) in dictionary.items():
			setattr(self, key, value)
		self.ADDR = (self.HOST, self.PORT)
		self.sessionSocket = socket(AF_INET, SOCK_STREAM)
		self.sessionSocket.connect(self.ADDR)
		print "Client Connected"
		
	def sendMessage(self, msg):
		'''Sends a message string to the server.'''
		size = len(msg)
		size = zfill(str(size), 4)
		self.sessionSocket.send(size)
		self.sessionSocket.send(msg)
	
	def sendCommand(self, dictionary, commandChar):
		'''
		Sends a command to the server. The interpretMessage function
		in the PATServer must be able to handle the commandChar sent,
		and the associated handler function must know how to unpack 
		the dictionary.
		'''
		dictData = pickle.dumps(dictionary)
		msg = commandChar + dictData
		self.sendMessage(msg)
	
	def sendMediatorCommand(self, fnName, fnArgs = ()):
		'''
		Used to send commands associated with the mediator interface.
		fnName must be the name of a valid mediator interface function.
		fnArgs must be a tuple of the arguments fnName takes.
		'''	
		cmdDict = dict()
		cmdDict['function'] = fnName
		cmdDict['arguments'] = fnArgs
		self.sendCommand(cmdDict, 'm')
	
	def sendSpecificDeviceCommand(self, devName, 
										fnName, 
										fnArgs = (), 
										waitForResponse = False, 
										pickledResponse = False
										):
		cmdDict = dict()
		cmdDict['function'] = fnName
		cmdDict['arguments'] = fnArgs
		cmdDict['deviceName'] = devName
		cmdDict['waitForResponse'] = waitForResponse
		self.sendCommand(cmdDict, 's')
		msg = ''
		if waitForResponse:
			msg = self.recieveMessage()
			if pickledResponse:
				value = pickle.loads(msg)
				return value
			else:
				return msg
		else:
			self.awaitConfirmation()
		
	def close(self):
		self.sendCommand({}, 'c')
		self.sessionSocket.close()
		
	def recieveMessage(self):
		'''Retrieves a message string from the server.'''
		sessionSocket = self.sessionSocket
		size = sessionSocket.recv(4)
		msg = sessionSocket.recv(int(size))
		return msg
	
	def awaitConfirmation(self):
		'''
		Forces client to wait until server confirms that the last command
		sent was executed.
		'''
		msg = self.recieveMessage()
		status = msg[:7]
		if status == "SUCCESS":
			print msg
		elif status == "FAILURE":
			print msg
		 	#throw an exception
		else:
		 	print "INVALID CONFIRMATION MESSAGE"
			

		
