"""image processing but blob identification"""
import numpy as np
import pandas as pd
import cv2 as cv 
import os
from PIL import Image 
import matplotlib.pyplot as plt
import sys

## Helper function to plot multiple images
def plot_img(images, titles):
  fig, axs = plt.subplots(nrows = 1, ncols = len(images), figsize = (15, 15))
  for i, p in enumerate(images):
    axs[i].imshow(p, 'gray')
    axs[i].set_title(titles[i])
    #axs[i].axis('off')
  plt.show()

fishimage = cv.imread("/Users/sotolab/Documents/GitHub/robot-fish-lure/ImageProcessing/fishphoto1.png")
threshval = 200

# scale factor (0 to 1, where 1 returns the original size)
scale_factor = 0.5

# generate dimensions for resized image
print(type(fishimage))

widthoriginal = int(fishimage.shape[1])
heightoriginal = int(fishimage.shape[0])

dimoriginal= (widthoriginal, heightoriginal)
print()
print("Original Dimensions:", dimoriginal)
print("Scale Factor:", scale_factor)
width = int(fishimage.shape[1] * scale_factor)
height = int(fishimage.shape[0] * scale_factor)
dim =(width, height)

# resize image
resizedfish = cv.resize(fishimage, dim, interpolation = cv.INTER_AREA)

print('Resized Dimensions : ', resizedfish.shape)
print()

resizedfishgray = cv.cvtColor(resizedfish, cv.COLOR_BGR2GRAY)
cv.imshow("resized fish image",resizedfishgray)

ret_binary, fishbinary = cv.threshold(resizedfishgray, threshval, 255 ,cv.THRESH_BINARY )
images = [ resizedfishgray, fishbinary]
titles = ["resized and greyscale", "threshold binary"]
cv.imshow(" fish binary",fishbinary)

#print("going to plot")
#plot_img(images, titles) ## we know now that the smallfish is not beoing recognized

# find the image contours
contours, hierarchy = cv.findContours(fishbinary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) ##what does this do?

print("Number of Contours found = " + str(len(contours)))

# Copy the image to preserve original
fishbinary_copy = fishbinary.copy()

# overlay the contours on the original image 
overlay = cv.drawContours(fishbinary_copy, contours, -1, (0,255,0), 1)

# Plot the image with overlayed contours 
cv.imshow('contour trace',overlay)
cv.waitKey(0)

cv.destroyAllWindows()
print("done")