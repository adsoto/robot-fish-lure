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
        return(poslist[frame][0])
    
    def getYposition(self, poslist, frame):
        # extracts the x positions of a particular fish in a particular frame from the dictioanry of fish positions and times
        # fishlist = self.get_fish_positions(fishlist, fish) # returns as: [time1 , fish1 X1, fish1 Y1], [time2 , fish1 X2, fish1 Y2]
        return(poslist[frame][1])
    
    def getTime(self, poslist, frame):
        return (poslist[frame][2])

    def xVelocity(self,x1, x2, timestep):
        return float((x2-x1)/timestep)

    def yVelocity(self,y1, y2, timestep):
        return float((y2-y1)/timestep)
    
    def fw_vel_est(self, poslist, frame):
        # computes a forward estimation velocity 
        futureframe = frame+1
        t_current = self.getTime(poslist,frame)

        t_diff = self.getTime(poslist,futureframe) - self.getTime(poslist,frame)
        x_current = self.getXposition(poslist, frame)
        x_future = self.getXposition(poslist, futureframe)

        y_current = self.getYposition(poslist, frame)
        y_future = self.getYposition(poslist, futureframe)

        xvel = self.xVelocity(x_current, x_future,t_diff)
        yvel = self.yVelocity(y_current, y_future, t_diff)

        addvel = [round(xvel, 4), round(yvel, 4)]
        return addvel
    
    def bw_vel_est(self, poslist, frame):
        # computes a backwards referenced velocity estimation
        pastframe = frame-1
        t_diff = self.getTime(poslist,frame) - self.getTime(poslist,pastframe)
        t_current = self.getTime(poslist,frame)

        x_current = self.getXposition(poslist, frame)
        x_past = self.getXposition(poslist, pastframe)

        y_current = self.getYposition(poslist, frame)
        y_past = self.getYposition(poslist, pastframe)

        xvel = self.xVelocity(x_past, x_current,t_diff)
        yvel = self.yVelocity(y_past, y_current,t_diff)

        addvel = [round(xvel, 4), round(yvel, 4)]
        return addvel

    def center_vel_est(self, poslist, frame):
        # computes center estimation for velocity
        futureframe = frame+1
        pastframe = frame-1
        t_current = self.getTime(poslist,frame)

        t_past = self.getTime(poslist, pastframe)
        t_future = self.getTime(poslist,futureframe)
        t_diff = t_future-t_past

        x_future = self.getXposition(poslist, futureframe)
        x_past = self.getXposition(poslist, pastframe)
    
        y_future = self.getYposition(poslist, futureframe)
        y_past = self.getYposition(poslist, pastframe)

        xvel = self.xVelocity(x_past, x_future,t_diff)
        yvel = self.yVelocity(y_past, y_future, t_diff)
        addvel = [round(xvel, 4), round(yvel, 4)]
        return addvel

    def run(self):
        newFishDict = self._fishdict
        for fish in newFishDict: # iterates over each id in the dictionary
            
            fishkey = newFishDict[fish] 
            #print()
            vel_list = []
            # frame conditional for the end of the list

            for frame in list(range(len(fishkey))):
                frame = int(frame)
                futureframe = frame+1
                pastframe = frame-1
                current_stat = fishkey[frame]

                if pastframe == -1 and frame == 0:    # computes forwards estimation for the first datapoint in the set
                    addvel = self.fw_vel_est(fishkey, frame)
                    current_stat.append(addvel[0])
                    current_stat.append(addvel[1])

                print("frame",frame)
                print("fishkey",len(fishkey))

                if frame == (len(fishkey)-1) :   # compute backwards estimation for the last datapoint in the set
                    print(len(fishkey))
                    addvel = self.bw_vel_est(fishkey, frame)
                    current_stat.append(addvel[0])
                    current_stat.append(addvel[1])

                else:    # otherwise, compute a normal, center estimation for velocity
                    addvel = self.center_vel_est(fishkey, frame)
                    current_stat.append(addvel[0])
                    current_stat.append(addvel[1])

                    # print("time:", time_current, "fish num:", fish)
                    # print("the x velocity is:", round(xvel, 4), 'the y velocity is:', round(yvel, 4))

            self._fishdict = newFishDict
        return(self._fishdict)


if __name__ == '__main__':
    fishdict =  {
        # t, x, y, vx, vy
                  1:  [[1 , 10, 30],  [30 , 100, 300], [55 , 1000, 5000], [77 , 10000, 20000]], 
                  2:  [[1 , 20, 50],  [30 , 200, 500], [55, 2000, 7000],  [77 , 20000, 40000]], 
                  3:  [[1 , 30, 90],  [30 , 300, 700], [55, 3000, 9000],  [77 , 30000, 50000]],
                  4:  [[1 , 40, 120], [30 , 400, 900], [55 , 4000, 1200], [77 , 40000, 70000]], 
                 }

    # fish: time in frames, x, y
   
    cv = CalcVelocity(fishdict)
    # fishkey = fishdict[1]
    # for frame in list(range(len(fishkey))):
    #     current_stat = fishkey[frame]
    #     current_stat.append(19)
    #     print(current_stat)
        
    # print(fishkey)

    updatedfish_dict = cv.run()
    print(updatedfish_dict)
