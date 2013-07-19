# Automatically generated
import os
import sys
path_components = ['E:', 'PyProjects', 'PyPixeLINK', 'CodeGenerator']
sys.path.insert(0,os.sep.join(path_components))
from ctypes import *
# this module is found in the code generator folder
from Types import *
######################################################################
# PixeLINK status CODES
######################################################################
error_msg = {
	0 : "The function completed successfully",
	1 : "Indicates that a set feature is successful but one or more parameter had to be changed (ROI)",
	2 : "The stream is already started",
	3 : "There is not as much memory as needed for optimum performance. Performance may be affected.",
	-2147483644 : "A buffer passed as parameter is too small.",
	-2147483643 : "The function cannot be called at this time",
	-2147483642 : "The API cannot complete the request",
	-2147483647 : "Unknown error",
	-2147483640 : "There is no response from the camera",
	-2147483639 : "The Camera responded with an error",
	-2147483638 : "The API does not recognize the camera",
	-2147483637 : "There is not enough 1394 bandwidth to start the stream",
	-2147483636 : "The API can not allocate the required memory",
	-2147483646 : "The handle parameter invalid",
	-2147483634 : "The serial number coundn't be obtained from the camera",
	-2147483633 : "A camera with that serial number coundn't be found",
	-2147483632 : "Not enough disk space to complete an IO operation",
	-2147483631 : "An error occurred during an IO operation",
	-2147483630 : "Application requested streaming termination",
	-2147483645 : "Invalid parameter",
	-2147483628 : "Error creating the preview window",
	-2147483626 : "Indicates that a feature set value is out of range",
	-2147483625 : "There is no camera available",
	-2147483624 : "Indicated that the name specified is not a valid camera name",
	-2147483623 : "GextNextFrame() can't be called at this time because its being use by an FRAME_OVERLAY callback function",
	-2147483622 : "A frame was still in use when the buffers were deallocated.",
	-2147483641 : "The camera is already being used by another application",
	-1879048179 : "The camera returned an invalid frame (image)",
	-1879048180 : "Timeout waiting for the camera to respond",
	-2147483635 : "The API cannot run on the current operating system",
	-1879048178 : "An operating system service returned an error",
	-2147483629 : "The pointer parameter=NULL",
}
def API_SUCCESS(rc): return not (rc & 0x80000000)
######################################################################
######################################################################

class PixeLINKException(Exception):
    def __init__(self,error_code,handle):
        self.error_code = error_code
        msg = error_msg[error_code]
        error_report = ERROR_REPORT()
        p_error_report = POINTER(ERROR_REPORT)(error_report)
        Generic().GetErrorReport(handle,p_error_report)
        msg += '\nerror_report: ' + ''.join(chr(c) for c in error_report.strReturnCode)
        msg += '\nfunction_name: ' + ''.join(chr(c) for c in error_report.strFunctionName)
        Exception.__init__(self,msg)
    
