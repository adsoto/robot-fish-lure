"""order of events for image processing
load in greyscale video
identify frame and objects -- thresholds, which type of processing is better?
sort the identified objects based on properties (size???)
identify centroids and track movement of specified objects over time
"""
"""some source code: https://learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
otherwise source code from Prof. Soto's tutorials for object tracking inputs""" 


import numpy as np
import pandas as pd
import cv2 as cv
import os
import matplotlib.pyplot as plt
import sys

codec  = 'mp4v'
ind_max = 1000 #max number of frames for bg model
#input video path
input_path = "/Users/sotolab/Documents/GitHub/robot-fish-lure/ImageProcessing/trimmed-fishvid1.mp4"
input_vidpath = input_path

# Set codec for video
codec = 'mp4v'
# Set max number of frames for background model
ind_max = 1000


#bg_model = cv.createBackgroundSubtractorMOG2(history=500, varThreshold = 16)
bg_model = cv.createBackgroundSubtractorKNN(history=800, dist2Threshold=1.0)

## Open video
cap = cv.VideoCapture(input_vidpath)
if not cap.isOpened():
    sys.exit(
        'Video file cannot be read! Please check input_vidpath to ensure it is correctly pointing to the video file')
    
# Get first frame for setting up output video
ret, frame_init = cap.read()

# iterate through frames to compute background image
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        break

    # Convert current frame to grayscale
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Extract current frame number
    frame_curr = cap.get(1)

    if ret:
        # Apply background model, returns binary foreground image
        # we can fiddle with the second input or leave empty
        # fgmask = bg_model.apply(frame, 0.6)
        fgmask = bg_model.apply(frame)

        # Get background image
        bg_im = bg_model.getBackgroundImage()

        if cv.waitKey(30) & 0xFF == ord('q'):
            break

    # Save background image and Break loop after max frames
    if frame_curr >= ind_max:
        # Write background image
        cv.imwrite("/Users/sotolab/Documents/GitHub/robot-fish-lure/ImageProcessing/video_background.png", bg_im)

# Display background image


#Reset the counter for the video capture object
cap.set(cv.CAP_PROP_POS_FRAMES, 0)

# Initialize variable to break while loop when last frame is achieved
last = 0

xPos = []
yPos = []

xPos1 = []
yPos1 = []
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Bail out when the video file ends
    if not ret:
        break

    # Extract current frame number
    this_frame = cap.get(1)

    # Copy of current frame 
    original = frame.copy()

    if ret:
        # Convert current frame to grayscale
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Take complement of background
        bg_inv = cv.bitwise_not(bg_im)

        # Background subtraction (by adding inverse of background)
        frame_sub = cv.add(frame, bg_inv)

        # Apply smoothing filter
        frame_smooth = cv.bilateralFilter(frame_sub, 5, 40, 40)
        
        # Global thresholding
        frame_binary = cv.threshold(frame_smooth, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
        # thresh = cv2.threshold(frame_smooth, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Get image contours 
        cnts = cv.findContours(frame_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        # Sort contours largest to smallest
        sorted_cnts = sorted(cnts, key=cv.contourArea, reverse=True)
        # sorts contours into a list of areas, largest to smallest
    
        """I dont really understand how this function worked -- how can we modify it to happen for all the contours we want?"""
      
        if len(sorted_cnts):
            cnt = sorted_cnts[0]
            cnt1 = sorted_cnts[1]
            
            M = cv.moments(cnt) #detects movements for contour "cnt", which is the first, largest contour
            M2 = cv.moments(cnt1)

            # Initialize array for object coordinates
            coords = np.array([0, 0])

            if M["m00"] != 0: #calculates centroid for m0
              cX = int(M["m10"] / M["m00"])
              cY = int(M["m01"] / M["m00"])

            if M2["m00"] != 0: #calculates centroid for m1
              cX1 = int(M2["m10"] / M2["m00"])
              cY1 = int(M2["m01"] / M2["m00"])
            
            else:
              cX, cY = 0, 0 #else, centroid position is the origin

            coords = np.array([cX, cY]) #tracks centroid through movement?
            xPos += [cX]
            yPos += [cY]
            

            coords1 = np.array([cX1, cY1]) #tracks centroid through movement?
            xPos1 += [cX1]
            yPos1 += [cY1]
            if cv.waitKey(30) & 0xFF == ord('q'):
              break

    if last >= this_frame:
        break

    last = this_frame

    # otherwise

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
cv.waitKey(1)
print("Done!!")

plt.title('Animal Trajectory')
plt.ylabel('yPred (pixels)')
plt.xlabel('xPred (pixels)')
plt.savefig('animal_trajectory.png')

# OpenCV stores images as BGR, but MatPlotLib uses RGB
RGB_img = cv.cvtColor(bg_im, cv.COLOR_BGR2RGB)

fig, ax = plt.subplots()

im = ax.imshow(RGB_img)

ax.plot(xPos, yPos, linewidth=2.0)
ax.plot(xPos1, yPos1, linewidth=2.0)

plt.show()

# confused about the ordering here #


# ^^ for some reason the labels aren't working?? 


""""
to display the background iamge taken:

cv.imshow("image",bg_im)
cv.waitKey(0)
cv.destroyAllWindows
# displays backgroung image up to here!!
"""
"""
#threshold filtering:

while(cap.isOpened()):
  # read frames in
  ret, frame = cap.read()

  if ret == True:
    frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    bg_inv = cv.bitwise_not(bg_im)
    frame_sub = cv.add(frame,bg_inv)
    frame_smooth = cv.bilateralFilter(frame_sub, 5, 40, 40)

    #GLOBAL THRESHOLD
    frame_binary = cv.threshold(frame_smooth,0,255,cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    cv.imshow('Frame',frame)
 
    # q to exit
    if cv.waitKey(25) & 0xFF == ord('q'):
      break
 
  else: 
    break
 
cap.release()
cv.destroyAllWindows()

"""