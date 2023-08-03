"""Plot velocities!"""
import pandas as pd
import VelocityTracker as vt
from datetime import *
import matplotlib.pyplot as plt
import os
import VelocityTracker as vt
import VelocityHandler as vh
import fishTracker as ft
import numpy as np

class Plotter:
    def __init__(self, numfish):
        self._numfish = numfish

    def read_indivcsv(self, filename):
        df = pd.read_csv(filename) # read csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder
        return df
    
    def read_bigcsv(self, filename):  # also need to import robot position
        bigdata = pd.read_csv(filename)# read BIG csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder
        return bigdata
    
    def allfish_axis(self, name):
        # creates a list of columns to plot for al fishh. ex: finds the x positions of all fish and outputs a list to plot them
        axisplot = []
        for i in list(range(1,self._numfish)):
            axisplot += [name + str(i)]
        return axisplot
    
    def displayplots(self,robotposition, bigcsv):
        robo_pos_x = robotposition['Actual X-Pos vs. Time: x (m)']
        robot_pos_y = robotposition['Actual Y-Pos vs. Time: y (m)']

        # creates a dynamic list of how many fish we have, then creates a series of all of the things we want
        yvelaxis = self.allfish_axis("Yvelocity")   # creates a list of all of the Y position columns for easy graphing
        xvelaxis = self.allfish_axis("Xvelocity")   # same thing, in X direction
    
        # Plot settings for Velocity X versus time -- alpha is the opacity constant
        bigcsv.plot.line(x="Time1", y=xvelaxis, alpha=1) # plots xvelocity versus time for all fish\ 
        plt.title("X Velocity of Fish Over Time")
        plt.xlabel("Time (sec)")
        plt.ylabel("Velocity (m/s)")
        plt.legend(loc='upper center', bbox_to_anchor=(1.1, 1.016), ncol=1, prop = { "size": 7})
        plt.tight_layout()

        # Plot settings for Velocity Y versus time -- alpha is the opacity constant
        bigcsv.plot.line(x="Time1", y=yvelaxis, alpha=1)     # plots yvelocity versus time for all fish
        plt.title("Y Velocity of Fish Over Time")
        plt.xlabel("Time (sec)")
        plt.ylabel("Velocity (m/s)")
        plt.legend(loc='upper center', bbox_to_anchor=(1.1, 1.016), ncol=1, prop = { "size": 7})
        plt.tight_layout()

        # FOR POSITIONS - overlays different lines together! 
        # cannot use a smart list function here, since each X must be plotting against its own corresponding Y
        fig, positions = plt.subplots()
        line1 = positions.plot(bigcsv['Xpositions1'], bigcsv['Ypositions1'])
        line2 = positions.plot(bigcsv['Xpositions2'], bigcsv['Ypositions2'])
        line3 = positions.plot(bigcsv['Xpositions3'], bigcsv['Ypositions3'])
        line4 = positions.plot(bigcsv['Xpositions4'], bigcsv['Ypositions4'])
        line5 = positions.plot(bigcsv['Xpositions5'], bigcsv['Ypositions5'])
        line6 = positions.plot(bigcsv['Xpositions6'], bigcsv['Ypositions6'])
        line7 = positions.plot(bigcsv['Xpositions7'], bigcsv['Ypositions7'])
        line8 = positions.plot(bigcsv['Xpositions8'], bigcsv['Ypositions8'])
        line9 = positions.plot(bigcsv['Xpositions9'], bigcsv['Ypositions9'])
        line10 = positions.plot(bigcsv['Xpositions10'], bigcsv['Ypositions10'])
        line11 = positions.plot(robo_pos_x, robot_pos_y, color='k', linestyle='dashed', alpha = 1) # displays the robot position in black
        
        # Position plot settings
        positions.set_title('Postions')
        positions.legend(['Fish1', 'Fish2', "Fish3", "Fish4", "Fish5", "Fish6", "Fish7", "Fish8", "Fish9", "Fish10", "Robot"], prop = { "size": 7}, loc ="upper right")
        positions.set_xlabel('Fish X Position (m)')
        positions.set_ylabel('Fish Y Position (m)')
        positions.set_ylim(0.05, 0.3) # match the tank 
        positions.set_xlim(0, 0.6 ) # match the tank

        plt.show() # displays all plots

    def displayspeedplot():
        return

if __name__ == '__main__':

    robotcsv = r"C:\Users\ginar\OneDrive\Documents\robot-fish-lure-code-refactor\src\7.17.23 - 16.28.csv" # CHANGE THIS!!!

    #fishdict =  {
        # t, x, y, vx, vy
                #   1:  [[1 , 10, 30],  [30 , 100, 300], [55 , 1000, 5000], [77 , 10000, 20000]], 
                #   2:  [[1 , 20, 50],  [30 , 200, 500], [55, 2000, 7000],  [77 , 20000, 40000]], 
                #   3:  [[1 , 30, 90],  [30 , 300, 700], [55, 3000, 9000],  [77 , 30000, 50000]],
                #   4:  [[1 , 40, 120], [30 , 400, 900], [55 , 4000, 1200], [77 , 40000, 70000]], 
                #   5:  [[1 , 20, 50],  [30 , 200, 500], [55, 2000, 7000],  [77 , 20000, 40000]], 
                #   6:  [[1 , 30, 90],  [30 , 300, 700], [55, 3000, 9000],  [77 , 30000, 50000]],
                #   7:  [[1 , 40, 120], [30 , 400, 900], [55 , 4000, 1200], [77 , 40000, 70000]], 
                #   8:  [[1 , 10, 30],  [30 , 100, 300], [55 , 1000, 5000], [77 , 10000, 20000]], 
                #   9:  [[1 , 10, 30],  [30 , 100, 300], [55 , 1000, 5000], [77 , 10000, 20000]], 
                #   10:  [[1 , 10, 30],  [30 , 100, 300], [55 , 1000, 5000], [77 , 10000, 20000]], 

                #  }

    # fishdict = ft.run

    plotter = Plotter(11) # input the number of fish in the video! -- input length +1 becuase of zero indexing

    # creates time and position dictionary
    #something here from fishtracker about getting dictionary!

    foregroundpath = r"C:\Users\ginar\OneDrive\Documents\robot-fish-lure-code-refactor\src\use_for_velocities (online-video-cutter.com).mp4"
    backgroundPath = r"C:\Users\ginar\OneDrive\Documents\robot-fish-lure-code-refactor\src\background.png"
    camera_bounds = np.array([[570,  300], [1450, 820]]) # find these with calibrate_setup.pyq
    ft = ft.fishTracker(foregroundpath, backgroundPath, camera_bounds)
    fishdict = ft.getFishDict()
    print("dict", fishdict)
    
    # sends time and position dictionary to calculate velocity in velocitytracker.py
    vt = vt.CalcVelocity(fishdict) # takes self, fishdict
    vel_fishdict = vt.run() # creating the velocity dictionary in velocitytracker.py

    # sends velocity dictionary into velocity hander to write out data into different dataframes, saves locally
    vh = vh.VelocityHandler(vel_fishdict) # takes self, velocitydict
    megadata_filename = vh.run() # writes out dataframes by running velocityhandler.py, outputs the bigCSV filename

    bigcsv = plotter.read_bigcsv(megadata_filename) # input the fish file we want to read!
    print(bigcsv) # checks that this was imported correctly

    print("nonee???", robotcsv)
    robotposition = plotter.read_indivcsv(robotcsv) #input the robot file we want to read!
    print(robotposition) # checks that this was imported correctly

    print("done!")
    plotter.displayplots(robotposition, bigcsv)
    
