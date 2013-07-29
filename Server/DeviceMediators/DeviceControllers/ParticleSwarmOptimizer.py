'''
Optimizer for MOT Loading

Adapted from:
http://deap.gel.ulaval.ca/doc/default/examples/pso_basic.html
'''
### DEAP Imports
import operator
from random import uniform
from numpy import array
from deap import base
from deap import creator
from deap import tools

class ParticleSwarmOptimizer(object):

	def __init__(self, paramBounds, 
						numOfParticles, 
						numOfGenerations, 
						fitnessEvalScript,
						phiG = 1, 
						phiP = 1,
						speedLimiter = 1,
						minimization = False
				):
		self.paramBounds = paramBounds
		self.numOfParticles = numOfParticles
		self.numOfGenerations = numOfGenerations
		self.fitnessEvalScript = fitnessEvalScript
		
		if minimization:
			weights = (-1.0,)
		else:
			weights = (1.0,)	
		print "Weights: ", weights
		
		creator.create("Fitness", base.Fitness, weights = weights)
		creator.create("Particle", list, fitness=creator.Fitness, speed=list, smin=None, smax=None, best=None)

		def generate(paramBounds):
			''' Generate a particle with a set position and velocity'''
			part = creator.Particle(uniform(bL, bH) for bL, bH in paramBounds) 
			part.smax = [(bH - bL) * speedLimiter for bL, bH in paramBounds]
			part.smin = [(bL - bH) * speedLimiter for bL, bH in paramBounds]
			part.speed = [uniform(part.smin[i], part.smax[i]) for i in range(len(part))]
			return part
	
		def updateParticle(part, best, phiG, phiP):	
			'''
			Updates the particles velocity and position as follows:
			vNew = w*vOld + wP*(part-partBest) + wG(part - globBest)
			'''
			wP = (uniform(0, 1) * phiP for _ in range(len(part)))	# Velocity weight towards particle best.
			wG = (uniform(0, 1) * phiG for _ in range(len(part)))	# Velocity weight toward global best.
			vP = map(operator.mul, wP, map(operator.sub, part.best, part))	# Elementwise: wP(part.best - part)
			vG = map(operator.mul, wG, map(operator.sub, best, part))		# Elementwise: wG(best - part)
			part.speed = list(map(operator.add, part.speed, map(operator.add, vP, vG)))
			for i in range(len(part)):
				if part.speed[i] < part.smin[i]:
					part.speed[i] = part.smin[i]
				elif part.speed[i] > part.smax[i]:
					part.speed[i] = part.smax[i]
			part[:] = list(map(operator.add, part, part.speed))
			
			for i in range(len(part)):
				if part[i] < paramBounds[i][0]:
					distanceOver = paramBounds[i][0] - part[i]
					part[i] = paramBounds[i][1] - distanceOver
					part.speed[i] = uniform(part.smin[i], part.smax[i])
				elif part[i] > paramBounds[i][1]:
					distanceOver = part[i] - paramBounds[i][1]
					part[i] = paramBounds[i][0] + distanceOver
					part.speed[i] = uniform(part.smin[i], part.smax[i])
			
		def evaluateParticle(args):
			''' Evaluate the goodness of particle based on the MOT loading.'''
			lcl = dict()
			for (key, value ) in args.items():
				lcl[key] = value
			lcl['fitness'] = None
		 	execfile(self.fitnessEvalScript, lcl)
		 	fitness = lcl['fitness']
			return fitness

		toolbox = base.Toolbox()
		toolbox.register("particle", generate, paramBounds = paramBounds)
		toolbox.register("population", tools.initRepeat, list, toolbox.particle)
		toolbox.register("update", updateParticle, phiG = phiG, phiP = phiP)
		toolbox.register("evaluate", evaluateParticle)

		stats = tools.Statistics(lambda ind: ind.fitness.values)
		stats.register("Min", min)
		stats.register("Max", max)
		stats.register("Avg", tools.mean)
		stats.register("Std", tools.std)
		self.stats = stats
    
		column_names = ["gen", "evals"]
		column_names.extend(stats.functions.keys())
		self.logger = tools.EvolutionLogger(column_names)
		self.logger.logHeader()
    	
		self.toolbox = toolbox
		self.particles = toolbox.population(n = numOfParticles)
		self.best = None
		self.currentGen = 0
		self.currentPart = 0
		
	def getParticle(self):
		currentPart = self.currentPart
		currentGen = self.currentGen
		
		if currentGen < self.numOfGenerations:
			part = self.particles[currentPart]
			return part
		else:
			return False
		
	def evaluateParticle(self, args = {}):
		part = self.particles[self.currentPart]
		best = self.best
		part.fitness.values = self.toolbox.evaluate(args)
		if not part.best or part.best.fitness < part.fitness:
			part.best = creator.Particle(part)
			part.best.fitness.values = part.fitness.values
		if not best or best.fitness < part.fitness:
			self.best = creator.Particle(part)
			self.best.fitness.values = part.fitness.values
		self.incrementParticles()
		
	def incrementParticles(self):
		self.currentPart += 1
		if self.currentPart >= self.numOfParticles:
			self.currentGen += 1
			self.currentPart = 0
			self.updateParticles()
	
	def updateParticles(self):
		for part in self.particles:
			self.toolbox.update(part, self.best)
		self.stats.update(self.particles)
		self.logger.logGeneration(gen=self.currentGen, evals=len(self.particles), stats=self.stats)
	
if __name__ == '__main__':
	paramBounds = ((-10, 10), (-10, 10))	
	PSO = ParticleSwarmOptimizer(paramBounds, 10, 1000, 'DefaultFitnessEvaluator.py', 1, 1, 1)
	part = PSO.getParticle()
	while part:
		PSO.evaluateParticle({'part' : part})
		part = PSO.getParticle()
	print "BEST: ", PSO.best, PSO.best.fitness
		
	










