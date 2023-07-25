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
print(fish)

test = os.Object(1, 2, 3, 4)
print(test)
print(type(test))
test2 = test.to_string()
print(test2)
test3 = os.to_object(test2)
print(test3)
test4 = test.to_string()
print(test4)
print(type(test4))