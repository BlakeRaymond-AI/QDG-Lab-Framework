from DeviceMediatorInterface import DeviceMediatorInterface
from DeviceControllers.ParticleSwarmOptimizer import ParticleSwarmOptimizer
import pickle
from os import path


class OptimizerMediator(DeviceMediatorInterface):
    """
    Mediator for Particle Swarm Optimizer. Majority of functionality arises from
    function calls unique to this mediator and not the normal common calls.
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
                                                self.w,
                                                self.alpha,
                                                self.minimization)

    def start(self):
        pass

    def stop(self):
        pass

    def save(self, pth):
        pass

    def processExpData(self, pth):
        pass

    def saveState(self, expPath):
        fPath = path.join(expPath, "OptimizerState.pkl")
        self.optimizer.saveState(fPath)

    def restoreState(self, expPath):
        fPath = path.join(expPath, "OptimizerState.pkl")
        if path.exists(fPath):
            self.optimizer.restoreState(fPath)

        # ----- Additional Functions

    def getParticle(self):
        deapPart = self.optimizer.getParticle()
        if deapPart:
            part = deapPart[:]
        else:
            part = deapPart
        self.part = part
        partString = pickle.dumps(part)
        return partString

    def evaluateParticle(self, expPath, trialPath):
        self.optimizer.evaluateParticle(expPath, trialPath)
        self.saveState(expPath)
        self.saveState(trialPath)

    def getBestParticle(self):
        return self.optimizer.best


if __name__ == '__main__':
    print "Running Optimization on Himmelblau Function"
    numOfParticles = 30
    numOfGenerations = 200
    paramBounds = ((-6, 6), (-6, 6))
    fitnessEvalScript = fnPath = 'C:\PAT\OptimizationFunctions\himmelblau.py'
    phiG = 1
    phiP = 1
    w = 1
    speedLimiter = 1
    minimization = True
    settingsDict = {
    'numOfParticles': numOfParticles,
    'numOfGenerations': numOfGenerations,
    'paramBounds': paramBounds,
    'fitnessEvalScript': fitnessEvalScript,
    'phiG': phiG,
    'phiP': phiP,
    'w': w,
    'speedLimiter': speedLimiter,
    'minimization': minimization
    }
    optMediator = OptimizerMediator(settingsDict)
    part = pickle.loads(optMediator.getParticle())
    while part:
        print part
        optMediator.evaluateParticle('', '')
        part = pickle.loads(optMediator.getParticle())
    best = optMediator.getBestParticle()
    print "Best Particle"
    print "Values: ", best
    print "Fitness: ", best.fitness
	
		
	
					
	