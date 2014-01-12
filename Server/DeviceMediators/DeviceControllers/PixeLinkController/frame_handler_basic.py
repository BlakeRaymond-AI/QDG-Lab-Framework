# -*- coding: utf-8 -*-
"""
frames_handler = FramesHandler().
This is a basic frames handler class to use with the pixelink camera.
What is this?
It is whatever you want....
When the pixelink start() method is called it must be given a an object, 'A' say, that has an
"add_frame(frame)" method, A.add_frame(frame), and a number of frames to wait for.
The start method starts a separate thread that just waits for frames to appear from the camera,
and then passes them to the Frame_Handler, 'A' in this case, via A.add_frame(frame), where 
frame is a dictionary with (time,number,data) fields.
The object can do whatever it wants with the frame.  This version appends the frame to a list
of frames, the normal function we want.
-- It also has a 'generate frames array' which pulls out just the pixel data and converts it 
to a numpy array for ease of processing
-- A save_frames method which saves all the frames to the data folder if given (default 
to current directory) in the form 'datafolder/images_timestamp/frame_n.png' where n is the frame number.
-- this has an optional data argument which could be passed to it and used for various
custom methods
One can either make a custom subclass of this containing processing methods or just use
it to get the frames and process them with the calling script or something else.
"""
import os.path

pjoin = os.path.join
import time
import numpy
from PIL import Image


class FramesHandler(object):
    def __init__(self, data=None, folder='', time_stamp=None):
        if not time_stamp:
            self.time_stamp = time.strftime("%y%m%d_%H%M%S")
        else:
            self.time_stamp = time_stamp
        self.__data = data
        self.__frames = []
        if folder:
            self.set_datafolder(folder)

    def add_frame(self, frame):
        self.__frames.append(frame)
        #print "Add frame %d" % len(self.__frames)

    def generate_frames_array(self, float=True):
        self.frames_array = []
        for frame in self.__frames:
            img_array = numpy.array(frame['data'])
            if float:
                self.frames_array.append(img_array.astype('float'))
            else:
                self.frames_array.append(img_array)
        return self.frames_array

    def get_datafolder(self):
        return self.__datafolder

    def set_datafolder(self, folder):
        if os.path.isdir(folder):
            self.__datafolder = folder
        else:
            print "folder %s doesn't exist.  Writing to %s" % (folder, self.__datafolder)
            raise Exception(), "Folder '%s' doesn't exit" % folder

    def save_frames(self, folder=None, filenamebase=None, filenames=None, data=True, suffix=''):
        if data:
            subfolder = 'pixelink_image_data' + suffix
        else:
            subfolder = 'pixelink_images' + suffix
        if filenames:
            if len(filenames) < self.N:
                filenames = None
                print 'there were not enough filenames; using default names'
            #get datafolder
        if folder is None:
            d = self.__datafolder
        else:
            if os.path.isdir(folder):
                d = folder
            else:
                print "folder %s doesn't exist.  Writing to %s" % (folder, self.__data_folder)
                d = self.__datafolder
            #get frames and make image data folder
        self.generate_frames_array(float=False)
        print "Saving %d images" % len(self.frames_array)
        frames_folder = pjoin(d, subfolder)
        if not os.path.isdir(frames_folder):
            os.makedirs(frames_folder)
            #write data to files
        for (i, frame) in enumerate(self.frames_array):
            if filenamebase:
                fname = filenamebase % i
            if filenames:
                fname = filenames[i]
            else:
                if data:
                    fname = 'imagedata_%06d' % i
                else:
                    fname = 'image_%06d' % i
            if data:
                (w, h) = frame.shape
                fpath = pjoin(frames_folder, (fname + "_%04dx%04d.txt") % (w, h))
                numpy.savetxt(fpath, frame, fmt='%d', delimiter=',')
                print 'IMAGE DATA FILE NAME IS ', fpath
            else:
                fpath = pjoin(frames_folder, fname + '.png')
                self.__save_frame(frame, fname=fpath)
                print 'IMAGE FILE NAME IS ', fpath
        self.frames_folder = frames_folder

    def __save_frame(self, data, fname):
        img = Image.fromarray(data)
        img.save(fname)
        print "wrote the image ", time.time()

 