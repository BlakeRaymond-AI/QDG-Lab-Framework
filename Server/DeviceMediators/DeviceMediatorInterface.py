'''
Interface which all device mediators must extend. Defines basic functions
which mediators must have.
'''


class DeviceMediatorInterface(object):
    '''
    Interface for device controllers. All devices used in the PAT apparatus
    should implement its methods, and settings dictionaries for mediators should
    include the field within __init__
    '''

    def __init__(self):
        self.takeData = True
        self.dataFolderName = "DatafolderUnspecified"

    def start(self):
        '''Initialise the device for an experimental run.'''
        raise NotImplementedError()

    def stop(self):
        '''Stop a device after an experimental run.'''
        raise NotImplementedError()

    def save(self, pth):
        '''Save the data associated with the device to the pth given.'''
        raise NotImplementedError()

    def processExpData(self, pth):
        '''Process the data associated with the device to the pth given.'''
        raise NotImplementedError()

    def saveState(self, pth):
        '''Saves the state of the device mediator into an external file.'''
        raise NotImplementedError()

    def restoreState(self, pth):
        '''Restores the state of the device mediator from an external file.'''
        raise NotImplementedError()