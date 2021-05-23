import cv2
import numpy as np
import os
import threading
from color_detect import*
import time

'''
cap_W = 300
cap_H = 225
'''
# W 480 max 2CAMERA
cap_W = 480
cap_H = 270

cam_BDL_usb_path ='/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:{}:1.0-video-index0'\
                   .format('1.2.1')

cam_FUR_usb_path ='/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:{}:1.0-video-index0'\
                   .format('1.2.2')


def get_dev_videoX( path ):
    realpath = os.path.realpath( path )
    if not "/dev/video" in realpath:
        raise "Not a video device"
    print( realpath )
    if 'o' in realpath[-3] :
        devnum = int(realpath[-2])*10 + int(realpath[-1])
    else: devnum = int(realpath[-1])
    
    return devnum

vidcaps = [    cv2.VideoCapture( get_dev_videoX( cam_BDL_usb_path ) ),
               cv2.VideoCapture( get_dev_videoX( cam_FUR_usb_path ) ),
             
               ]

for vidcap in vidcaps:
    vidcap.set(3,cap_W)
    vidcap.set(4,cap_H)
    vidcap.set(cv2.CAP_PROP_FPS, 30)
    
 
def cap_img():
    cut = 25
    frames = []
    for vidcap in vidcaps :
        _,frame = vidcap.read()
        frame = frame[cut:cap_H-cut , cut:cap_W-cut ]#
        frames.append(frame)
   
    #frame_ALL= cv2.vconcat(frame[0],frame[0])
    frame_ALL= np.hstack( frames )
    
   
    #cv2.imshow('frame_ALL', frame_ALL)
    return frame_ALL


def release_all_cam():
    for vidcap in vidcaps:
        vidcap.release()
        cv2.destroyAllWindows()
    



class WebCamCapture:
    def __init__(self):
        self.Frame = cap_img()
        self.isstop = False
    
    def start(self):
    #print('cam started!')
        threading.Thread(target=self.queryframe).start()
        #threading.Thread(target=self.display_on_opencv_windows).start()
        
       
    def stop(self):
        self.isstop = True
        print('cam stopped!')
    
    def getframe(self):
        img,color1,color2 = circle_color(self.Frame)
        #return self.Frame
        return img
    def getcolor(self):
        img,color1,color2 = circle_color(self.Frame)
        return color1,color2
    def display_on_opencv_windows(self):
        
        while True:
            img = self.getframe()
            cv2.imshow('frame_ALL', img)
            if cv2.waitKey(1)== 27:
                release_all_cam()
                break
    def display(self):
        threading.Thread(target=self.display_on_opencv_windows).start()
    
    
    def queryframe(self):
        while (not self.isstop):
            self.Frame = cap_img()
        release_all_cam()




if __name__ == '__main__':

    webcam = WebCamCapture()
    webcam.start()
    
    #webcam.display_on_opencv_windows()
    def count_test():
        for i in range(1000):
            print(i)
            time.sleep(0.1)
    
    threading.Thread(target = count_test).start()
    webcam.display()
    '''
    while True:
        img = webcam.getframe()
        cv2.imshow('frame_ALL', img)
        if cv2.waitKey(1)== 27:
            release_all_cam()
            break
    '''



'''
if __name__ == '__main__':
    while True:
        img = cap_img()
        cv2.imshow('frame_ALL', img)
        if cv2.waitKey(1)== 27:
            release_all_cam()
            break
 '''       