######################################################################
######################################################################
class Generic(object):
	def __new__(cls):
		dll = windll.PxLAPI41
		cls._CameraRead = dll['_PxL_4_1_CameraRead@12']
		cls._CameraRead.argtypes = [c_ulong,c_ulong,POINTER(c_ubyte)]
		cls._CameraRead.restype = c_int32
		cls._CameraWrite = dll['_PxL_4_1_CameraWrite@12']
		cls._CameraWrite.argtypes = [c_ulong,c_ulong,POINTER(c_ubyte)]
		cls._CameraWrite.restype = c_int32
		cls._CreateDescriptor = dll['_PxL_4_1_CreateDescriptor@12']
		cls._CreateDescriptor.argtypes = [c_ulong,POINTER(c_ulong),c_ulong]
		cls._CreateDescriptor.restype = c_int32
		cls._FormatClip = dll['_PxL_4_1_FormatClip@12']
		cls._FormatClip.argtypes = [c_char_p,c_char_p,c_ulong]
		cls._FormatClip.restype = c_int32
		cls._FormatImage = dll['_PxL_4_1_FormatImage@20']
		cls._FormatImage.argtypes = [c_void_p,POINTER(FRAME_DESC),c_ulong,c_void_p,POINTER(c_ulong)]
		cls._FormatImage.restype = c_int32
		cls._GetCameraFeatures = dll['_PxL_4_1_GetCameraFeatures@16']
		cls._GetCameraFeatures.argtypes = [c_ulong,c_ulong,POINTER(CAMERA_FEATURES),POINTER(c_ulong)]
		cls._GetCameraFeatures.restype = c_int32
		cls._GetCameraInfo = dll['_PxL_4_1_GetCameraInfo@8']
		cls._GetCameraInfo.argtypes = [c_ulong,POINTER(CAMERA_INFO)]
		cls._GetCameraInfo.restype = c_int32
		cls._GetErrorReport = dll['_PxL_4_1_GetErrorReport@8']
		cls._GetErrorReport.argtypes = [c_ulong,POINTER(ERROR_REPORT)]
		cls._GetErrorReport.restype = c_int32
		cls._GetFeature = dll['_PxL_4_1_GetFeature@20']
		cls._GetFeature.argtypes = [c_ulong,c_ulong,POINTER(c_ulong),POINTER(c_ulong),POINTER(c_float)]
		cls._GetFeature.restype = c_int32
		cls._GetNextFrame = dll['_PxL_4_1_GetNextFrame@16']
		cls._GetNextFrame.argtypes = [c_ulong,c_ulong,c_void_p,POINTER(FRAME_DESC)]
		cls._GetNextFrame.restype = c_int32
		cls._GetNumberCameras = dll['_PxL_4_1_GetNumberCameras@8']
		cls._GetNumberCameras.argtypes = [POINTER(c_ulong),POINTER(c_ulong)]
		cls._GetNumberCameras.restype = c_int32
		cls._Initialize = dll['_PxL_4_1_Initialize@8']
		cls._Initialize.argtypes = [c_ulong,POINTER(c_ulong)]
		cls._Initialize.restype = c_int32
		cls._LoadSettings = dll['_PxL_4_1_LoadSettings@8']
		cls._LoadSettings.argtypes = [c_ulong,c_ulong]
		cls._LoadSettings.restype = c_int32
		cls._RemoveDescriptor = dll['_PxL_4_1_RemoveDescriptor@8']
		cls._RemoveDescriptor.argtypes = [c_ulong,c_ulong]
		cls._RemoveDescriptor.restype = c_int32
		cls._ResetPreviewWindow = dll['_PxL_4_1_ResetPreviewWindow@4']
		cls._ResetPreviewWindow.argtypes = [c_ulong]
		cls._ResetPreviewWindow.restype = c_int32
		cls._SaveSettings = dll['_PxL_4_1_SaveSettings@8']
		cls._SaveSettings.argtypes = [c_ulong,c_ulong]
		cls._SaveSettings.restype = c_int32
		cls._SetCameraName = dll['_PxL_4_1_SetCameraName@8']
		cls._SetCameraName.argtypes = [c_ulong,c_char_p]
		cls._SetCameraName.restype = c_int32
		cls._SetFeature = dll['_PxL_4_1_SetFeature@20']
		cls._SetFeature.argtypes = [c_ulong,c_ulong,c_ulong,c_ulong,POINTER(c_float)]
		cls._SetFeature.restype = c_int32
		cls._SetStreamState = dll['_PxL_4_1_SetStreamState@8']
		cls._SetStreamState.argtypes = [c_ulong,c_ulong]
		cls._SetStreamState.restype = c_int32
		cls._Uninitialize = dll['_PxL_4_1_Uninitialize@4']
		cls._Uninitialize.argtypes = [c_ulong]
		cls._Uninitialize.restype = c_int32
		cls._UpdateDescriptor = dll['_PxL_4_1_UpdateDescriptor@12']
		cls._UpdateDescriptor.argtypes = [c_ulong,c_ulong,c_ulong]
		cls._UpdateDescriptor.restype = c_int32
		return object.__new__(cls)
	
	@classmethod
	def CameraRead(cls,*args):
		ret = cls._CameraRead(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def CameraWrite(cls,*args):
		ret = cls._CameraWrite(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def CreateDescriptor(cls,*args):
		ret = cls._CreateDescriptor(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def FormatClip(cls,*args):
		ret = cls._FormatClip(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def FormatImage(cls,*args):
		ret = cls._FormatImage(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def GetCameraFeatures(cls,*args):
		ret = cls._GetCameraFeatures(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def GetCameraInfo(cls,*args):
		ret = cls._GetCameraInfo(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def GetErrorReport(cls,*args):
		ret = cls._GetErrorReport(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def GetFeature(cls,*args):
		ret = cls._GetFeature(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def GetNextFrame(cls,*args):
		ret = cls._GetNextFrame(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def GetNumberCameras(cls,*args):
		ret = cls._GetNumberCameras(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def Initialize(cls,*args):
		ret = cls._Initialize(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def LoadSettings(cls,*args):
		ret = cls._LoadSettings(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def RemoveDescriptor(cls,*args):
		ret = cls._RemoveDescriptor(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def ResetPreviewWindow(cls,*args):
		ret = cls._ResetPreviewWindow(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def SaveSettings(cls,*args):
		ret = cls._SaveSettings(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def SetCameraName(cls,*args):
		ret = cls._SetCameraName(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def SetFeature(cls,*args):
		ret = cls._SetFeature(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def SetStreamState(cls,*args):
		ret = cls._SetStreamState(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def Uninitialize(cls,*args):
		ret = cls._Uninitialize(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
	@classmethod
	def UpdateDescriptor(cls,*args):
		ret = cls._UpdateDescriptor(*args)
		if not API_SUCCESS(ret):
			raise PixeLINKException(ret,args[0])
		return ret
