from socket import *
from string import zfill
import pickle

host= 'LOCALHOST'
port = 34536

class PATClient(object):
	def __init__(self): #, dictionary)
		self.host = host
		self.port = port
		self.addr = (self.host, self.port)
		self.sessionSocket = socket(AF_INET, SOCK_STREAM)
		self.sessionSocket.connect(self.addr)
		
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
		if cmdChar == 'o':
			print msg
	
	def awaitConfirmation(self, msg):
		sessionSockect = self.sessionSocket
		size = sessionSocket.recv(4)
		msg = sessionsSocket.recv(4)
		status = msg[:7]
		if status == SUCCESS:
			print msg
		elif status == FAILURE:
			print msg
		 	#throw an exception
		else:
		 	print "INVALID CONFIRMATION MESSAGE"
		
	def sendCommand(self, dictionary, commandChar):
		dictData = pickle.dumps(dictionary)
		msg = commandChar + dictData
		self.sendMessage(msg)
	
	def createDevices(self, deviceDict):
		sendCommand(deviceDict, 'c')
			
	def sendMediatorCommand(self, fnName,	# String 
								  fnArgs = () # Tuple
								  ):	
		cmdDict = dict()
		cmdDict["function"] = fnName
		cmdDict["arguments"] = fnArgs
		self.sendCommand(cmdDict, 'c')
		
