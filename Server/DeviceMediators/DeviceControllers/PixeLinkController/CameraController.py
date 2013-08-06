from ctypes import *
from threading import Thread, Event
from PixeLINK import PixeLINK, FREE_RUNNING, SOFTWARE,HARDWARE

"""
How to use the camera controller:
You create a camera controller object in your script (call it C for now).
with this you can set all the camera properties given as methods below.
to start snapping frames you call C.start(number_of _frames, frames_handler)
this will start a thread which starts the camera driver and watches for 'number_of_frames' frames to arrive
(how they are taken depends on how you set it up -- usually we use external triggers)
at each frame arrival it called the frames_handler.add_frame(frame) method.  

frames_handler can be any class.  you can make as many as you want to do anything
you want but it must have an 'add_frame(frame)' method, that accepts the pixelink frame format.

you can stop the camera before it recieves all the frames, but otherwise it will either keep waiting 
or stop itself when it recieves all the frames it was supposed to.
"""
class CameraController(object):
    def __init__(self):
        self.__driver = PixeLINK()
        self.__running = False
        self.__must_stop = False
        self.failed = False
        self.__first_frame_captured = Event()
        self.__acquisition_stopped = Event()
    
    def get_trigger_type(self):
        return self.__driver.get_trigger_type()
    def set_trigger_type(self,**kw):
        self.__driver.set_trigger_type(**kw)
    def set_external_trigger(self):
        self.__driver.set_external_trigger()
        
    def set_roi(self,*roi):
        self.__driver.set_roi(*roi)
    def get_roi(self):
        return self.__driver.get_roi()

    def set_exposure_time_ms(self,ms):
        self.__driver.set_exposure_time(ms/1000.0)
    def get_exposure_time_ms(self):
        return 1000*self.__driver.get_exposure_time()

    def set_gain(self,db):
        self.__driver.set_gain(db)
    def get_gain(self):
        return self.__driver.get_gain()

    @property
    def driver(self):
        return self.__driver

    def __frame_grabber(self,nr_frames,frames_handler):
        D = self.__driver
        D.start()
        self.__first_frame_captured.clear()
        self.__acquisition_stopped.clear()
        interrupted = False
        self.__running = True
        for i in range(nr_frames):
            try:
           	    frame = D.get_frame(copy=True,allow_interrupt=True)
           	except PixeLINKException as e:
           		self.failed = True
				raise e           	
            if self.__must_stop: 
                interrupted = True
                break            
            frames_handler.add_frame(frame)
            if i == 0: self.__first_frame_captured.set()
        self.__running = False
        self.__acquisition_stopped.set()
        # stop it only if the camera wasn't interrupted
        if not interrupted:
            D.stop()

    def wait_first_frame(self):
        self.__first_frame_captured.wait()
        return 1

    def start(self,nr_frames,frames_handler):
        self.__must_stop = False
        self.T = T = Thread(target = self.__frame_grabber,args = (nr_frames,frames_handler))
        T.start()

    def stop(self):
        if self.__running: 
            self.__must_stop = True
            self.__driver.stop()
            self.__acquisition_stopped.wait()
