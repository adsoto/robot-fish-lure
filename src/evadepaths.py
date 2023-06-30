"""file defines the pathbounds of the new evasion path, also defines the fish radius
sends different paths to controller based on the position and robot + fish"""
import math
import random
import numpy as np
import controller
import convert
import orange
import math
import centroidTracker as ct
import cv2

# from controller import robot_pos

#DELETE THESE
#LAIR 
#X DIR CONVERSTIONS
xoff = 574
xslope = 1151

#Y DIR CONVERSIONS
yoff = 762
yslope = (-1156)

class evadePaths:

    def __init__(self, camera_port, camera_bounds, save_video):
        self._cap = cv2.VideoCapture(camera_port)
        self._port = camera_port
        self._go = True # not implemented
        self._bounds = camera_bounds
        self._current_frame = None
        self._video = orange.VideoProcessor(camera_port, camera_bounds, save_video)


    def xpxtomet(xpix):
        xadjust = xpix - xoff  # accounts for offset in px - origin on the left side of the tank
        x_met = ((xadjust/xslope) + 0.49) # adjust origin to lower left IN METERS
        return x_met

    def ypxtomet(ypix):
        yadjust = ypix - yoff # accounts for offset in px and moves origin to lower left corner or tank
        y_met = ((yadjust/yslope) - 0.3)  # adjust  origin to lower left IN METERS
        return y_met

    def ymettopx(ymet):
        y_px = (ymet+0.3) * yslope
        yadjust = y_px + yoff
        return yadjust

    def xmettopx(xmet):
        x_px = (xmet -0.49) * xslope
        xadjust = x_px + xoff
        return xadjust

    def createbounds(self, bounds):
        # CONVERT TO MET TO MATCH PATHS AND robot_pos
        x1_met = convert.xpxtomet(float(bounds[0][0]))
        y1_met = convert.ypxtomet(float(bounds[0][1]))
        x2_met = convert.xpxtomet(float(bounds[1][0]))
        y2_met = convert.ypxtomet(float(bounds[1][1]))
        return x1_met, y1_met, x2_met, y2_met

    def createcorners(self, x1_met,y1_met,x2_met,y2_met): # PASS METER VALUES HERE
        """creates corners of the tank for the robot to search in -- reassigns origin to lower left corner, matching robot position in meters"""

        height_met = abs(y2_met - y1_met) # 13in ish - good
        width_met= abs(x2_met - x1_met)  # 27.25in ish - good
        x1_met = 0 # sets left wall to be x = 0
        y1_met = height_met
        x2_met = width_met
        y2_met = 0 #set the bottom to be y = 0
        listcorners = [[0,0], [0,y1_met], [x2_met,y1_met], [x2_met,0]]
        return listcorners #in meters!!!

    def cornerdist(self, robot_pos, listofcorners):
        distlist = []
        mindist = 10000 #arbitrary
        for i in listofcorners:
            dist = [i,math.dist(robot_pos, i)]
            distlist += [dist]
        return distlist

    def runevadepaths(self):
        # tankboundspx = controller.bounds
        bounds = ([[ 687 ,396],[1483 ,801]])
        tankboundspx = bounds
        #vp = orange.VideoProcessor(self._port, self._bounds, True)
        [head, tail] = self._video.get_coords(2)
        robot_pos = (head + tail)/2
    
        print(robot_pos)
        # robot_x_met = robot_pos[0] #calls robot pos from controller
        # robot_y_met = robot_pos[1] #calls robot pos from controller
        cenTracker = ct.centroidTracker(self._port, self._bounds, True)
        # findNeighbor = cenTrack.ct.findClosestNeighbor()
        fishDist = cenTracker.findClosestNeighbor(robot_pos)
        #lurecoords = cenTrack.ct.findClosestNeighbor(robot_pos)
        #fishdist = math.dist(robot_pos, lurecoords)

        x1_met, y1_met, x2_met, y2_met = self.createbounds(tankboundspx)
        listcorners = self.createcorners(x1_met, y1_met, x2_met, y2_met)
        distlist = self.cornerdist(robot_pos, listcorners)

        self._go  = False

    #     print("robot position:", robot_pos, "lure position:", lurecoords) 

    #     if 0 <= robot_x_met <= 0.05 and 0 <= robot_y_met <= 0.05:
    #         print("check for fish in bottom left corner")
    #     if fishdist <= 0.1:
    #         print("fish is in lower left corner --> run away!!!")

    #     if 0 <= robot_x_met <= 0.05  and  0.3 <= robot_y_met <= 0.35:
    #         print("check for fish in top left corner")
    #     if fishdist <= 0.1:
    #         print("fish is in bottom left corner --> run away!!!")

    #     if 0.64 <= robot_x_met <= 0.69  and  0.3 <= robot_y_met <= 0.35:
    #         print("check for fish in top right corner")
    #     if fishdist <= 0.1:
    #         print("fish is in top right corner --> run away!!!")

    #     if 0.64 <= robot_x_met <= 0.69  and  0 <= robot_y_met <= 0.05:
    #         print("check for fish in bottom right corner")
    #     if fishdist <= 0.1:
    #         print("fish is in bottom right  corner --> run away!!!")

    #     print()
    #     print(listcorners)

    def is_go(self):
        return self._go

if __name__ == '__main__':
    camera_index = 0
    #cap = cv2.VideoCapture(foregroundPath)
    #ret, frame = cap.read()
    camera_bounds = np.array([[467, 382], [1290, 862]]) # find these with calibrate_setup.py
    ep = evadePaths(camera_index, camera_bounds, False)
    while True:
        ep.runevadepaths()
        if not ep.is_go(): break
