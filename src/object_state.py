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
    
    def to_string(self): #should this maybe be a list? 
        if self:
            t_string = str(self.t)
            x_string = str(self.x)
            y_string = str(self.y)
            theta_string = str(self.theta)
            object_string = t_string+ ',' + x_string+ ',' + y_string + ',' +theta_string
            #object_list = t_string + x_string + y_string + theta_string
            return object_string
        else:
            return str() 
    
    
def to_object(string): #not a part of the Object class because it takes in a string
    list2 = list(string.split(","))
    t = list2[0]
    x = list2[1]
    y = list2[2]
    theta = list2[3]
    new_object = Object(t,x,y,theta)
    return new_object






    
