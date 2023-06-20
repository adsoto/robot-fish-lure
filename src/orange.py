import numpy as np
import cv2
import os
from datetime import datetime
import controller
import matplotlib.pyplot as plt
import math

PIX2METERS = .635/820 # meters/pixels conversion TODO: automate this calculation in __init__
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

bg_model = cv2.createBackgroundSubtractorKNN(history = 800, dist2Threshold = 255.0, detectShadows = True) 


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

    def get_lure_thresh(self):
        ret, frame = self._cap.read()

        frame = cv2.undistort(frame, MTX, DIST, None, MTX)
        frame = frame[self._bounds[0][1]:self._bounds[1][1], self._bounds[0][0]:self._bounds[1][0]]
        self._current_frame = frame.copy()

        if (ret is None or frame is None): 
            print("frame has nothing")
            
            return  # if frame isn't valid, return
        
        
        ## Orange threshhlding for the robot to follow the orange dots

        lure_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_orange= np.array([0, 90, 100], dtype = "uint8") 
        upper_orange= np.array([200, 200, 255], dtype = "uint8")
    
        lure_mask=cv2.inRange(lure_hsv,lower_orange,upper_orange)

        kernellure = np.ones((2,2),np.uint8)

        orange_opening = cv2.morphologyEx(lure_mask, cv2.MORPH_OPEN, kernellure)
        lure_threshcopy = cv2.cvtColor(orange_opening, cv2.COLOR_BGR2RGB)
        
        cv2.imshow("orange thresh",lure_threshcopy)
       
        if self._save_video: self._out.write(frame)
        
        return lure_threshcopy


    def get_lure_contours(self, num_objects):
        """Finds the lure contours"""
        lure_thresh = self.get_lure_thresh()

        lure_cnts = cv2.findContours(lure_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        lure_cnts = lure_cnts[0] if len(lure_cnts) == 2 else lure_cnts[1]
        sorted_lure_cnts = sorted(lure_cnts, key=cv2.contourArea, reverse=True)
        return sorted_lure_cnts


    def get_lure_coords(self, num_objects):
        """Finds lure and returns its centroids in size order"""
        
        coords = np.zeros([num_objects, 2])
        cnts = self.get_lure_contours(num_objects)
        if len(cnts) < num_objects: return coords # if there aren't enough contours, return
        for i in range(0, num_objects):
            M = cv2.moments(cnts[i])
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else: cX, cY = 0, 0
            cv2.circle(self._current_frame, (cX, cY), int(5/(i+1)), (320, 159, 22), -1)
            coords[i,:] = np.array([cX, cY])
        coords[:,1] = self._height - coords[:,1] # move origin to lower left corner
        return coords*PIX2METERS

    def get_fish_thresh(self):
        ret, frame = self._cap.read()

        frame = cv2.undistort(frame, MTX, DIST, None, MTX)
        frame = frame[self._bounds[0][1]:self._bounds[1][1], self._bounds[0][0]:self._bounds[1][0]]
        self._current_frame = frame.copy()

        if (ret is None or frame is None): 
            print("frame has nothing")
            
            return  # if frame isn't valid, return
        ## Orange threshhlding for the robot to follow the orange dots

        kernelopen = np.ones((5,5),np.uint8)
        kernelclosed = np.ones((3,3),np.uint8)

        resultimage = np.zeros((800, 800))
        contrasted = cv2.normalize(frame, resultimage, -32, 255, cv2.NORM_MINMAX)
        fish_hsv = cv2.cvtColor(contrasted,cv2.COLOR_BGR2HSV)
        
        fish_lower = np.array([0,60,0], dtype = "uint8")
        fish_upper = np.array([24, 255, 145], dtype = "uint8")
        
        fish_mask = cv2.inRange(fish_hsv, fish_lower, fish_upper) # filters out black dots
        fish_mask_closing = cv2.morphologyEx(fish_mask, cv2.MORPH_CLOSE, kernelclosed)
        fish_mask_opening = cv2.morphologyEx(fish_mask_closing, cv2.MORPH_OPEN, kernelopen)
        fish_threshcopy = cv2.cvtColor(fish_mask_opening, cv2.COLOR_BGR2RGB)
        
        cv2.imshow('fish', fish_threshcopy)

        return fish_threshcopy

    def get_fish_contours(self, num_objects):
        fish_thresh = self.get_fish_thresh()

        fish_cnts, hierarchy = cv2.findContours(fish_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        fish_cnts = fish_cnts[0] if len(fish_cnts) == 2 else fish_cnts[1]
        sorted_fish_cnts = sorted(fish_cnts, key=cv2.contourArea, reverse=True)
        return sorted_fish_cnts

    def get_fish_coords(self, num_objects):
        """Finds fish and returns centroids in size order"""
        cnts = self.get_fish_contours(num_objects)
        coords = np.zeros([num_objects, 2])
        if len(cnts) < num_objects: return coords # if there aren't enough contours, return
        for i in range(0, num_objects):
            M = cv2.moments(cnts[i])
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else: cX, cY = 0, 0
            cv2.circle(self._current_frame, (cX, cY), int(5/(i+1)), (320, 159, 22), -1)
            coords[i,:] = np.array([cX, cY])
        coords[:,1] = self._height - coords[:,1] # move origin to lower left corner
        return coords*PIX2METERS

           
    def findClosestNeighbor(self):
        fishCoords = self.get_fish_coords
        lureContours = self.get_lure_contours
        lurePos = controller.robot_pos
        closestFish = fishCoords[0]
        minDist = math.dist(lurePos,closestFish)
        for fish in fishCoords:
            distance = math.dist(lurePos, fish)
            if (distance) < minDist:
                minDist = distance
                closestFish = fish
        print(closestFish)
        cv2.circle(lureContours, closestFish, 10, (255, 0, 255), -1)

    def displayWindows(self):
        #displays original video
        ret, frame = self._cap.read()

        cv2.namedWindow('fgframe', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('fgframe', 400, 400)
        cv2.imshow('fgframe', frame)
        
        sortedfishContours = self.get_fish_contours
        lureContours = self.get_lure_contours
        fish_thresh = self.get_fish_thresh()

        fishContours = cv2.drawContours(fish_thresh, sortedfishContours, -1, (0,255,0), 2) 

        if fishContours is not None:# or lureContours is not None:
            #allContours = cv2.add(fishContours, lureContours)
            #displays blobs
            cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Contours', 400, 400)
            cv2.imshow('Contours', fishContours)
        key = cv2.waitKey(0)
        if key & 0xFF == ord('g'):
            self._go = True
        elif key & 0xFF == ord('q'):
            self._go = False

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
    
    def display(self, target):
        """Shows live video feed, plotting dots on identified objects and the bot target"""

        if self._current_frame is not None:
            cv2.circle(self._current_frame, (int(target[0]/PIX2METERS), int(self._height-target[1]/PIX2METERS)), 5, (0, 159, 22), -1)
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
        vp.get_lure_coords(1)
        vp.display()
        if not vp.is_go(): break
    vp.cleanup()
