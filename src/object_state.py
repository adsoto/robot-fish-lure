import numpy as np
import serial
import time
from point_tracker import track_point
from paths import *
import data_handler as dh
import matplotlib.pyplot as plt
import video_processor as vp
import lure as lure
import centroidTracker 


class Object: 
    _state = None #does this do anything? 

    def __init__(self, t, x, y, theta):
        self.t = t
        self.x = x
        self.y = y
        self.theta = theta


    def distance_to(self, X):
        """calculates distance between self and object X"""
        x_mid = np.square(self.x - X.x)
        y_mid = np.square(self.y - X.y)
        distance = np.sqrt(x_mid+y_mid)
        return distance
    




    
