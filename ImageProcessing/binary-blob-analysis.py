"""creates a video of just the fish with blob outlines"""

from __future__ import print_function
import cv2
import numpy as np
backSub = cv2.createBackgroundSubtractorKNN(history = 1, dist2Threshold = 600, detectShadows = False) 

path = r"/Users/alishachulani/Desktop/trimmed11sec.mp4"
thresh = 90
#backSub = cv.createBackgroundSubtractorMOG2()
capture = cv2.VideoCapture(path)

if not capture.isOpened():
    print('Unable to open')
    exit(0)

while True:
    ret, frame = capture.read()
    greyframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    fgMask = backSub.apply(frame) #create forground mask
    bg_inv = cv2.bitwise_not(fgMask) #invert foreground mask
    frame_sub = cv2.add(greyframe, bg_inv) #add inverted masks to the greyscale frames

    #get threshold image of the altered frames
    ret,thresh_img = cv2.threshold(frame_sub, thresh, 255, cv2.THRESH_BINARY)
 
    #find contours
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #sort countours largest to smallest. the fish countour is the 9th largest
    sorted_contours = sorted(contours, key = cv2.contourArea, reverse = True)

    #create an empty image for contours, just a black screen
    img_contours = np.zeros(frame_sub.shape)

    # draw the fish countour on the original image
    overlay = cv2.drawContours(frame_sub, sorted_contours[6:7], -1, (0,500,0), 3)

    #draw the fish countour on the binary image
    threshcopy = cv2.cvtColor(thresh_img, cv2.COLOR_BGR2RGB) #needs to be in RBG in order to make contours colorful
    overlay = cv2.drawContours(threshcopy, contours, -1, (0,500,0), 3) 

    cv2.imshow('draw countours on binary',overlay)
    #cv2.imshow('FG mask', fgMask)
    cv2.waitKey(1)

    print("done!")