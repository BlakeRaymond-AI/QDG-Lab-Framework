"""
This file is going to be placed in the Generic sub-package.
This file is not automatically generated!!
"""
#from ctypes import *
from ctypes import *
import Variables as V

def get_type_name(t):
    "t is a ctype instance. return its name as a string"
    n = t.__name__
    n_pointers = 0
    while n.startswith('LP_'):
        n_pointers += 1
        n = n[3:]
    n2= n
    for i in range(n_pointers):
        n2 = "POINTER(%s)" % n2
    return n2

U64 = c_ulonglong
U32 = c_ulong
U16 = c_ushort
U8  = c_uint8
S64 = c_longlong
S32 = c_long
S16 = c_short
S8  = c_int8
F32 = c_float

PXL_RETURN_CODE = c_int
float = c_float
ULONG = c_ulong
BYTE = c_uint8
UCHAR = c_uint8
HANDLE = c_uint32
LPSTR = c_char_p
LPVOID = c_void_p

class MyStructure(Structure):
    def __init__(self,*args,**kw):
        Structure.__init__(self,*args,**kw)
    
    def __str__(self):
        s = "%s:\n" % self.__class__.__name__
        for (name,type) in self._fields_:
            s += "\t%s -> %s\n" % (name,getattr(self,name))
        return s
    
    __repr__ = __str__

class FEATURE_PARAM(MyStructure):
    _fields_ = [
        ('fMinValue',float),
        ('fMaxValue',float),
        ]

class CAMERA_FEATURE(MyStructure):
    _fields_ = [
        ('uFeatureId',U32),
        ('uFlags',U32),
        ('uNumberOfParameters',U32),
        ('pParams',POINTER(FEATURE_PARAM)),
        ]

class CAMERA_FEATURES(MyStructure):
    _fields_ = [
        ('uSize',U32),
        ('uNumberOfFeatures',U32),
        ('pFeatures',POINTER(CAMERA_FEATURE)),
        ]
    
class CAMERA_INFO(MyStructure):
    _fields_ = [
        ('VendorName',S8*33),
        ('ModelName',S8*33),
        ('Description',S8*256),
        ('SerialNumber',S8*33),
        ('FirmwareVersion',S8*12),
        ('FPGAVersion',S8*12),
        ('CameraName',S8*256),
        ]


def __get_simple_float_structure(name,attribute):
    cd = {'_fields_' : [(attribute,float)]}
    return type(name,(MyStructure,),cd)

_frame_desc_structures = fds = {}
for sn in ('Brightness','AutoExposure','Sharpness','WhiteBalance','Hue',
              'Saturation','Gamma','Shutter','Gain','Iris','Focus','Temperature',
              'Zoom','Pan','Tilt','OpticalFilter','FrameRate','Decimation','PixelFormat',
              'DecimationMode','Rotate','ImagerClkDivisor','TriggerWithControlledLight',
              'MaxPixelSize'):
    _frame_desc_structures[sn] = __get_simple_float_structure(sn,'fValue')

class Trigger(MyStructure):
    _fields_ = [('fMode',float),('fType',float),('fPolarity',float),('fParameter',float)]
fds['Trigger'] = Trigger

PXL_MS = V.PXL_MAX_STROBES
class GPIO(MyStructure):
    _fields_ = [('fMode',float*PXL_MS),('fPolarity',float*PXL_MS),('fParameter1',float*PXL_MS),
                ('fParameter2',float*PXL_MS),('fParameter3',float*PXL_MS)]
fds['GPIO'] = GPIO

class Roi(MyStructure):
    _fields_ = [('fLeft',float),('fTop',float),('fWidth',float),('fHeight',float)]
fds['Roi'] = Roi

class Flip(MyStructure):
    _fields_ = [('fHorizontal',float),('fVertical',float)]
fds['Flip'] = Flip

class ExtendedShutter(MyStructure):
    _fields_ = [('fKneePoint',float*V.PXL_MAX_KNEE_POINTS)]
fds['ExtendedShutter'] = ExtendedShutter

class AutoROI(MyStructure):
    _fields_ = [('fLeft',float),('fTop',float),('fWidth',float),('fHeight',float)]
fds['AutoROI'] = AutoROI

class WhiteShading(MyStructure):
    _fields_ = [('fRedGain',float),('fGreenGain',float),('fBlueGain',float)]
fds['WhiteShading'] = WhiteShading


class FRAME_DESC(MyStructure):
    _fields_ = [
        ('uSize',U32),
        ('fFrameTime',float),
        ('uFrameNumber',U32),
        ]
    for (n,t) in _frame_desc_structures.items():
        _fields_.append((n,t))
                  
    def __init__(self):
        self.uSize = sizeof(FRAME_DESC)
      
class ERROR_REPORT(MyStructure):
    _fields_ = [
        ('uReturnCode',PXL_RETURN_CODE),
        ('strFunctionName',S8*32),
        ('strReturnCode',S8*32),
        ('strReport',S8*256)
        ]

#vars = locals().copy()
#for (n,t) in vars.items():
#    if isinstance(t,type) and issubclass(t,MyStructure):
#        types_map[n] = n


