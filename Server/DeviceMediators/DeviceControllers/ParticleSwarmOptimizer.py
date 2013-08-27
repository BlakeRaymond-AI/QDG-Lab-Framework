'''
Optimizer for MOT Loading

Adapted from:
http://deap.gel.ulaval.ca/doc/default/examples/pso_basic.html

Designed to be used from within the PATFramework.
'''
### DEAP Imports

from random import uniform
from numpy import array
from deap import base
from deap import creator
from deap import tools
from os import path
import copy
import csv
import operator
import pickle

class ParticleSwarmOptimizer(object):

	def __init__(self, paramBounds, 
						numOfParticles, 
						numOfGenerations, 
						fitnessEvalScript,
						phiG = 1, 
						phiP = 1,
						w = 1,
						alpha = 1,
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
		creator.create("Fitness", base.Fitness, weights = weights)
		creator.create("Particle", list, fitness=creator.Fitness, speed=list, smin=None, smax=None, best=None)

		def generate(paramBounds):
			''' Generate a particle with a set position and velocity'''
			part = creator.Particle(uniform(bL, bH) for bL, bH in paramBounds) 
			part.smax = [(bH - bL) * alpha for bL, bH in paramBounds]
			part.smin = [(bL - bH) * alpha for bL, bH in paramBounds]
			part.speed = [uniform(part.smin[i], part.smax[i]) for i in range(len(part))]
			return part
	
		def updateParticle(part, best, phiG, phiP, w):	
			'''
			Updates the particles velocity and position as follows:
			vNew = w*vOld + wP*(part-partBest) + wG(part - globBest)
			'''
			wP = (uniform(0, 1) * phiP for _ in range(len(part)))	# Velocity weight towards particle best.
			wG = (uniform(0, 1) * phiG for _ in range(len(part)))	# Velocity weight toward global best.
			vP = map(operator.mul, wP, map(operator.sub, part.best, part))	# Elementwise: wP(part.best - part)
			vG = map(operator.mul, wG, map(operator.sub, best, part))		# Elementwise: wG(best - part)
			wvOld = [v * w for v in part.speed]  					# Elementwise: w * vOld
			part.speed = list(map(operator.add, wvOld, map(operator.add, vP, vG)))
			
			# Check that all of the particles individual velocity components are
			# within the velocity bounds and correct them if not.
			for i in range(len(part)):
				if part.speed[i] < part.smin[i]:
					part.speed[i] = part.smin[i]
				elif part.speed[i] > part.smax[i]:
					part.speed[i] = part.smax[i]
			
			partOld = copy.copy(part[:])
			part[:] = list(map(operator.add, part, part.speed))
			
			# Check that all of the particles individual position components are
			# within the position bounds and correct them if not.
			for i in range(len(part)):
				if part[i] < paramBounds[i][0]:
					part[i] = uniform(paramBounds[i][0], partOld[i])
					part.speed[i] = part[i] - partOld[i]
				elif part[i] > paramBounds[i][1]:
					part[i] = uniform(partOld[i], paramBounds[i][1])
					part.speed[i] = part[i] - partOld[i]
			
		def evaluateParticle(args):
			'''
			Returns a fitness value which is the result of the 
			fitnessEvalScript.
			'''
			lcl = dict()
			for (key, value ) in args.items():
				lcl[key] = value
			lcl['fitness'] = None
		 	execfile(self.fitnessEvalScript, lcl)
		 	fitness = lcl['fitness']
			return (fitness,)

		toolbox = base.Toolbox()
		toolbox.register("particle", generate, paramBounds = paramBounds)
		toolbox.register("population", tools.initRepeat, list, toolbox.particle)
		toolbox.register("update", updateParticle, phiG = phiG, phiP = phiP, w = w)
		toolbox.register("evaluate", evaluateParticle)
     	
		self.toolbox = toolbox
		self.particles = toolbox.population(n = numOfParticles)
		self.best = None
		self.currentGen = 0
		self.currentPart = 0
		
	def getParticle(self):
		'''
		Gets the next particle for the optimization. Returns false the 
		optimization is complete.
		'''
		currentPart = self.currentPart
		currentGen = self.currentGen
		if currentGen < self.numOfGenerations:
			part = self.particles[currentPart]
			print "OPTIMIZER: Generation %d, Particle %d" % (currentGen, currentPart)
			return part
		else:
			return False
		
	def evaluateParticle(self, expPath, trialPath):
		'''
		Passes the expPath and trialPath to the fitnessEvalScript, assigns a
		fitness to the current particle, updates the local and global
		best and writes the information into a file in the trialPath given.
		'''
		part = self.particles[self.currentPart]
		best = self.best
		args = {'expPath' : expPath, 'trialPath' : trialPath, 'part' : part}
		part.fitness.values = self.toolbox.evaluate(args)
		if not part.best or part.best.fitness < part.fitness:
			part.best = creator.Particle(part)
			part.best.fitness.values = part.fitness.values
		if not best or best.fitness < part.fitness:
			self.best = creator.Particle(part)
			self.best.fitness.values = part.fitness.values
		fPath = path.join(trialPath, 'particle.csv')
		file = open(fPath, 'wb')
		fileWriter = csv.writer(file, delimiter=',')
		fileWriter.writerow(['Generation', 'Particle'])
		fileWriter.writerow([self.currentGen, self.currentPart])
		fileWriter.writerow(['Identifier', 'Parameters', 'Fitness'])
		fileWriter.writerow(['Particle', part, part.fitness])
		fileWriter.writerow(['Particle Best', part.best, part.best.fitness])
		fileWriter.writerow(['Global Best', self.best, self.best.fitness])
		file.close()
		self.incrementParticles()
			
	def incrementParticles(self):
		'''Increments the particle count and/or generation count.'''
		self.currentPart += 1
		if self.currentPart >= self.numOfParticles:
			self.currentGen += 1
			self.currentPart = 0
			self.updateParticles()
	
	def updateParticles(self):
		'''Updates all of the particles.'''
		for part in self.particles:
			self.toolbox.update(part, self.best)
			
	def saveState(self, fName):
		'''Saves the state of the optimizer to the given file name.'''
		file = open(fName, 'wb')
		pickle.dump(self.currentGen, file)
		pickle.dump(self.currentPart, file)
		pickle.dump(self.best, file)
		pickle.dump(self.particles, file)
		file.close()
	
	def restoreState(self, fName):
		'''Restores the state of the optimizer from the given file name.'''
		file = open(fName, 'rb')
		self.currentGen = pickle.load(file)
		self.currentPart = pickle.load(file)
		self.best = pickle.load(file)
		self.particles = pickle.load(file)
		file.close()

if __name__ == '__main__':
	paramBounds = ((-10, 10), (-10, 10))
	fnPath = 'C:\PAT\OptimizationFunctions\h1.py'	
	PSO = ParticleSwarmOptimizer(paramBounds, 10, 1000, fnPath)
	part = PSO.getParticle()
	while part:
		PSO.evaluateParticle('', '')
		part = PSO.getParticle()
	print "BEST: ", PSO.best, PSO.best.fitness

	










