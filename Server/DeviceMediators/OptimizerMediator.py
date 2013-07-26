from DeviceMediatorInterface import DeviceMediatorInterface
from DeviceControllers.ParticleSwarmOptimizer import ParticleSwarmOptimizer
import pickle
from os import path

class OptimizerMediator(DeviceMediatorInterface):
	"""
	Magic
	""" 
	
	def __init__(self, dictionary):
		for (k, v) in dictionary.items():
			setattr(self, k, v)
		
		self.optimizer = ParticleSwarmOptimizer(self.paramBounds, 
												self.numOfParticles, 
												self.numOfGenerations, 
												self.fitnessEvalScript,
												self.phiG, 
												self.phiP)												
	def start(self):
		pass
		
	def stop(self):
		pass

	def save(self, pth):
		pass
		
	def processExpData(self, pth):
		pass
	
	def getParticle(self):
		part = self.optimizer.getParticle()	
		partString = pickle.dumps(part)
		return partString
		
	def evaluateParticle(self, trialPath, extraArgs = {}):
		args = {'dataPath' : trialPath}
		for (key, value) in extraArgs.items():
			args[key] = value
		self.optimizer.evaluateParticle(args)

	def getBest(self):
		self.optimizer.best

if __name__ == '__main__':
	numOfParticles = 5
	numOfGenerations = 1000
	paramBounds = ((-10, 10), (-10, 10))
	fitnessEvalScript = 'DefaultFitnessEvaluator.py'
	phiG = 1
	phiP = 1
	settingsDict = {
		'numOfParticles' : numOfParticles,
		'numOfGenerations' : numOfGenerations,
		'paramBounds' : paramBounds,
		'fitnessEvalScript' : fitnessEvalScript,
		'phiG' : phiG,
		'phiP' : phiP
	}	
	optMediator = OptimizerMediator(settingsDict)
	part = pickle.loads(optMediator.getParticle())
	while part:
		optMediator.evaluateParticle('', {'part' : part})
		part = pickle.loads(optMediator.getParticle())
	print "BEST: ", optMediator.getBest()
	
		
	
					
	