"""angelinas background subtraction / blob analysis"""
import cv2
import numpy as np
import matplotlib as mp
import pandas as pd
import matplotlib.pyplot as plt

# Initialize variable to break while loop when last frame is achieved
last = 0

LxPos = []
LyPos = []

FxPos = []
FyPos = []

thresh = 100
fishContourIndex = 0
lureContourIndex = 0
bg_model = cv2.createBackgroundSubtractorKNN(history = 800, dist2Threshold = 255.0, detectShadows = True) 

#10 second vid
# one fish
#foregroundPath = r"C:\Users\ginar\Documents\robot-fish-lure\src\oneFish.mp4"

#many fish
#foregroundPath = r"C:\Users\ginar\Documents\robot-fish-lure\src\goodvid_lots_of_interaction (online-video-cutter.com).mp4"

#zebrafish // thresh=175, fgMask = bg_model.apply(dilated_img) 
#foregroundPath = r"C:\Users\ginar\Documents\robot-fish-lure\src\zf-hunting-prey-2.mp4"

#black and orange
#foregroundPath = r"C:\Users\ginar\Documents\robot-fish-lure\src\orange + black.mp4"

#foregroundCapture = cv2.VideoCapture(foregroundPath)

foregroundCapture = cv2.VideoCapture(0)

# foregroundCapture.set(cv2.CAP_PROP_POS_FRAMES, 0)
if not foregroundCapture.isOpened():
    print('Unable to open')
    exit(0)

while True:

    foreret, foreframe = foregroundCapture.read()

    if not foreret:
        break

    this_frame = foregroundCapture.get(1)

    if foreret:

        kernel = np.ones((7,7),np.uint8)

        ############ ORANGE TRACKING #############

        into_hsv =cv2.cvtColor(foreframe,cv2.COLOR_BGR2HSV)
        lower_orange= np.array([0, 70, 100], dtype = "uint8") 
        upper_orange= np.array([23, 150, 130], dtype = "uint8")
    
        
        b_mask=cv2.inRange(into_hsv,lower_orange,upper_orange)
        # creating the mask using inRange() function
        # this will produce an image where the color of the objects
        # falling in the range will turn white and rest will be black
        orange=cv2.bitwise_and(foreframe,foreframe,mask=b_mask)

        orange_dilated_img = cv2.dilate(orange, kernel, iterations=2)
        orange_closing = cv2.morphologyEx(orange_dilated_img, cv2.MORPH_CLOSE, kernel)
        orange_erosion = cv2.erode(orange_closing,kernel,iterations =0)

        bgrorange = cv2.cvtColor(orange_erosion, cv2.COLOR_HSV2BGR) #changes color type of orange mask OUT of HSV
        greyorange = cv2.cvtColor(bgrorange, cv2.COLOR_BGR2GRAY) # greyscales the orange mask
       
        
        #erosion = cv2.erode(greyorange,kernel,iterations = 1) #trims down
        #lure_erosion = cv2.erode(greyorange,kernel,iterations = 1) #trims down
        ret,lure_thresh_img = cv2.threshold(greyorange, 100, 255, cv2.THRESH_BINARY) #converts the greyscale orange mask to binary
        
        lure_contours, hierarchy = cv2.findContours(lure_thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #finds the contours in thresh_img
        lure_img_contours = np.zeros(lure_thresh_img.shape) # creates empty image for contours
        lure_threshcopy = cv2.cvtColor(lure_thresh_img, cv2.COLOR_BGR2RGB) #needs to be in RBG in order to make contours colorful
        lureContours = cv2.drawContours(lure_threshcopy, lure_contours, -1, (255,165,0), 2) 
        sorted_lure_contours = sorted(lure_contours, key = cv2.contourArea, reverse = True)

        ############# TRACK FISH W/ HSV ###############

        #foreframe_G = cv2.GaussianBlur(foreframe, (5, 5), 10)
        fish_hsv = cv2.cvtColor(foreframe,cv2.COLOR_BGR2HSV)
        

        #fish_lower = np.array([40, 70, 40], np.uint8)
        fish_lower = np.array([29,70,100], dtype = "uint8")
        fish_upper = np.array([35, 150, 110], dtype = "uint8")
        
        fish_mask = cv2.inRange(fish_hsv, fish_lower, fish_upper) # filters out black dots
        fish_dilated_img = cv2.dilate(fish_mask, kernel, iterations=9) # makes bigger
        fish_erosion = cv2.erode(fish_dilated_img,kernel,iterations = 6)
        fish_mask_opening = cv2.morphologyEx(fish_erosion, cv2.MORPH_OPEN, kernel)
        fish_mask_closing = cv2.morphologyEx(fish_mask_opening, cv2.MORPH_CLOSE, kernel)
        fish_mask_closing_again = cv2.morphologyEx(fish_mask_closing, cv2.MORPH_CLOSE, kernel)
        fish_erosion_again = cv2.erode(fish_mask_closing_again,kernel,iterations = 1) # FISH THRESHOLD/BINARY IMAGE

        fish_contours, hierarchy = cv2.findContours(fish_erosion_again, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #finds the contours in thresh_img
        fish_img_contours = np.zeros(fish_erosion_again.shape) # creates empty image for contours
        fish_threshcopy = cv2.cvtColor(fish_erosion_again, cv2.COLOR_BGR2RGB) #needs to be in RBG in order to make contours colorful
        fishContours = cv2.drawContours(fish_threshcopy, fish_contours, -1, (0,255,0), 2) 
        sorted_fish_contours = sorted(fish_contours, key = cv2.contourArea, reverse = True)


        def displayWindows():
            #displays original video
            cv2.namedWindow('fgframe', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('fgframe', 600, 600)
            
            #displays blobs
            cv2.namedWindow('Fish Contours', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Fish Contours', 600, 600)
            cv2.imshow('Fish Contours',fishContours)

           # cv2.namedWindow('Orange Detection Mask', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('Orange Detection Mask', 600, 600)
            #cv2.imshow('Orange Detection Mask',foreframe)  # displays the orange mask of objects
            cv2.namedWindow("Lure Contours", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Lure Contours", 400, 600)
            cv2.imshow("Lure Contours", lureContours)  # shows the thresholded binary image of the original orange contours
        
        fishContourCount = len(sorted_fish_contours)
        lureContourCount = len(sorted_lure_contours)

        if fishContourIndex>=(fishContourCount-1) or lureContourIndex>=(sorted_lure_contours-1):
            displayWindows()
            cv2.imshow('fgframe', foreframe)

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

                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

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
                    if cv2.waitKey(30) & 0xFF == ord('q'):
                        break

                    cv2.circle(lureContours, (LcX, LcY), 5, (255, 255, 255), -1)

        if last >= this_frame:
            break

        last = this_frame

        displayWindows()

    cv2.waitKey(1)
foregroundCapture.release()
cv2.destroyAllWindows()
# OpenCV stores images as BGR, but MatPlotLib uses RGB

new = bg_model.apply(into_hsv)
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
