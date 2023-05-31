import cv2
import numpy as np

"""Used when tank/image that the camera processes changes. DO NOT alter camera calibration when setup
changes location.
Run this and HARD CLICK opposite corners to define the robot's driving space. See code documentation in drive"""

MTX = np.array([[1.05663779e+03, 0.00000000e+00, 9.73055094e+02],
 [0.00000000e+00, 1.05269643e+03, 5.64799418e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
DIST = np.array([-3.80359934e-01,  1.49531854e-01,  2.50649988e-05,  8.39488578e-05,  -2.83529982e-02])

def on_mouse(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(resized, (x, y), 5, (320, 159, 22), -1)
        mouseX,mouseY = x,y

def get_click(image):
    while(True):
        cv2.imshow('image', image)
        k = cv2.waitKey(20) & 0xFF
        if k == ord('g'):
            # print(mouseX, mouseY)
            break
    return [mouseX, mouseY]

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', on_mouse)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
# frame = cv2.imread("data/04.11.2023/test.png")
frame = cv2.undistort(frame, MTX, DIST, None, MTX)
resized = cv2.resize(frame, (960, 540))

# HARD CLICK a corner, then press g to save and setup the next point.
# HARD CLICK opposite diagonal corner, then press g to save and exit.

[x1, y1] = get_click(frame)
[x2, y2] = get_click(frame)

print(np.array([[x1, y1], [x2, y2]])) # Generates array of video from size, input into controller file for image processing
cropped = frame[y1:y2, x1:x2]
resized = cv2.resize(cropped, (960, 540))
cv2.imshow('image', resized)
cv2.waitKey()

cv2.destroyAllWindows()