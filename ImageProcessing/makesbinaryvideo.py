import numpy as np
import cv2 as cv
import sys
import os

"""6.2.23 - emily, hacked together alishas blob analysis and a black and white video
currently outputs a binary video
how do we get it to outline the binary black parts with 1) green, 2) as blobs?

how to sort them??

"""
vidpath = '/Users/sotolab/Documents/GitHub/robot-fish-lure/supertrimmed6.2.mp4'

# reading the video
cap = cv.VideoCapture()

codec  = 'mp4v'
ind_max = 1000 #max number of frames for bg model
#input video path
input_vidpath = vidpath

# Set codec for video
codec = 'mp4v'
# Set max number of frames for background model
ind_max = 1000

## Open video
cap = cv.VideoCapture(input_vidpath)
if not cap.isOpened():
    sys.exit(
        'Video file cannot be read! Please check input_vidpath to ensure it is correctly pointing to the video file')
    
# Get first frame for setting up output video
ret, frame_init = cap.read()

# running the loop
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
        
        #good threshold for the trimmed video!! doesnt really pick up the shadow
        thresh = 90

        #get threshold image
        ret,thresh_img = cv.threshold(frame, thresh, 255, cv.THRESH_BINARY)

        #find contours
        contours, hierarchy = cv.findContours(thresh_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        #sort countours largest to smallest. the fish countour is the 9th largest
        sorted_contours = sorted(contours, key = cv.contourArea, reverse = True)

        #create an empty image for contours, just a black screen
        img_contours = np.zeros(frame.shape)

        # draw the fish countour on the original image
        overlay = cv.drawContours(frame, sorted_contours[8:9], -1, (255,0,0), 3)
        
        #draw the fish countour on the binary image
        threshcopy = thresh_img.copy()

        print("Number of Contours found = " + str(len(contours)))

        overlay = cv.drawContours(threshcopy, sorted_contours[8:9], -1, (0,255,0), 3) 
        ##looks like here, it saves the outlines but puts the outlining through the thresholding which makes it black again
        cv.imshow('draw countours on binary',overlay)
        cv.waitKey(0)
        cv.destroyAllWindows()

"""blob outlining testing 
first displays binary image 
then displays blob outlines over the original image"""
"""hello!! need to make changes to github"""

