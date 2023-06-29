"""angelinas background subtraction / blob analysis"""
import cv2
import numpy as np
import matplotlib as mp
import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import datetime
import os
from tracker import *

PIX2METERS = .635/820 # meters/pixels conversion
FPS = 10

# MTX and DIST are properties of the camera (have to do with fisheye lens)
MTX = np.array([[1.05663779e+03, 0.00000000e+00, 9.73055094e+02],
 [0.00000000e+00, 1.05269643e+03, 5.64799418e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
DIST = np.array([-3.80359934e-01,  1.49531854e-01,  2.50649988e-05,  8.39488578e-05,  -2.83529982e-02])

LxPos = []
LyPos = []

FxPos = []
FyPos = []

fishTracker = EuclideanDistTracker()
lureTracker = EuclideanDistTracker()

bg_model = cv2.createBackgroundSubtractorKNN(history = 800, dist2Threshold = 255.0, detectShadows = True) 



class centroidTracker:

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

    def get_lure_thresh(self):
        ret, frame = self._cap.read()

        #frame = cv2.undistort(frame, MTX, DIST, None, MTX)
        #frame = frame[self._bounds[0][1]:self._bounds[1][1], self._bounds[0][0]:self._bounds[1][0]]

        if (ret is None or frame is None): 
            print("frame has nothing")
            exit(0)
        
        self._current_frame = frame.copy()
        ## Orange threshhlding for the robot to follow the orange dots

        lure_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_orange= np.array([0, 70, 200], dtype = "uint8") 
        upper_orange= np.array([250, 210, 255], dtype = "uint8")
    
        lure_mask=cv2.inRange(lure_hsv,lower_orange,upper_orange)
        kernellure = np.ones((10,10),np.uint8)
        orange_closing = cv2.morphologyEx(lure_mask, cv2.MORPH_CLOSE, kernellure)
        orange_dilation = cv2.dilate(orange_closing, None, 1)
        return orange_dilation


    def get_lure_contours(self, num_objects):
        """Finds the lure and returns centroids in size order"""
        lure_thresh = self.get_lure_thresh()

        if (lure_thresh is None):
            print("no lure")
            exit(0)

        lure_cnts = cv2.findContours(lure_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        lure_cnts = lure_cnts[0] if len(lure_cnts) == 2 else lure_cnts[1]
        sorted_lure_cnts = sorted(lure_cnts, key=cv2.contourArea, reverse=True)
        if num_objects == 0:
            return sorted_lure_cnts
        else:
            return sorted_lure_cnts[0:num_objects]


    def get_lure_coords(self, numObj):
        lureCoords = []
        cnts = self.get_lure_contours(numObj)
        if len(cnts) == 0: return lureCoords # if there aren't enough contours, return
        for f in cnts:
            LM = cv2.moments(f)
            if LM["m00"] != 0:
                lcX = int(LM["m10"] / LM["m00"])
                lcY = int(LM["m01"] / LM["m00"])
            else: 
                lcX, lcY = 0, 0
            lureCoords.append([lcX, lcY])

        return lureCoords

    def get_fish_thresh(self):
        ret, frame = self._cap.read()

        #frame = cv2.undistort(frame, MTX, DIST, None, MTX)
        #frame = frame[self._bounds[0][1]:self._bounds[1][1], self._bounds[0][0]:self._bounds[1][0]]

        if (ret is None or frame is None): 
            print("frame has nothing")
            exit(0)
        
        self._current_frame = frame.copy()
        ## Orange threshhlding for the robot to follow the orange dots

        kernelopen = np.ones((5,5),np.uint8)
        kernelclosed = np.ones((5,5),np.uint8)

        resultimage = np.zeros((800, 800))
        contrasted = cv2.normalize(frame, resultimage, -32, 255, cv2.NORM_MINMAX)
        fish_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        
        fish_lower = np.array([7,44,140], dtype = "uint8")
        fish_upper = np.array([15,100,220], dtype = "uint8")
        
        fish_mask = cv2.inRange(fish_hsv, fish_lower, fish_upper) # filters out black dots
        
        fish_kernel_open = np.ones((6,6),np.uint8)
        fish_kernel_closed = np.ones((4,4),np.uint8)

        fish_mask_closing = cv2.morphologyEx(fish_mask, cv2.MORPH_CLOSE, fish_kernel_closed)
        fish_mask_closing2 = cv2.morphologyEx(fish_mask_closing, cv2.MORPH_CLOSE, fish_kernel_closed)
        fish_mask_opening = cv2.morphologyEx(fish_mask_closing2, cv2.MORPH_OPEN, fish_kernel_open)
        
        return fish_mask_opening

    def get_fish_contours(self):
        fish_thresh = self.get_fish_thresh()

        if (fish_thresh is None): 
            print("no thresh")
            exit(0)  # if frame isn't valid, return

        fish_cnts, hierarchy = cv2.findContours(fish_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #fish_cnts = fish_cnts[0] if len(fish_cnts) == 2 else fish_cnts[1]
        sortedfishContours = sorted(fish_cnts, key=cv2.contourArea, reverse=True)
        fishContours = cv2.drawContours(self._current_frame, sortedfishContours, -1, (0,255,0), 2) 
        return sortedfishContours


    def get_fish_coords_id(self, num_objects):
        """Finds fish and returns centroids in size order"""
        fishCoords = []
        print("start")
        cnts = self.get_fish_contours()[0:num_objects]
        #coords = np.zeros([num_objects, 2])
        if (len(cnts)) < num_objects: return fishCoords # if there aren't enough contours, return

        fishdetections = []
        for cnt in cnts:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 5:
                #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                fishdetections.append([x, y, w, h])

        
        fish_boxes_ids = fishTracker.update(fishdetections) # contains fish identifications
        for box_id in fish_boxes_ids:
            x, y, w, h, id = box_id
            
            cv2.putText(self._current_frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            cv2.rectangle(self._current_frame, (x, y), (x + w, y + h), (0, 255, 0), 3) # draws rectangle aroudn contours
            print(box_id)

        return fish_boxes_ids
    
    def get_fish_coords(self):
        """Finds fish and returns centroids in size order"""
        fishCoords = []
        cnts = self.get_fish_contours()
        #coords = np.zeros([num_objects, 2])
        if (len(cnts)) == 0 : return fishCoords # if there aren't enough contours, return
        for f in cnts:
            FM = cv2.moments(f)
            if FM["m00"] != 0:
                fcX = int(FM["m10"] / FM["m00"])
                fcY = int(FM["m01"] / FM["m00"])
                
            else: 
                fcX, fcY = 0, 0
            #print(str(fcX))
            #cv2.circle(self._current_frame, (fcX, fcY), 3, (320, 159, 22), -1)
            fishCoords.append([fcX, fcY])
            #FxPos += [fcX]
            #FyPos += [fcY]
            #print(fishCoords)
        #fishCoords[:,1] = self._height - fishCoords[:,1] # move origin to lower left corner
        #print(fishCoords)
        return fishCoords

     
           
    def findClosestNeighbor(self):
        fishCoords = self.get_fish_coords()

        [head, tail] = self.get_lure_coords(2)
        headX, headY = head[0], head[1]
        tailX, tailY = tail[0], tail[1]
        lurePos = [((headX + tailX)/2), ((headY + tailY)/2)]
        #cv2.circle(self._current_frame, lurePos, 10, (0, 0, 255), -1)
        if fishCoords is not None:
            #print(lurePos)
            closestFish = fishCoords[0]
            minDist = math.dist(lurePos,closestFish)
            for fish in fishCoords:
                distance = math.dist(lurePos, fish)
                if (distance) < minDist:
                    minDist = distance
                    closestFish = fish
            return 
        # cv2.circle(self._current_frame, closestFish, 10, (255, 0, 255), -1)
        # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('frame', 400, 400)
        # cv2.imshow("frame", self._current_frame)
        # cv2.waitKey(0)
        

    def displayWindows(self):
        #displays original video
        ret, frame = self._cap.read()
        self._current_frame = frame.copy()
        if self._current_frame is not None:
            cv2.namedWindow('fgframe', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('fgframe', 400, 400)
            cv2.imshow('fgframe', frame)
            cv2.waitKey(0)
        
        # sortedfishContours = self.get_fish_contours
        # lureContours = self.get_lure_contours
        # fish_thresh = self.get_fish_thresh()

        # fishContours = cv2.drawContours(fish_thresh, sortedfishContours, -1, (0,255,0), 2) 

        # if fishContours is not None:# or lureContours is not None:
        #     #allContours = cv2.add(fishContours, lureContours)
        #     #displays blobs
        #     cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
        #     cv2.resizeWindow('Contours', 400, 400)
        #     cv2.imshow('Contours', fishContours)
        # key = cv2.waitKey(0)
        # if key & 0xFF == ord('g'):
        #     self._go = True
        # elif key & 0xFF == ord('q'):
        #     self._go = False

    def displayPlots():
        bgforgraph = bg_model.getBackgroundImage()
        RGB_img = cv2.cvtColor(bgforgraph, cv2.COLOR_BGR2RGB)

        fig, ax1 = plt.subplots()
        im1 = ax1.imshow(bgforgraph)
        ax1.plot(FxPos, FyPos, '*', linewidth=2.0)
        plt.title('Fish Trajectory')
        plt.ylabel('yPred (pixels)')
        plt.xlabel('xPred (pixels)')
        plt.savefig('fish_trajectory.png')
        plt.show()

        fig, ax2 = plt.subplots()
        im2 = ax2.imshow(bgforgraph)
        ax2.plot(LxPos, LyPos, '*', linewidth=2.0)

        plt.title('Lure Trajectory')
        plt.ylabel('yPred (pixels)')
        plt.xlabel('xPred (pixels)')

        plt.savefig('lure_trajectory.png')

        plt.show()

    def is_go(self):
        return self._go

    def cleanup(self):
        self._cap
        if self._save_video:
            self._out.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    camera_index = 0
    foregroundPath = r"C:\Users\ginar\Documents\robot-fish-lure\videos\lureMoving.mp4"
    #cap = cv2.VideoCapture(foregroundPath)
    #ret, frame = cap.read()
    camera_bounds = np.array([[467, 382], [1290, 862]]) # find these with calibrate_setup.py
    ct = centroidTracker(foregroundPath, camera_bounds, True)
    while True:
        #ct.get_coords(1)
        #ct.displayWindows()
        ct.findClosestNeighbor()
        if not ct.is_go(): break
    ct.cleanup()