from os import path, walk
import sys

scriptPath = sys.argv[0]

mainPath, script = path.split(scriptPath)
settingsPath = path.join(mainPath, 'DefaultSettings')
templateName = path.join(mainPath, 'settingsTemplate.py')
template = open(templateName, 'wb')
keys = []

for root, dirs, files in walk(settingsPath):
    for file in files:
        if file.endswith('.py') and not file.startswith('__'):
            fPath = path.join(settingsPath, file)
            f = open(fPath, 'rb')
            l = f.readline()
            if l[1:4] == "key":
                keys.append(l[5:-2])
            for line in f:
                line = '#' + line
                template.write(line)
            f.close()
            template.write('\n# ----------------------------------- \n')
    template.write('\nupdatePackage = { \n')
    for key in keys:
        template.write(''.join(['#\'', key, '\'', ' :	,\n']))
    template.write('}\n')
template.close()

