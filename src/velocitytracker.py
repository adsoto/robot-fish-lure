import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tracker import *


# import lure as lure

PIX2METERS = .635/820 # meters/pixels conversion
FPS = 10


class CalcVelocity:

    def __init__(self, fishdict):
        self._fishdict = fishdict
    
    def getposlist(self, fishdict, fish):
        # returns list of time and positions for fish i
        return fishdict[fish][0]
      
    def getXposition(self,poslist, frame):
        # extracts the x positions of a particular fish in a particular frame from the dictioanry of fish positions and times
        # fishlist = self.get_fish_positions(fishlist, fish) # returns as: [time1 , fish1 X1, fish1 Y1], [time2 , fish1 X2, fish1 Y2]
        return(poslist[frame][1])
    
    def getYposition(self, poslist, frame):
        # extracts the x positions of a particular fish in a particular frame from the dictioanry of fish positions and times
        # fishlist = self.get_fish_positions(fishlist, fish) # returns as: [time1 , fish1 X1, fish1 Y1], [time2 , fish1 X2, fish1 Y2]
        return(poslist[frame][2])
    
    def getTime(self, poslist, frame):
        return (poslist[frame][0])

    def xVelocity(self,x1, x2, timestep):
        return float((x2-x1)/timestep)

    def yVelocity(self,y1, y2, timestep):
        return float((y2-y1)/timestep)
    
    def fw_vel_est(self, poslist, frame):
        # computes a forward estimation velocity 
        futureframe = frame+1
        t_current = cv.getTime(poslist,frame)

        t_diff = cv.getTime(poslist,futureframe) - cv.getTime(poslist,frame)
        x_current = cv.getXposition(poslist, frame)
        x_future = cv.getXposition(poslist, futureframe)

        y_current = cv.getYposition(poslist, frame)
        y_future = cv.getYposition(poslist, futureframe)

        xvel = cv.xVelocity(x_current, x_future,t_diff)
        yvel = cv.yVelocity(y_current, y_future, t_diff)

        addvel = [round(xvel, 4), round(yvel, 4), t_current]
        return addvel
    
    def bw_vel_est(self, poslist, frame):
        # computes a backwards referenced velocity estimation
        pastframe = frame-1
        t_diff = cv.getTime(poslist,frame) - cv.getTime(poslist,pastframe)
        t_current = cv.getTime(poslist,frame)

        x_current = cv.getXposition(poslist, frame)
        x_past = cv.getXposition(poslist, pastframe)

        y_current = cv.getYposition(poslist, frame)
        y_past = cv.getYposition(poslist, pastframe)

        xvel = cv.xVelocity(x_past, x_current,t_diff)
        yvel = cv.yVelocity(y_past, y_current,t_diff)

        addvel = [round(xvel, 4), round(yvel, 4), t_current]
        return addvel

    def center_vel_est(self, poslist, frame):
        # computes center estimation for velocity
        futureframe = frame+1
        pastframe = frame-1
        t_current = cv.getTime(poslist,frame)

        t_past = cv.getTime(poslist, pastframe)
        t_future = cv.getTime(poslist,futureframe)
        t_diff = t_future-t_past

        x_future = cv.getXposition(poslist, futureframe)
        x_past = cv.getXposition(poslist, pastframe)
    
        y_future = cv.getYposition(poslist, futureframe)
        y_past = cv.getYposition(poslist, pastframe)

        xvel = cv.xVelocity(x_past, x_future,t_diff)
        yvel = cv.yVelocity(y_past, y_future, t_diff)
        addvel = [round(xvel, 4), round(yvel, 4), t_current]
        return addvel

    def run(self):
        newFishDict = self._fishdict
        for fish in newFishDict:
            
            fishkey = newFishDict[fish]
            poslist = cv.getposlist(newFishDict, fish) 
            #print()
            vel_list = []

            # frame conditional for the end of the list

            for frame in range(len(poslist)-1):
                frame = int(frame)
                futureframe = frame+1
                pastframe = frame-1

                if pastframe == -1:    # computes forwards estimation for the first datapoint in the set
                    addvel = cv.fw_vel_est(poslist, frame)
                    vel_list.append(addvel)

                if frame == (len(poslist)):   # compute backwards estimation for the last datapoint in the set
                    addvel = cv.bw_vel_est(poslist, frame)
                    vel_list.append(addvel)

                else:    # otherwise, compute a normal, center estimation for velocity
                    addvel = cv.center_vel_est(poslist, frame)
                    vel_list.append(addvel)

                    # print("time:", time_current, "fish num:", fish)
                    # print("the x velocity is:", round(xvel, 4), 'the y velocity is:', round(yvel, 4))

            newFishDict[fish].append(vel_list)

            self._fishdict = newFishDict
        return(self._fishdict)


if __name__ == '__main__':

    # fishlist =  [
    #     # t, x, y
    #               [[1 , 10, 30],  [30 , 100, 300], [55 , 1000, 5000], [77 , 10000, 20000]], 
    #               [[1 , 20, 50],  [30 , 200, 500], [55, 2000, 7000],  [77 , 20000, 40000]], 
    #               [[1 , 30, 90],  [30 , 300, 700], [55, 3000, 9000],  [77 , 30000, 50000]],
    #               [[1 , 40, 120], [30 , 400, 900], [55 , 4000, 1200], [77 , 40000, 70000]]
    # ]

    fishdict =  {
        # t, x, y
                  'f1':  [[[1 , 10, 30],  [30 , 100, 300], [55 , 1000, 5000], [77 , 10000, 20000]], ], 
                  'f2':  [[[1 , 20, 50],  [30 , 200, 500], [55, 2000, 7000],  [77 , 20000, 40000]], ], 
                  'f3':  [[[1 , 30, 90],  [30 , 300, 700], [55, 3000, 9000],  [77 , 30000, 50000]], ],
                  'f4':  [[[1 , 40, 120], [30 , 400, 900], [55 , 4000, 1200], [77 , 40000, 70000]], ], 
                 }

    # fish: time in frames, x, y
   
    cv = CalcVelocity(fishdict)

    vel_return = cv.run()
    print(vel_return)
