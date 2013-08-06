"""
"""
from ctypes import *
import numpy

from Generic import Generic, PixeLINKException, Types, Variables as V

# CONSTANTS
(FREE_RUNNING,SOFTWARE,HARDWARE) = (0,1,2)

class ArrayFromPointer(object):
    def __init__(self,**kw):
        pointer = kw.pop("pointer")
        template = numpy.zeros(**kw)
        a = self.__array_interface__ = template.__array_interface__.copy()
        a['data'] = (pointer,False)

def get_feature_flag_value(flag_name):
    return getattr(V,'FEATURE_FLAG_' + flag_name.upper())

class CameraFeatureDescMC(type):
    def __init__(cls,cls_name,bases,class_dict):
        # flags become properties
        def get_flag_method(flag_name):
            mask = get_feature_flag_value(flag_name)
            def method(self):
                return (self.flags & mask) != 0
            method.func_name = 'get_' + flag_name
            return method
        cls.flag_names = flag_names = ('off','onepush','read_only','auto','manual','desc_supported','presence')
        for flag_name in flag_names:
            method = get_flag_method(flag_name)
            setattr(cls,'get_'+flag_name,method)
            setattr(cls,flag_name,property(method))

class CameraFeatureDesc(object):
    __metaclass__ = CameraFeatureDescMC
    
    def __init__(self,name,id,flags,parms):
        self.name = name
        self.id = id
        self.flags = flags
        self.parms = parms
    def __str__(self):
        s = self.name + ":\n"
        s += "\tflags = %d\n" % self.flags
        for fname in self.flag_names:
            s += "\t  %s : %r\n" % (fname,getattr(self,fname))
        for (i,p) in enumerate(self.parms):
            s += "\t[%d] (min,max) = (%f,%f)\n" % (i,p[0],p[1])
        return s
    __repr__ = __str__

class CameraFeatureMC(type):
    def __init__(cls,cls_name,bases,class_dict):
        # flags become properties
        def get_flag_method(flag_name):
            mask = get_feature_flag_value(flag_name)
            def method(self):
                return (self.flags & mask) != 0
            method.func_name = 'get_' + flag_name
            return method
        cls.flag_names = flag_names = ('off','onepush','read_only','auto','manual','desc_supported','presence')
        for flag_name in flag_names:
            method = get_flag_method(flag_name)
            setattr(cls,'get_'+flag_name,method)
            setattr(cls,flag_name,property(method))

class CameraFeature(object):
    __metaclass__ = CameraFeatureMC
    
    def __init__(self,name,id,flags,parms):
        self.name = name
        self.id = id
        self.flags = flags
        self.parms = parms
    def __str__(self):
        s = self.name + ":\n"
        s += "\tflags = %d\n" % self.flags
        for fname in self.flag_names:
            s += "\t  %s : %r\n" % (fname,getattr(self,fname))
        for (i,p) in enumerate(self.parms):
            s += "\t[%d] => %f\n" % (i,p)
        return s
    __repr__ = __str__
# camera states
STARTED = 10
STOPPED = 20
PAUSED = 30

