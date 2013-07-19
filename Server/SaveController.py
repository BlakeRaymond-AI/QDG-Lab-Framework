'''
Controller which generates path to which data will be saved. 
expPath: 	<basePath>/<Date>/<Time><_TimeSuffix>/
dataPath:	<basePath>/<Date>/<Time><_TimeSuffix>/Data

'''

from os import mkdir, path
from time import strftime


class DataFolderDuplicationError(Exception):
	'''
	Raised by SaveController when it detects that two different experimental
	runs are writing data to the same folder.
	'''
	
	def __init__(self, p):
		self.msg = 'The path {0} already exists from a previous run.'.format(p)

	def __str__(self):
		return repr(self.msg)

class SaveController(object):
	
	def __init__(self, basePath, timeSuffix):
		self.basePath = basePath
		self.timeSuffix = timeSuffix
		self.date = strftime('%Y_%m_%d')
		self.time = strftime('%H_%M_%S')
		self.expPath = self._generateExpPath()
		self.dataPath = self._generateDataPath()
		self._trialNum = 0
	
	def makeFolder(self, p):
		if path.isdir(p):
			raise DataFolderDuplicationError(p)
		else:
			mkdir(p)

	def generateTrialPath(self, trialName = ''):
		if not trialName:
			trialName = str(self._trialNum)
			self._trialNum += 1
		p = path.join(self.dataPath, trialName)	
		self.makeFolder(p)
		return p
	
	def _generateExpPath(self):
		p = self.basePath
		# Generate Date Folder
		p = path.join(p, self.date)	
		if not (path.isdir(p)):
			mkdir(p)
		# Generate Time Folder	
		if self.timeSuffix:
			fName =''.join([self.time, '_', self.timeSuffix])	
			p = path.join(p, fName)
		else: 
			p = path.join(p, self.time)	
		self.makeFolder(p)
		return p		
			
	def _generateDataPath(self):
		p = self.expPath
		p = path.join(p, 'Data')
		self.makeFolder(p)
		return p

if __name__ == '__main__':
	SaveController('C:\PAT\PATData', 'SaveTest')
	
	
	
		 	
		