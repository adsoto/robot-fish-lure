import numpy as np
import serial
import time
from point_tracker import track_point
from paths import *
import data_handler as dh
import matplotlib.pyplot as plt
import video_processor as vp
import lure as lure
import fishTracker 




def get_robot_state(t):
    [head, tail] = lure.get_coords(2)
    fish_vect = head - tail
    theta = np.arctan2(fish_vect[1], fish_vect[0])
    robot_pos = (head + tail)/2

