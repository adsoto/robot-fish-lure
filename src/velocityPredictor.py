import math
import cv2
import numpy as np

class velocityPredictor:

    def __init__(self, camera_port):
        self._port = camera_port
        

    def getposlist(self, fishdict, fish):
        # returns list of time and positions for fish i
        return fishdict[fish][0]

    def getXposition(self, fish):
        # extracts the x positions of a particular fish in a particular frame from the dictioanry of fish positions and times
        id, x, y, t, w, h = fish
        cx = (x + x + w) // 2
        return(cx)
    
    def getYposition(self, fish):
        # extracts the x positions of a particular fish in a particular frame from the dictioanry of fish positions and times
        id, x, y, t, w, h = fish
        cy = (y + y + h) // 2
        return(cy)
    
    def getTime(self, fish):
        time = fish[3]
        #print ("time", time)
        return (time)
    
    def xVelocity(self,x1, x2, timestep):
        return float((x2-x1)/timestep)

    def yVelocity(self,y1, y2, timestep):
        return float((y2-y1)/timestep)
    
    def bw_vel_est(self, lastfish, currentfish):
        # computes a backwards referenced velocity estimation
        t_current = self.getTime(currentfish)
        t_diff = t_current - self.getTime(lastfish)
        
        x_current = self.getXposition(currentfish)
        x_past = self.getXposition(lastfish)

        y_current = self.getYposition(currentfish)
        y_past = self.getYposition(lastfish)

        xvel = self.xVelocity(x_past, x_current,t_diff)
        yvel = self.yVelocity(y_past, y_current,t_diff)

        vel = [round(xvel, 4), round(yvel, 4)]
        return vel

    def assignIDs(self, totalPrevList, fishMeasurements): # fish: [x,y,t,w,h], prevList: [[[1,x,y,t,w,h], [2,x,y,t,w,h]],...]
        
        t_1 = totalPrevList[-1]
        
        crossoverList = [] # id's of fish that crossover during frame

        for i in range(0,len(t_1)-1): # check for duplicate (x,y) coords (overlapping fish)
            for j in range(1, len(t_1)):
                if t_1[i][1] == t_1[j][1] and t_1[i][2] == t_1[j][2] and t_1[i][0] != t_1[j][0]:
                        if t_1[i] not in crossoverList and t_1[j] not in crossoverList:
                            crossoverList.append(t_1[i])
                            crossoverList.append(t_1[j])

        t_2 = totalPrevList[-2]
        fishCount = len(t_1)
        returnList = []
        measuredList = []


        if len(t_2) != len(t_1):
            pass
        else:
            for i in range (0, fishCount):
                t_2Fish = t_2[i]
                t_1Fish = t_1[i]
                [deltax, deltay] = self.bw_vel_est(t_2Fish, t_1Fish)
                xPrev = self.getXposition(t_1Fish)
                yPrev = self.getYposition(t_1Fish)
                predictedCoord = ((xPrev + deltax), (yPrev + deltay))

                coord = ((int(predictedCoord[0]), int(predictedCoord[1])))
                

                minDist = 1000000 # baseline distance

                for fish in fishMeasurements:
                    x, y, t, w, h = fish
                    cx = (x + x + w) // 2
                    cy = (y + y + h) // 2
                    dist = math.dist((cx, cy), predictedCoord)
                    if dist<minDist: # finding shortest distance between current fish and fish from previous frame
                        minDist = dist
                        newFish = [i+1, x, y, t, w, h]
                if crossoverList == []:
                    #self.displayPredictions(fishMeasurements, coord, t_1[i][0])
                    returnList.append(newFish)
                else:
                    # smoothing filter
                    id, x, y, t, w, h = newFish

                    x_t_1 = t_1[i][1]
                    x_t_2 = t_1[i][2]

                    measuredX = float(x)
                    measuredY = float(y)

                    measuredFish = newFish
                    measuredList.append(measuredFish)

                    l = float(0.8) # leans toward measured
                    x_smooth = (l*measuredX) + ((1-l)*x_t_1)
                    y_smooth = (l*measuredY) + ((1-l)*x_t_2)
                    #print("smooth", x_smooth, y_smooth)
                    self.displayPredictions(fishMeasurements, (x_smooth, y_smooth), t_1[i][0])
                    newFish = [id, int(x_smooth), int(y_smooth), t, w, h]
                    #print("compare: ", x_smooth, y_smooth, w, h)
                    returnList.append(newFish)
                    

            if crossoverList != []:
                
                leftoverMeasurements = []
                for measurement in fishMeasurements: # checks if any fish measurements are not accounted for (due to crossover)
                    found = False
                    for returnFish in measuredList:
                        if returnFish[1:] == measurement:
                            found = True
                            break
                            
                    if found == False:
                        leftoverMeasurements.append(measurement)
                
                for m in leftoverMeasurements: # [[820, 382, 3, 50, 66]]
                    mx, my, mt, mw, mh = m
                    minDist = 110
                    for c in crossoverList: # [[5, 825, 376, 2, 45, 72], [9, 825, 376, 2, 45, 72]]
                        id, cx, cy, ct, cw, ch = c

                        dist = math.dist((mx, my), (cx, cy))
                        if dist<minDist:
                            minDist = dist
                            closestFish = c # finds closest 
                    if minDist < 100:
                        closestFish = [id, mx, my, mt, mw, mh]
                        for i in range(0, len(returnList)):
                            if returnList[i][0] == closestFish[0]:
                                returnList[i] = closestFish

            return returnList # ex: [[1, 10, 10, 200, 1, 1], [2, 60, 50, 200, 1, 1], [3, 310, 410, 200, 1, 1]]

    def displayPredictions(self, fishMeasurements, predictedCoord, id):
        img = cv2.imread(self._port)
        bounds = np.array([[570,  300], [1450, 820]]) 
        img = img[bounds[0][1]:bounds[1][1], bounds[0][0]:bounds[1][0]]
        
        for fish in fishMeasurements:
            x = fish[0]
            y = fish[1]
            w = fish[3]
            h = fish[4]
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            cv2.circle(img, (cx,cy), 3, [255,0,0], 3) # blue = fish measurement
            
            plottableCoord = (int(predictedCoord[0]), int(predictedCoord[1]))

            cv2.circle(img, plottableCoord, 3, [0,0,0], 3) # black = predicted velocity
            cv2.putText(img, str(id), (plottableCoord[0]-30, plottableCoord[1] + 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

        cv2.imshow("cropped", img)
        cv2.waitKey(1)



if __name__ == '__main__':
    frame = r"C:\Users\ginar\OneDrive\Documents\robot-fish-lure-code-refactor\videos\background.png"
    vp = velocityPredictor(frame)
    vp.assignIDs([[[1, 1, 2, 100, 1, 1], [2, 50, 40, 100, 1, 1], [3, 300, 400, 100, 1, 1]], [[1, 5, 5, 200, 1, 1], [2, 55, 45, 200, 1, 1], [3, 305, 405, 200, 1, 1]]],  [[10, 10, 200, 1, 1], [60, 50, 200, 1, 1], [310, 410, 200, 1, 1]])