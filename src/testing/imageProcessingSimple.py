
import cv2
import numpy as np

mtx = np.array([[1.05663779e+03, 0.00000000e+00, 9.73055094e+02],
 [0.00000000e+00, 1.05269643e+03, 5.64799418e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

dist = np.array([-3.80359934e-01,  1.49531854e-01,  2.50649988e-05,  8.39488578e-05,  -2.83529982e-02])

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('output.mp4', fourcc, 10.0, (920,540))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.undistort(frame, mtx, dist, None, mtx)
    frame = frame[322:794, 593:1412]
    # out.write(frame)

    if (ret and frame is not None):
        original = frame.copy()
   
        # Resize and display the resulting frame
        cv2.namedWindow("output", cv2.WINDOW_NORMAL)
        resized = cv2.resize(original, (920, 540))
        cv2.imshow('frame', resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
# out.release()
