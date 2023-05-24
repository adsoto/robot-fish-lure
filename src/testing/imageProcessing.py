
import cv2
import numpy as np

mtx = np.array([[1.05663779e+03, 0.00000000e+00, 9.73055094e+02],
 [0.00000000e+00, 1.05269643e+03, 5.64799418e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

dist = np.array([-3.80359934e-01,  1.49531854e-01,  2.50649988e-05,  8.39488578e-05,  -2.83529982e-02])


cap = cv2.VideoCapture(0)

#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (910,565))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if (ret and frame is not None):

        # Our operations on the frame come here
        frame = frame[300:865, 435:1345]
        #out.write(frame)

        original = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (53,53), 0)
        # global thresholding
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # adaptive thresholding
        #thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 201, 10)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        #print(len(cnts))
        sorted_cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        #for c in cnts:
        head_coords = np.array([0, 0])
        tail_coords = np.array([0, 0])
        for i in range(0,len(sorted_cnts)):
            c = sorted_cnts[i]
            # Obtain bounding rectangle to get measurements
            x,y,w,h = cv2.boundingRect(c)
            area = cv2.contourArea(c)

            
            #print(angle_2_x)

            # Find centroid
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            if i == 0:
                head_coords = np.array([cX, cY])
                #print(head_coords)
            if i == 1:
                tail_coords = np.array([cX, cY])
                #print(tail_coords)
            
            if i == 0:
                #print("x = " + str(cX) + ", y = " + str(cY))
                # Draw the contour and center of the shape on the image
                #cv2.rectangle(original,(x,y),(x+w,y+h),(36,255,12), 4)
                cv2.circle(original, (cX, cY), 10, (320, 159, 22), -1) 
                #if cX > 500:
                #    print("yo")
                #else:
                #    print("no")
        if head_coords[0] != 0 and tail_coords[0] != 0:
            x_axis      = np.array([1, 0])
            fish_vect   = head_coords - tail_coords
            fish_unit   = fish_vect/np.linalg.norm(fish_vect)
            dot_product = np.dot(x_axis, fish_unit)
            angle_2_x   = np.arccos(dot_product)
            if head_coords[1] > tail_coords[1]:
                angle_2_x = -1*angle_2_x + 2*np.pi
            #print(angle_2_x*180/np.pi)
        # Resize and display the resulting frame
        cv2.namedWindow("output", cv2.WINDOW_NORMAL)
        resized = cv2.resize(original, (960, 540))
        cv2.imshow('frame', resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
# out.close()
