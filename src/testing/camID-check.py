import cv2

cam_index = 1

cap = cv2.VideoCapture(cam_index)

# try:
#     cap = cv2.VideoCapture(cam_index)
#     if not cap.isOpened():
#         raise IOError("Cannot open webcam with ID:", cam_index)
    
# Check if the webcam is opened correctly
if not cap.isOpened():
    cam_index = cam_index + 1
    raise IOError("Cannot open webcam with ID:", cam_index)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()