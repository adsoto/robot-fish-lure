import numpy as np
import cv2 as cv
import cv2
import sys
import os

"""6.2.23 - emily, hacked together alishas blob analysis and a black and white video
currently outputs a binary video
how do we get it to outline the binary black parts with 1) green, 2) as blobs?

how to sort them??

6.5.23 - alisha, updated binary vid to include blobs 
    *note that halfway through video when fish goes over clay rectangle, blob becomes one

"""
vidpath = '/Users/alishachulani/Desktop/supertrimmed6.2.mp4'

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
    
bg_model = cv.createBackgroundSubtractorKNN(history=800, dist2Threshold=1.0, detectShadows=True)

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
        cv.imwrite("/Users/alishachulani/Desktop/video_background.png", bg_im)

    print('done')
    


cap.set(cv.CAP_PROP_POS_FRAMES, 0)
# Get first frame for setting up output video
ret, frame_init = cap.read()

# running the loop
while True:
    print('entered')
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Bail out when the video file ends
    if not ret:
        print('broke')
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

        copy = bg_im.copy()

        thresh_copy = cv2.cvtColor(thresh_img, cv2.COLOR_BGR2RGB)
        overlay = cv.drawContours(thresh_copy, contours, -1, (0,255,0), 3) 
        cv.imshow('draw countours on binary',overlay)
        cv.waitKey(0) #change to 0 to click through frames

        cv.destroyAllWindows()

"""blob outlining testing 
first displays binary image 
then displays blob outlines over the original image"""
"""hello!! need to make changes to github"""