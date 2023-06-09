
"""Program meant to save video captures from the overhead webcam above the fishtank. 
Source code from: https://www.geeksforgeeks.org/saving-a-video-using-opencv/  
Modified to change the filename and extension, as well as display image pixel location on click"""

import cv2
from datetime import *
import numpy as np

# MTX and DIST are properties of the camera (have to do with fisheye lens)
MTX = np.array([[1.05663779e+03, 0.00000000e+00, 9.73055094e+02],
 [0.00000000e+00, 1.05269643e+03, 5.64799418e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
DIST = np.array([-3.80359934e-01,  1.49531854e-01,  2.50649988e-05,  8.39488578e-05,  -2.83529982e-02])

video = cv2.VideoCapture(0)

# We need to check if camera
# is opened previously or not
if (video.isOpened() == False):
    print("Error reading video file")

def click_event(event, x, y, flags, params):
   if event == cv2.EVENT_LBUTTONDOWN:
      print(f'({x},{y})') # when clicked image, display pixels
    
while(True):

    #keck: [570,  311], [1442, 802]
    # lair [685,  394], [1481, 800]
    camera_bounds = np.array([[570,  311], [1442, 802]])   #CHANGE THESE! THESE ARE TANK BOUNDS
    ret, frame = video.read()
    frame = cv2.undistort(frame, MTX, DIST, None, MTX)
    frame = frame[camera_bounds[0][1]:camera_bounds[1][1], camera_bounds[0][0]:camera_bounds[1][0]]

    if ret == True:

        # Display the frame -- clicking place on frame will print the pixels 
        cv2.namedWindow('Frame')
        cv2.setMouseCallback('Frame', click_event)
        cv2.imshow('Frame', frame)

        # Press q on keyboard to end camera capture
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# When everything done, release the video capture and write objects
video.release()
    
# closes windows
cv2.destroyAllWindows()
