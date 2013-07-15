from os import path, walk
import sys

scriptPath = sys.argv[0]

mainPath, script = path.split(scriptPath)
settingsPath = path.join(mainPath, 'Settings')
templateName = path.join(mainPath, 'settingsTemplate.py')
template = open(templateName, 'wb')

for root, dirs, files in walk(settingsPath):
	for file in files:
		if file.endswith('.py') and not file.startswith('__'):
			fPath = path.join(settingsPath, file)
			f = open(fPath, 'rb')
			for line in f:
				line = '# ' + line
				template.write(line)
			f.close()
			template.write('\n # ----------------------------------- \n')
			#template.write('')
			#template.write('')
			
			
template.close()