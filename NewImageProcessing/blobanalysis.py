"""angelinas background subtraction / blob analysis"""

from __future__ import print_function
import cv2
import numpy as np
import matplotlib as mp
import pandas as pd
import matplotlib.pyplot as plt

# Initialize variable to break while loop when last frame is achieved
last = 0

xPos = []
yPos = []

thresh = 100
bg_model = cv2.createBackgroundSubtractorKNN(history = 800, dist2Threshold = 255.0, detectShadows = True) 


#10 second vid
# one fish
#foregroundPath = r"C:\Users\ginar\Documents\robot-fish-lure\src\oneFish.mp4"

#many fish
foregroundPath = r"C:\Users\ginar\Documents\robot-fish-lure\src\goodvid_lots_of_interaction (online-video-cutter.com).mp4"

#zebrafish
#foregroundPath = r"C:\Users\ginar\Documents\robot-fish-lure\src\zf-hunting-prey-2.mp4"

foregroundCapture = cv2.VideoCapture(foregroundPath)

foregroundCapture.set(cv2.CAP_PROP_POS_FRAMES, 0)

if not foregroundCapture.isOpened():
    print('Unable to open')
    exit(0)

while True:

    foreret, foreframe = foregroundCapture.read()

    if not foreret:
        break

    this_frame = foregroundCapture.get(1)

    if foreret:
        
        # Convert current frame to grayscale
        #foreframe_G = cv2.GaussianBlur(foreframe, (5, 5), 10)
        fg_greyframe = cv2.cvtColor(foreframe, cv2.COLOR_BGR2GRAY)
        fg_bilateral = cv2.bilateralFilter(fg_greyframe, 8, 50, 100)
        
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 5))
        kernel = np.ones((7,7),np.uint8)
        
        erosion = cv2.erode(fg_bilateral,kernel,iterations = 1) #trims down
        dilated_img = cv2.dilate(erosion, kernel, iterations=1) # makes bigger
        
        opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel) # closing dots inside fish and in backround
        

        # Take complement of background
        fgMask = bg_model.apply(closing)
        #bg_greyframe = cv2.cvtColor(fgMask, cv2.COLOR_BGR2GRAY)
        #bg_inv = cv2.bitwise_not(bg_greyframe)
        ret,thresh_img = cv2.threshold(dilated_img, thresh, 100, cv2.THRESH_BINARY)
        #thresh_img = cv2.adaptiveThreshold(opening, 100, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 199, 5)

        #find contours
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #find area
        
        #sort countours largest to smallest. the fish countour is the 9th largest
        sorted_contours = sorted(contours, key = cv2.contourArea, reverse = True)

        img_contours = np.zeros(thresh_img.shape)

        threshcopy = cv2.cvtColor(thresh_img, cv2.COLOR_BGR2RGB)
        rgbthresh = cv2.cvtColor(threshcopy, cv2.COLOR_BGR2RGB)
        greencontours = cv2.drawContours(rgbthresh, contours[0:30], -1, (0,255,0), 2) 
        
        

        if len(sorted_contours):

            cnt = sorted_contours[2]

            if cnt is not None:

                M = cv2.moments(cnt) # makes identity matrix of blob
        
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"]) #finds mass center
                    cY = int(M["m01"] / M["m00"])
                    
                else:
                    cX, cY = 0, 0

                coords = np.array([cX, cY])
                xPos += [cX]
                yPos += [cY]
                
                #print(coords)
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

        if last >= this_frame:
            break

        last = this_frame

        #displays original video
        cv2.namedWindow('fgframe', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('fgframe', 400, 600)
        cv2.circle(greencontours, (cX, cY), 5, (255, 255, 255), -1)
        cv2.imshow('fgframe', foreframe)
        
        #displays blobs
        cv2.namedWindow('draw countours on binary', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('draw countours on binary', 400, 600)
        cv2.imshow('draw countours on binary',greencontours)

# When everything done, release the capture
foregroundCapture.release()
cv2.destroyAllWindows()
cv2.waitKey(0)

# OpenCV stores images as BGR, but MatPlotLib uses RGB
bgforgraph = bg_model.getBackgroundImage()
RGB_img = cv2.cvtColor(bgforgraph, cv2.COLOR_BGR2RGB)
fig, ax = plt.subplots()

im = ax.imshow(RGB_img)

ax.plot(xPos, yPos, '*', linewidth=2.0)

plt.title('Animal Trajectory')
plt.ylabel('yPred (pixels)')
plt.xlabel('xPred (pixels)')

plt.savefig('animal_trajectory.png')

plt.show()
print("done!")

# only track only one blob over multiple frames
#create function that returns coordinates in "make-path form"