class PixeLINK(Generic):
    @classmethod
    def get_number_of_cameras(cls):
        n = Types.U32()
        serial_numbers = POINTER(Types.U32)()
        cls.GetNumberCameras(serial_numbers,n)
        return n.value

    @classmethod
    def get_serial_numbers(cls):
        n = Types.U32()
        serial_numbers = POINTER(Types.U32)()
        cls.GetNumberCameras(serial_numbers,n)
        serial_numbers_array_type = Types.U32*n.value
        serial_numbers_array = serial_numbers_array_type()
        cls.GetNumberCameras(serial_numbers_array,n)
        return list(serial_numbers_array)
    
    def __init__(self,index=0):
        """
        @param index: the camera index to use (start from 0)
        """
        Generic.__init__(self)
        serial_numbers = self.get_serial_numbers()
        self.__serial_number = sn = serial_numbers[index]
        print "PixeLINK camera sn = ",sn
        # initialize the camera
        self.initialize()
        self.__get_features_desc()
        # init ROI
        self.__roi = map(int,self.get_feature('roi').parms)
        self.__update_frame_buffer()
        self.stop()
        # self.__state= STOPPED

    def __del__(self):
        self.uninitialize()

    def initialize(self):
        handle = Types.HANDLE()
        p_handle = POINTER(Types.HANDLE)(handle)
        self.Initialize(self.__serial_number,p_handle)
        self.__handle = p_handle.contents
    
    def uninitialize(self):
        self.Uninitialize(self.__handle)

    def get_camera_info(self):
        if not hasattr(self,'camera_info'): 
            raw_CI = Types.CAMERA_INFO()
            self.GetCameraInfo(self.__handle,raw_CI)
            self.camera_info = CI = {}
            for (n,t) in Types.CAMERA_INFO._fields_:
                CI[n] = string_at(addressof(getattr(raw_CI,n)))
        return self.camera_info

    def get_features_desc(self):
        return self.__features_desc
    
    def get_feature_desc(self,name):
        return self.__features_desc[name.upper()]
    
    def get_feature(self,name):
        name = name.upper()
        if name == "LOOKUP_TABLE":
            return self.get_lookup_table()
        FD = self.get_feature_desc(name)
        flags = Types.U32()
        nparms = len(FD.parms)
        parms = (Types.float * nparms)()
        self.GetFeature(self.__handle,
                        Types.U32(FD.id),
                        flags,
                        Types.U32(nparms),
                        parms)
        
        return CameraFeature(name,FD.id,flags.value,list(parms))

    def get_lookup_table(self):
        """
        This is a special feature
        """
        fname = "LOOKUP_TABLE"
        FD = self.get_feature_desc(fname)
        size = int(FD.parms[0]['max'])
        flags = Types.U32()
        parms = (Types.float * size)()
        self.GetFeature(self.__handle,
                        Types.U32(FD.id),
                        flags,
                        Types.U32(size),
                        parms)
        
        return dict(flags=flags.value,
                    parms = list(parms))

    def get_bits_pp(self):
        """
        Return the number of bits per pixel
        """
        bpp_map = {V.PIXEL_FORMAT_MONO8 : 8,
                   V.PIXEL_FORMAT_MONO16 : 16}
        pixel_format = int(self.get_feature('pixel_format').parms[0])
        return bpp_map[pixel_format]
    bits_pp = property(get_bits_pp)
    
    def get_bytes_pp(self):
        bits_pp = self.bits_pp
        if bits_pp % 8 == 0:
            return int(bits_pp/8)
        else:
            return 1 + int(bits_pp/8)
    bytes_pp = property(get_bytes_pp)
    
    def get_roi(self):
        return self.__roi
    def set_roi(self,L,T,W,H):
        self.__set_feature('roi',parms=(L,T,W,H))
        self.__roi = (L,T,W,H)
        self.__update_frame_buffer()

    def get_gain(self):
        return self.get_feature('gain').parms[0]
    def set_gain(self,value):
        FD = self.get_feature_desc('gain')
        (m,M) = FD.parms[0]
        if value < m or value > M:
            raise Exception("Gain '%f' outside valid range [%f,%f]" % (value,m,M))
        self.__set_feature('gain',[value])

    def get_exposure_time(self):
        return self.get_feature('shutter').parms[0]

    def set_exposure_time_override(self,value):
        FD = self.get_feature_desc('shutter')
        (m,M) = FD.parms[0]
        if value < m or value > M:
            print "Exposure time '%f' outside valid range [%f,%f]" % (value,m,M)
            value = 0.00004
        self.__set_feature('shutter',[value])
        
    def set_exposure_time(self,value):
        FD = self.get_feature_desc('shutter')
        (m,M) = FD.parms[0]
        if value < m or value > M:
            raise Exception("Exposure time '%f' outside valid range [%f,%f]" % (value,m,M))
        self.__set_feature('shutter',[value])

    def get_trigger_type(self):
        return self.get_feature('trigger')
    
    def set_trigger_type(self,**kw):
        mode = kw.get('mode',0)
        type = kw['type']
        polarity = kw.get('polarity',1)
        delay = kw.get('delay',0)
        parm = kw.get('parameter',0)
        self.__set_feature('trigger',[mode,type,polarity,delay,parm])

    def set_external_trigger(self):
        self.set_trigger_type(mode = 0,polarity = 1,type = HARDWARE,delay =0)

    def start(self):
        state = V.START_STREAM
        self.SetStreamState(self.__handle,state)
        self.__state = STARTED

    def stop(self):
        state = V.STOP_STREAM
        self.SetStreamState(self.__handle,state)
        self.__state = STOPPED

    def pause(self):
        state = V.PAUSE_STREAM
        self.SetStreamState(self.__handle,state)
        self.__state = PAUSED

    def get_frame(self,copy=True,allow_interrupt=True):
        try:
            self.GetNextFrame(self.__handle,self.__frame_size,
                              self.__frame_buffer_pointer,self.__frame_desc)
        except PixeLINKException,E:
            if allow_interrupt and E.error_code == -2147483630:
                return
            else:
                raise

        FD = self.__frame_desc
        if copy:
            data = self.__frame_array.copy()
        else:
            data = self.__frame_array
        return dict(time = FD.fFrameTime,number=FD.uFrameNumber,data=data)

    def __get_features_desc(self):
        # find the feature names
        feature_names = [n[8:] for n in dir(V) if n.startswith('FEATURE_') and 
                         not n.startswith('FEATURE_FLAG') and not 
                         n in ('FEATURE_ALL',)]
        # map feature id to feature name
        self.__fid2fn = fid2fn = {}
        self.__fn2fid = fn2fid = {}
        for fn in feature_names:
            fid = getattr(V,'FEATURE_%s' % fn)
            fid2fn[fid] = fn
            fn2fid[fn] = fid
        
        # get all supported features
        buffer_size = Types.U32()
        self.GetCameraFeatures(self.__handle,V.FEATURE_ALL,None,buffer_size)
        p_camera_features = cast(create_string_buffer(buffer_size.value),
                                POINTER(Types.CAMERA_FEATURES))
        self.GetCameraFeatures(self.__handle,
                               V.FEATURE_ALL,
                               p_camera_features,
                               buffer_size)
        CFS = p_camera_features.contents
        self.__features_desc = features = {}
        for fid in range(CFS.uNumberOfFeatures):
            fname = fid2fn[fid]
            CF = CFS.pFeatures[fid]
            flags = CF.uFlags
            if not flags & V.FEATURE_FLAG_PRESENCE: continue
            parms = []
            for i in range(CF.uNumberOfParameters):
                P = CF.pParams[i]
                parms.append((P.fMinValue,P.fMaxValue))
            features[fname] = CameraFeatureDesc(fname,fid,flags,parms)

    def __set_feature(self,name,parms=[],flags=[]):
        fid = Types.U32(self.__fn2fid[name.upper()])
        flags_ = Types.U32(sum(map(get_feature_flag_value,flags)))
        nparms = len(parms)
        nparms_ = Types.U32(nparms)
        parms_ = (Types.F32*nparms)(*parms)
        self.SetFeature(self.__handle,fid,flags_,nparms_,parms_)

    def __update_frame_buffer(self):
        (L,T,W,H) = self.__roi
        bpp = self.bytes_pp
        if bpp == 1:
            dt = 'u1'
        elif bpp == 2:
            dt = 'u2'
        else:
            raise Exception("Unexpected bpp")
        self.__frame_array = a = numpy.zeros((H,W),dtype=dt)
        self.__frame_size = Types.U32(W*H*bpp)
        self.__frame_buffer_pointer = cast(a.__array_interface__['data'][0],c_void_p)       
        self.__frame_desc = Types.FRAME_DESC()
