class PATError(Exception):
	def __str__(self):
		return repr('An error has occured with the PAT apparatus')

