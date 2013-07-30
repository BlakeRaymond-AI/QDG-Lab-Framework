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
												self.phiP,
												self.speedLimiter,
												self.minimization)												
	def start(self):
		pass
		
	def stop(self):
		pass

	def save(self, pth):
		pass
		
	def processExpData(self, pth):
		pass
	
	def getParticle(self):
		deapPart = self.optimizer.getParticle()
		if deapPart:
			part = deapPart[:]
		else:
			part = deapPart
		partString = pickle.dumps(part)
		return partString
		
	def evaluateParticle(self, trialPath, extraArgs = {}):
		args = {'dataPath' : trialPath}
		for (key, value) in extraArgs.items():
			args[key] = value
		self.optimizer.evaluateParticle(args)

	def getBestParticle(self):
		return self.optimizer.best

if __name__ == '__main__':
	numOfParticles = 30
	numOfGenerations = 1000
	paramBounds = ((-6, 6), (-6, 6))
	fitnessEvalScript = fnPath = 'C:\PAT\OptimizationFunctions\himmelblau.py'	
	phiG = 1
	phiP = 1
	speedLimiter = 1
	minimization = True
	settingsDict = {
		'numOfParticles' : numOfParticles,
		'numOfGenerations' : numOfGenerations,
		'paramBounds' : paramBounds,
		'fitnessEvalScript' : fitnessEvalScript,
		'phiG' : phiG,
		'phiP' : phiP,
		'speedLimiter' : speedLimiter,
		'minimization' : minimization
	}	
	print settingsDict['minimization']
	optMediator = OptimizerMediator(settingsDict)
	part = pickle.loads(optMediator.getParticle())
	while part:
		optMediator.evaluateParticle('', {'part' : part})
		part = pickle.loads(optMediator.getParticle())
	best = optMediator.getBestParticle()
	print "Best Particle"
	print "Values: ", best
	print "Fitness: ", best.fitness
	
		
	
					
	