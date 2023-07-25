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
from datetime import datetime
import object_state
import os
import csv
import pandas as pd


class DataLogger:  

    def __init__(self, plot=True, save=True): #save_dual=True #should this include data_filename etc??
        self._plot = plot
        self._save = save
        #self._save_dual = save_dual
        self._robot = {}
        self._fish = {}
        self._desired = {}
        self._distances = {}
    
    def create_file(self): #should this be part of the initializer?? 
        #gets time and date and checks for existing file etc.
        now = datetime.now()
        data_folder = 'data/' +'backup/'+ now.strftime("%m.%d.%Y/") 
        data_filename = 'data/' + 'backup/' + now.strftime("%m.%d.%Y/%H.%M") + '.csv'


        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        field_names = {'Robot': [],
        'Fish': [],
        'Desired': [],
        'Distances': []
        }

        df = pd.DataFrame(field_names)
        df.to_csv(data_filename, index=False)


    def log_data(self, robot_state, fish_state, desired_state, distance):
        robot_string = robot_state.to_string()
        if fish_state:
            fish_string = fish_state.to_string()
            distance_string = distance
        else: 
            fish_string = str()
            distance_string = str()
        desired_string = desired_state.to_string()

        now = datetime.now()
        data_filename = 'data/'+ 'backup/'+ now.strftime("%m.%d.%Y/%H.%M") + '.csv'

        df = pd.read_csv(data_filename)
  
        # updating the column value/data
        df.loc[len(df.index)] = [robot_string, fish_string, desired_string, distance_string] 
  
        # writing into the file
        df.to_csv(data_filename, index=False)
        

    def close_logger(self):
        #closes logger?
        pass