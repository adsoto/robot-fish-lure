
"""Program meant to save video captures from the overhead webcam above the fishtank. 
Source code from: https://www.geeksforgeeks.org/saving-a-video-using-opencv/  
Modified to change the filename and extension."""

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

#getting resolutions 
frame_width = int(video.get(3))
frame_height = int(video.get(4))

print("height:",frame_height)
print("width:",frame_width)

# generates date and time info for the video filename
size = (frame_width, frame_height)
now = str(datetime.now())
filename = str(now[0:19])

# writes video to save -- filename, fourcc, framerate, size of video 
result = cv2.VideoWriter(filename +".avi",cv2.VideoWriter_fourcc(*'MJPG'), 30, size)
	
while(True):
	ret, frame = video.read()
	frame = cv2.undistort(frame, MTX, DIST, None, MTX)


	
	if ret == True:

		result.write(frame)

		# Display the frame saved in the file
		cv2.imshow('Frame', frame)

		# Press q on keyboard to end camera capture
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	else:
		break

# When everything done, release the video capture and write objects
video.release()
result.release()
	
# closes windows
cv2.destroyAllWindows()

print("The video was successfully saved as:", filename )
