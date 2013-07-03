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
from deap import benchmarks
from deap import creator
from deap import tools

### PAT Controller Imports
from DefaultSettings.SettingsConsolidator import defaultSettings, overwriteSettings
from OverwriteSettings import MOTLoadDataCap
from PATController import PATController

### Set up optimisation parameter ranges.
paramBounds = (
	(-5.0, 5.0),	'2D_I_1'
	(-5.0, 5.0),	'2D_I_2'
	(-5.0, 5.0),	'2D_I_3'
	(-5.0, 5.0)		'2D_I_4'
)

populationSize = 5
generations = 5
phiG = 1	# Velocity weight toward best global particle.
phiP = 1	# Velocity weight towards best local particle.



creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Particle", list, fitness=creator.FitnessMax, speed=list, smin=None, smax=None, best=None)

def generate(paramBounds):
	''' Generate a particle with a set position and velocity'''
	part = creator.Particle(uniform(bL, bH) for bL, bH in paramBounds) 
	part.smax = [bH - bL for bL, bH in paramBounds]
	part.smin = [bL - bH for bL, bH in paramBounds]
	part.speed = [uniform(part.smin[i], part.smax[i]) for i in range(len(part))]
	return particle
	
def updateParticle(part, best, phiG, phiL)	
	'''
	Updates the particles velocity and position as follows:
	vNew = w*vOld + wP*(part-partBest) + wG(part - globBest)
	'''
	wP = (uniform(0, phiP)	# Velocity weight towards particle best.
	wG = (uniform(0, phiG)	# Velocity weight toward global best.
	vP = map(operator.mul, wP, map(operator.sub, part.best, part)	# Elementwise: wP(part.best - part)
	vG = map(operator.mul, wG, map(operator.sub, best, part)		# Elementwise: wG(best - part)
	part.speed = list(map(operator.add, part.speed, map(operator.add, vP, vG))))
	for i in range(len(particle)):
		if speed[i] < part.smin[i]:
			part.speed[i] = part.smin[i]
		elif speed[i] > part.smax[i]:
			part.speed[i] = part.smax[i]
	part[:] = list(map(operator.add, part, part.speed))
	for i in range(len(particle)):
		if part[i] < paramBound[i][0]:
			part[i] = paramBounds[i][0]
		elif part[i] > paramBounds[i][1]
			part[i] = paramBounds[i][1]
			
def evaluateParticle(part):
	''' Evaluate the goodness of particle based on the MOT loading.'''
	#PAT CONTROLLER CODE GOES HERE
	pass	

toolbox = base.Toolbox()
toolbox.register("particle", generate, paramBounds = paramBounds)
toolbox.register("population". tools.initRepeat, list, toolbox.particle)
toolbox.register("update", updateParticles, phiG = phiG, phiL = phiL
toolbox.register("evaluate", evaluateParticle)

def main():
	pop = toolbox.population(n=populationSize)
	best = None
	### statTools
	
	for g in range(generations):
		for part in pop;
			part.fitness.values = toolbox.evaluate(part)
			if not part.best or part.best.fitness < part.fitness:
				part.best = creator.Particle(part)
				part.best.fitness.values = part.fitness.values
			if not best or best.fitness < part.fitness:
				best = creator.Particle(part)
				best.fitness.values = part.fitness.values
		for part in pop:
			toolbox.update(part, best)
	return pop, best
	
if __name__ == "__main__":
    main()			
			
			 

	










