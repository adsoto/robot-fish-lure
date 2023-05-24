
import cv2

cap = cv2.VideoCapture(0)

i = 0
while True:
    ret, frame = cap.read()
    resized = cv2.resize(frame, (960, 540))
    cv2.imshow("frame", resized)
    if cv2.waitKey(1) & 0xFF == ord('p'): # save a picture
        cv2.imwrite("checkerboard_pic_" + str(i) + ".png", frame)
        i += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
