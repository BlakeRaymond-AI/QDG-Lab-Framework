'key:Optimizer'
'''Default Optimizer Settings'''
OptimizerSettings = dict()
OptimizerSettings['fitnessEvalScript'] = 'C:\PAT\PATScripts\Optimizations\ScriptNameHere.py'
OptimizerSettings['numOfParticles'] = 0		# Number of particles in a generation.
OptimizerSettings['numOfGenerations'] = 0	# Number of generations.
OptimizerSettings['phiG'] = 1	# Velocity weight towards best global particle.
OptimizerSettings['phiP'] = 1	# Velocity weight towards best local particle.
OptimizerSettings['w'] = 1		# Velocity damping factor.
OptimizerSettings['alpha'] = 1 # Limits the max speed of a particle in any of it's dimensions to alpha * (upperBound - lowerBound)
OptimizerSettings['minimization'] = False	# Toggles minimization or maximization. 

# paramBounds is an n-tuple of 2-tuples representing the lower and upper bounds of paramaters.
paramBounds = (
	# (lowerBound1, upperBound1),
	# (lowerBound2, upperBound2),
	# ...
)
OptimizerSettings['paramBounds'] = paramBounds

OptimizerSettings['takeData'] = False	# Won't actually take data, but will enable optimizer.
OptimizerSettings['dataFolderName'] = "OptimizerData"
OptimizerSettings['persistent'] = True