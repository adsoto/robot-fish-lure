"""angelinas background subtraction / blob analysis"""
import cv2
import numpy as np
import matplotlib as mp
import pandas as pd
import matplotlib.pyplot as plt
from datetime import *

# Initialize variable to break while loop when last frame is achieved
last = 0

LxPos = []
LyPos = []

FxPos = []
FyPos = []

thresh = 100
fishContourIndex = 0
lureContourIndex = 0

MTX = np.array([[1.05663779e+03, 0.00000000e+00, 9.73055094e+02],
 [0.00000000e+00, 1.05269643e+03, 5.64799418e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
DIST = np.array([-3.80359934e-01,  1.49531854e-01,  2.50649988e-05,  8.39488578e-05,  -2.83529982e-02])

bg_model = cv2.createBackgroundSubtractorKNN(history = 800, dist2Threshold = 255.0, detectShadows = True) 

foregroundCapture = cv2.VideoCapture(0)
ret_init, frame_init_ = foregroundCapture.read()

#getting resolutions 
frame_width = int(foregroundCapture.get(3))
frame_height = int(foregroundCapture.get(4))

print("height:",frame_height)
print("width:",frame_width)

# generates date and time info for the video filename
size = (frame_width, frame_height)
now = str(datetime.now())
filename = str(now[0:19])

# writes video to save -- filename, fourcc, framerate, size of video 
result = cv2.VideoWriter(filename +".avi",cv2.VideoWriter_fourcc(*'MJPG'), 30, size)

# foregroundCapture.set(cv2.CAP_PROP_POS_FRAMES, 0)
if not foregroundCapture.isOpened():
    print('Unable to open')
    exit(0)

while True:

    ret, frame = foregroundCapture.read()
    #qframe = cv2.undistort(frame, MTX, DIST, None, MTX)
    #frame = frame[382:862, 467:1290]
    

    if not ret:
        break

    this_frame = foregroundCapture.get(1)

    if ret:
        bg = bg_model.apply(frame_init_)
        kernellure = np.ones((2,2),np.uint8)
        kernelopen = np.ones((5,5),np.uint8)
        kernelclosed = np.ones((3,3),np.uint8)

        ############ ORANGE TRACKING #############

        lure_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_orange= np.array([0, 90, 100], dtype = "uint8") 
        upper_orange= np.array([200, 200, 255], dtype = "uint8")
    
        lure_mask=cv2.inRange(lure_hsv,lower_orange,upper_orange)

        orange_closing = cv2.morphologyEx(lure_mask, cv2.MORPH_CLOSE, kernellure)
        orange_opening = cv2.morphologyEx(lure_mask, cv2.MORPH_OPEN, kernellure)
        
        lure_contours, hierarchy = cv2.findContours(orange_opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #finds the contours in thresh_img
        lure_threshcopy = cv2.cvtColor(orange_opening, cv2.COLOR_BGR2RGB) #needs to be in RBG in order to make contours colorful
        lureContours = cv2.drawContours(lure_threshcopy, lure_contours, -1, (255,165,0), 2) 
        sorted_lure_contours = sorted(lure_contours, key = cv2.contourArea, reverse = True)

        ############# TRACK FISH W/ HSV ###############

        resultimage = np.zeros((800, 800))
        contrasted = cv2.normalize(frame, resultimage, -32, 255, cv2.NORM_MINMAX)
        fish_hsv = cv2.cvtColor(contrasted,cv2.COLOR_BGR2HSV)
        

        #fish_lower = np.array([40, 70, 40], np.uint8)
        fish_lower = np.array([0,60,0], dtype = "uint8")
        fish_upper = np.array([24, 255, 145], dtype = "uint8")
        
        fish_mask = cv2.inRange(fish_hsv, fish_lower, fish_upper) # filters out black dots
        
       
        fish_mask_closing = cv2.morphologyEx(fish_mask, cv2.MORPH_CLOSE, kernelclosed)
        fish_mask_opening = cv2.morphologyEx(fish_mask_closing, cv2.MORPH_OPEN, kernelopen)

        fish_contours, hierarchy = cv2.findContours(fish_mask_opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #finds the contours in thresh_img        fish_img_contours = np.zeros(fish_erosion_again.shape) # creates empty image for contours
        fish_threshcopy = cv2.cvtColor(fish_mask_opening, cv2.COLOR_BGR2RGB) #needs to be in RBG in order to make contours colorful
        fishContours = cv2.drawContours(fish_threshcopy, fish_contours, -1, (0,255,0), 2) 
        sorted_fish_contours = sorted(fish_contours, key = cv2.contourArea, reverse = True)


        def displayWindows():
            #displays original video
            cv2.namedWindow('fgframe', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('fgframe', 600, 600)
            
            #displays blobs
            cv2.namedWindow('Fish Contours', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('Fish Contours', 600, 600)
            cv2.imshow('Fish Contours',fishContours)

           # cv2.namedWindow('Orange Detection Mask', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('Orange Detection Mask', 600, 600)
            #cv2.imshow('Orange Detection Mask',frame)  # displays the orange mask of objects
            cv2.namedWindow("Lure Contours", cv2.WINDOW_NORMAL)
            #cv2.resizeWindow("Lure Contours", 400, 600)
            cv2.imshow("Lure Contours", lureContours)  # shows the thresholded binary image of the original orange contours
        
        fishContourCount = len(sorted_fish_contours)
        lureContourCount = len(sorted_lure_contours)


        if fishContourIndex>=(fishContourCount-1) or lureContourIndex>=(lureContourCount-1):
            displayWindows()
            cv2.imshow('fgframe', frame)

        if len(sorted_fish_contours):

            Fcnt = sorted_fish_contours[fishContourIndex]

            if Fcnt is not None:

                ### FISH TRACKING ###
                FM = cv2.moments(Fcnt) # makes identity matrix of blob
        
                if FM["m00"] != 0:
                    fcX = int(FM["m10"] / FM["m00"]) #finds mass center
                    fcY = int(FM["m01"] / FM["m00"])
                    
                else:
                    fcX, fcY = 0, 0

                Fcoords = np.array([fcX, fcY])
                FxPos += [fcX]
                FyPos += [fcY]

                print(Fcoords)
                cv2.circle(fishContours, (fcX, fcY), 5, (255, 255, 255), -1)
                Lcnt = sorted_lure_contours[lureContourIndex]

            if Lcnt is not None:
                ### LURE TRACKING ###

                LM = cv2.moments(Lcnt) # makes identity matrix of blob
        
                if LM["m00"] != 0:
                    LcX = int(LM["m10"] / LM["m00"]) #finds mass center
                    LcY = int(LM["m01"] / LM["m00"])
                    
                else:
                    LcX, LcY = 0, 0

                Lcoords = np.array([LcX, LcY])
                LxPos += [LcX]
                LyPos += [LcY]
                
                print(Lcoords)

                cv2.circle(lureContours, (LcX, LcY), 5, (255, 255, 255), -1)
                #cv2.imshow('Frame', frame)
            
            # Display the frame saved in the file
            
        displayWindows()
        cv2.imshow('fgframe', frame)
            # Press q on keyboard to end camera capture
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
        


foregroundCapture.release()
result.release
cv2.destroyAllWindows()
# OpenCV stores images as BGR, but MatPlotLib uses RGB

#new = bg_model.apply(frame_init_)
bgforgraph = bg_model.getBackgroundImage()
RGB_img = cv2.cvtColor(bgforgraph, cv2.COLOR_BGR2RGB)

fig, ax1 = plt.subplots()
im1 = ax1.imshow(RGB_img)
ax1.plot(FxPos, FyPos, '*', linewidth=2.0)
plt.title('Fish Trajectory')
plt.ylabel('yPred (pixels)')
plt.xlabel('xPred (pixels)')
plt.savefig('fish_trajectory.png')
plt.show()

fig, ax2 = plt.subplots()
im2 = ax2.imshow(RGB_img)
ax2.plot(LxPos, LyPos, '*', linewidth=2.0)

plt.title('Lure Trajectory')
plt.ylabel('yPred (pixels)')
plt.xlabel('xPred (pixels)')

plt.savefig('lure_trajectory.png')

plt.show()
