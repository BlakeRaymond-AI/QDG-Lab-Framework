'''Default PATCLient Settings'''
from socket import gethostbyname


PATClientSettings = dict()
PATClientSettings['HOST'] = gethostbyname("QDG-PATPC")
PATClientSettings['PORT'] = 34567