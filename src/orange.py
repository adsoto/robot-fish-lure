import numpy as np
import cv2
import os
from datetime import datetime
from controller import setup
import convert

#X DIR CONVERSTIONS
xoff = 574
xslope = 1151

#Y DIR CONVERSIONS
yoff = 762
yslope = (-1156)
PIX2METERS = 0.653/820

"""
OLD global conversion:
0.653 overshoots the trajectory by roughly 1cm, which can be concluded as error
0.635 was declans original calibration constant (which underperformed by 2cm)
"""

FPS = 10

# MTX and DIST are properties of the camera (have to do with fisheye lens)
MTX = np.array([[1.05663779e+03, 0.00000000e+00, 9.73055094e+02],
 [0.00000000e+00, 1.05269643e+03, 5.64799418e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
DIST = np.array([-3.80359934e-01,  1.49531854e-01,  2.50649988e-05,  8.39488578e-05,  -2.83529982e-02])

class VideoProcessor:
    """Class to handle video processing, displaying, CV, etc."""

    def __init__(self, camera_port, camera_bounds, save_video):
        self._cap = cv2.VideoCapture(camera_port)
        self._save_video = save_video
        self._height = camera_bounds[1,1]-camera_bounds[0,1]
        self._go = True # not implemented
        self._current_frame = None
        self._bounds = camera_bounds
        
        if save_video == True: # not tested            
            size = np.diff(camera_bounds, axis=0)
            now = str(datetime.now())
            filename = str(now[0:19])
            daymonthyear = datetime.now()
            date = str(daymonthyear)
            display = date[:10]

            video_folder = 'data/' + display
            video_filename = 'data/' + filename + '.avi'
 
            #result = cv2.VideoWriter(video_filename +".avi",cv2.VideoWriter_fourcc(*'MJPG'),FPS, (size[0][0],size[0][1]))
            if not os.path.exists(video_folder):
                os.makedirs(video_folder)
            
            self._out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'MJPG'), FPS, (size[0][0],size[0][1]))

    def get_coords(self, num_objects):
        """Finds the n largest dark objects and returns their centroids in order"""

        coords = np.zeros([num_objects, 2])
        ret, frame = self._cap.read()

        frame = cv2.undistort(frame, MTX, DIST, None, MTX)
        frame = frame[self._bounds[0][1]:self._bounds[1][1], self._bounds[0][0]:self._bounds[1][0]]
        self._current_frame = frame.copy()

        if (ret is None or frame is None): return coords # if frame isn't valid, return

        ## Orange threshhlding for the robot to follow the orange dots
        into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_orange= np.array([0, 100, 50], dtype = "uint8")
        upper_orange= np.array([10, 200, 255], dtype = "uint8")
        b_mask=cv2.inRange(into_hsv,lower_orange,upper_orange)
        orange=cv2.bitwise_and(frame,frame,mask=b_mask)
        ret,thresh_img = cv2.threshold(orange, 90, 255, cv2.THRESH_BINARY) #converts the greyscale orange mask to binary
        greybin = cv2.cvtColor(thresh_img, cv2.COLOR_RGB2GRAY)
        ret, bwthresh= cv2.threshold(greybin, 10, 255, cv2.THRESH_BINARY) #converts the greyscale orange mask to binary

        # cv2.imshow("orange thresh",thresh_img)       # for debugging!
        # cv2.imshow("blackwhite thresh", bwthresh)    # for debugging!
        
        if self._save_video: self._out.write(frame)

        cnts = cv2.findContours(bwthresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        if len(cnts) < num_objects: return coords # if there aren't enough contours, return
        
        for i in range(0, num_objects):
            M = cv2.moments(cnts[i])
            if M["m00"] != 0:
                cX_px = int(M["m10"] / M["m00"]) #in pixels
                cY_px = int(M["m01"] / M["m00"]) #in pixels
                cX_met = convert.xpxtomet(cX_px) #in meters
                cY_met = convert.ypxtomet(cY_px) #in meters

            else: cX_px, cY_px = 0, 0 #pixels

            cv2.circle(self._current_frame, (cX_px, cY_px), int(5/(i+1)), (320, 159, 22), -1) ##orange circle -- plots circles in pixels
            coords[i,:] = np.array([cX_met, cY_met]) #appends meter coords to the array "coords"

        return coords ##IN METERS!
    
    def display(self, target, pathinmeters):
        """Shows live video feed, plotting dots on identified objects and the bot target"""

        if self._current_frame is not None:

            if pathinmeters == True: #converts a meter path to px for graping
                xtarget_px = convert.xmettopx(target[0]) 
                ytarget_px = convert.ymettopx(target[1])
                frameheight = int(self._bounds[1][1] - self._bounds[0][1])
              
                if setup =="LAIR":
                    cv2.circle(self._current_frame, (int(xtarget_px), int(ytarget_px)), 5, (0, 159, 22), -1)
                    # green dot for target path
                    print("meters path")

                if setup =="KECK":
                    cv2.circle(self._current_frame, (int(xtarget_px), int(ytarget_px -160 )), 5, (0, 159, 22), -1)
                    # green dot for target path
                    print("meters path")

            if pathinmeters == False:  #graphs target in px
                xtarget_met = convert.xpxtomet(target[0]) #path target in meters
                ytarget_met = convert.ypxtomet(target[1]) #path target in meters
                cv2.circle(self._current_frame, (int(target[0]/PIX2METERS), int(self._height-target[1]/PIX2METERS)), 5, (0, 159, 22), -1)
                #green dot for target path    
                print("pixels path")    

            cv2.namedWindow("output", cv2.WINDOW_NORMAL)
            resized = cv2.resize(self._current_frame, (960, 540))
            cv2.imshow('frame', resized)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('g'):
                self._go = True
            elif key & 0xFF == ord('q'):
                self._go = False

    def is_go(self):
        return self._go

    def cleanup(self):
        self._cap
        if self._save_video:
            self._out.release()
        cv2.destroyAllWindows()
    
if __name__ == '__main__':
    camera_index = 0
    
    camera_bounds = np.array([[467, 382], [1290, 862]]) # find these with calibrate_setup.py
    vp = VideoProcessor(camera_index, camera_bounds, True)
    while True:
        vp.get_coords(1)
        vp.display()
        if not vp.is_go(): break
    vp.cleanup()