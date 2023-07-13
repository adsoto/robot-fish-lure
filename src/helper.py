import numpy as np
import serial
import time
#from point_tracker import track_point
from paths import *
import data_handler as dh
import matplotlib.pyplot as plt
import video_processor as vp
import lure as lure
import centroidTracker 
import object_state as os
from positions_in_tank import *
import make_traj_pts


robot = os.Object(2, 3, 4, 0)
fish = os.Object(2, 5, 7, 2.3)

thetatry=fish.theta

robotcoords = (robot.x, robot.y)
fishcoords = (fish.x, fish.y)

#r2fish = robotcoords-fishcoords

distance = robot.distance_to(fish)

print(distance)
print(thetatry)
print(robotcoords)


x = np.array((2,3))
y = np.array((4,5))

dist=np.linalg.norm(x-y)
print(dist)

A_x = A[0]
A_y = A[1]
B_x = B[0]
B_y = B[1]

start_pos = np.array([0,0])
start_time = 0
dt = 1
start_theta = -np.pi/2

Bxdist = np.square(B_x - A_x)
Bydist = np.square(B_y-A_y)
B_rob_dist = np.sqrt(Bxdist+Bydist)
dist = B_rob_dist
traj_t = make_traj_pts.straight_traj(dist, 0.05, 1, start_pos, 0)