import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import datetime
import os
from tracker import *
import convert as c
import setupcontrol as sc
import lure as lure
import object_state

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

bg_model = cv2.createBackgroundSubtractorKNN(history = 800, dist2Threshold = 255.0, detectShadows = False) 

hsvRanges = []


class centroidTracker:

    def __init__(self, camera_port, background_path, camera_bounds, save_video):
        self._cap = cv2.VideoCapture(camera_port)
        #bf = cv2.imread(background_path, cv2.IMREAD_COLOR)

        self._backframe = cv2.imread(background_path, cv2.IMREAD_COLOR)
        self._lure = lure.VideoProcessor(camera_port, camera_bounds, save_video)
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

    def show_frame(self): #helps with debugging
        ret, frame = self._cap.read()

        if (not ret): 
            print("frame has nothing")
            exit(0)
                
        self._current_frame = frame.copy()

        cv2.imshow("frame", frame)
        cv2.waitKey(30)

    def get_fish_thresh(self):
        ret, frame = self._cap.read()
        backframe = self._backframe

        if (not ret): 
            print("frame has nothing")
            exit(0)

        frame = cv2.undistort(frame, MTX, DIST, None, MTX)
        backframe = cv2.undistort(backframe, MTX, DIST, None, MTX)
        frame = frame[self._bounds[0][1]:self._bounds[1][1], self._bounds[0][0]:self._bounds[1][0]]
        backframe = backframe[self._bounds[0][1]:self._bounds[1][1], self._bounds[0][0]:self._bounds[1][0]]

        self._current_frame = frame.copy()
        ## puts the fish into a color mask ##
        fish_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        

        if sc.setup == "KECK":
            #manual backsub, HSV -> morphs

            # inv_frame = cv2.bitwise_not(frame)
            # inv_backframe = cv2.bitwise_not(backframe)
            # backsub = cv2.add(inv_frame,inv_backframe)



            fish_kernel_open = np.ones((3,3),np.uint8)    
            fish_kernel_closed = np.ones((5,5),np.uint8)

            fish_lower = np.array([0,35,0], dtype = "uint8")
            fish_upper = np.array([25,255,230], dtype = "uint8")
            
            colorfish = cv2.inRange(fish_hsv, fish_lower, fish_upper)
            fish_mask_opening = cv2.morphologyEx(colorfish, cv2.MORPH_OPEN, fish_kernel_open)
            fish_mask_opening2 = cv2.morphologyEx(fish_mask_opening, cv2.MORPH_OPEN, fish_kernel_open)
            fish_mask_closing = cv2.morphologyEx(fish_mask_opening2, cv2.MORPH_CLOSE, fish_kernel_closed)

            dilation = cv2.dilate(fish_mask_opening2, fish_kernel_open, iterations= 1)


            #colorfish = cv2.cvtColor(colorfish, cv2.COLOR_GRAY2BGR)
            backframe = cv2.cvtColor(backframe, cv2.COLOR_BGR2GRAY)

            inv_thresh = cv2.bitwise_not(fish_mask_closing)
            ret, bgthresh = cv2.threshold(backframe, 215, 255, cv2.THRESH_BINARY)
            inv_bg = cv2.bitwise_not(bgthresh)
            backsub = cv2.bitwise_not(cv2.add(inv_thresh, inv_bg))

            fish_cnts, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            sortedfishContours = sorted(fish_cnts, key=cv2.contourArea, reverse=True)
            
            fishCount = len(sortedfishContours)

            # if fishCount > 10:
            #     print ("fish breaking up: ", fishCount)
            # if fishCount > 10:
            #     print ("fish out of frame or blending together: ", fishCount)


            cv2.imshow("frame", frame)
            cv2.imshow("bg", fish_mask_closing)
            cv2.waitKey(1)
    
            return dilation

        if sc.setup == "LAIR":
            fishkernel = np.ones((5,5),np.uint8)
            
            fish_lower = np.array([10,40,80], dtype = "uint8")
            fish_upper = np.array([50,120,220], dtype = "uint8")

            fish_mask = cv2.inRange(fish_hsv, fish_lower, fish_upper)

            fish_mask_closing = cv2.morphologyEx(fish_mask, cv2.MORPH_CLOSE, fishkernel)
            fish_mask_opening = cv2.morphologyEx(fish_mask_closing, cv2.MORPH_OPEN, fishkernel)

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


    def get_fish_coords_id(self, fish_id):
        """Finds fish and returns centroids in size order"""
        fishCoords = []
        #print("start")
        cnts = self.get_fish_contours()
        #print(len(cnts))
        #coords = np.zeros([num_objects, 2])
        if (len(cnts)) < fish_id: return fishCoords # if there aren't enough contours, return

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
            id, x, y, w, h = box_id
            
            cv2.putText(self._current_frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            cv2.rectangle(self._current_frame, (x, y), (x + w, y + h), (0, 255, 0), 3) # draws rectangle aroudn contours
            cv2.imshow("frame", self._current_frame)
            cv2.waitKey(1)
            fishCoords.append(box_id)
        for coord in fishCoords:
            if fish_id == 0:
                print (fishCoords)
                return fishCoords
            if coord[0] == fish_id:
                print (coord)
                return coord
            else:
                print("fish out of frame")
    
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

            fishCoords.append([fcX, fcY])

        return fishCoords
           
    def findClosestNeighbor(self):
        ret, frame = self._cap.read()
        fishCoords = self.get_fish_coords()

        [head, tail] = self._lure.get_coords(2)
        headX, headY = head[0], head[1]
        tailX, tailY = tail[0], tail[1]
        lurePos = [((headX + tailX)/2), ((headY + tailY)/2)]

        # PIX to METER CONVERSIONS #
        for f in fishCoords:
            f[0] = c.xpxtomet(int(f[0]))
            f[1] = c.ypxtomet(int(f[1]))

        lurePos[0] = c.xpxtomet(int(lurePos[0]))
        lurePos[1] = c.ypxtomet(int(lurePos[1]))

        
        if fishCoords is not None:
            closestFish = fishCoords[0]
            minDist = math.dist(lurePos,closestFish)
            for fish in fishCoords:
                distance = math.dist(lurePos, fish)
                if (distance) < minDist:
                    minDist = distance
                    closestFish = fish # [x,y] coords
            closestFishCoords = (closestFish[0], closestFish[1])
            #cv2.circle(self._current_frame, closestFishCoords, 3, [255,0,0])

            return minDist
        
    def get_closest_fish_state(self, t):

        fish_pos = self.findClosestNeighbor()

        if fish_pos:
            closest_fish_state = object_state.Object(t, fish_pos[0], fish_pos[1], 0) #theta is 0 for now?? how to calculate this? same as lure?
            return closest_fish_state


    def is_go(self):
        return self._go

    def cleanup(self):
        self._cap
        if self._save_video:
            self._out.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    camera_index = 0
    foregroundpath = r"C:\Users\ginar\OneDrive\Documents\robot-fish-lure-code-refactor\videos\use_for_velocities.avi"
    backgroundPath = r"C:\Users\ginar\OneDrive\Documents\robot-fish-lure-code-refactor\videos\background2.png"
    camera_bounds = np.array([[575, 300], [1445, 825]]) # find these with calibrate_setup.pyq
    ct = centroidTracker(foregroundpath, backgroundPath, camera_bounds, False)
    while True:
        ct.get_fish_thresh()
        if not ct.is_go(): break

    ct.cleanup()
