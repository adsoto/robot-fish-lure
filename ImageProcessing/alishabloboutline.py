"""blob outlining testing 
first displays binary image 
then displays blob outlines over the original image
then displays blob outlines over binary image"""

import cv2
import numpy as np
import cv2 as cv

img = cv2.imread('/Users/alishachulani/Desktop/kecktrial.png', cv2.IMREAD_UNCHANGED)

#convert img to grey
img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#set a thresh
thresh = 120
#get threshold image
ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
cv2.imshow('binary image',thresh_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#find contours
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#sort countours largest to smallest. the fish countour is the 9th largest
sorted_contours = sorted(contours, key = cv.contourArea, reverse = True)

#create an empty image for contours, just a black screen
img_contours = np.zeros(img.shape)

# draw the fish countour on the original image

#fish 1 - 4:5
#fish 2 - 5:6
#fish 3 - 6:7
overlay = cv2.drawContours(img, sorted_contours[6:7], -1, (0,500,0), 3)
cv2.imshow('draw countours on original',overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()

#draw the fish countour on the binary image
threshcopy = cv2.cvtColor(thresh_img, cv2.COLOR_BGR2RGB)
overlay = cv2.drawContours(threshcopy, contours, -1, (0,500,0), 3) 
cv2.imshow('draw countours on binary',overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()
