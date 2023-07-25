"""Plot velocities!"""
import pandas as pd
import VelocityTracker as vt
from datetime import *
import matplotlib.pyplot as plt
import os

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

if __name__ == '__main__':

    plotter = Plotter(11) # input the number of fish in the video! -- input length +1 becuase of zeor indexing
    
    bigcsv = plotter.read_bigcsv('/Users/loaner/Downloads/total_data_set14.54 - Sheet1-2.csv')
    print(bigcsv)

    # creates a smart list of how many fish we have, then creates a series of all of the things we want
    yvelaxis = plotter.allfish_axis("Yvelocity")   # creates a list of all of the Y position columns for easy graphing
    xvelaxis = plotter.allfish_axis("Xvelocity")   # same thing, in X direction

    print(yvelaxis)
    # vY versus time -- alpha is the opacity constant
   
    bigcsv.plot.line(x="Time", y=yvelaxis, alpha=1)     # plots yvelocity versus time for all fish
    plt.title("Y Velocity of Fish Over Time")
    plt.xlabel("Time (sec)")
    plt.ylabel("Velocity (m/s)")
    plt.legend(loc='upper center', bbox_to_anchor=(1.1, 1.016), ncol=1, prop = { "size": 7})
    plt.tight_layout()

    bigcsv.plot.line(x="Time", y=xvelaxis, alpha=1) # plots xvelocity versus time for all fish\ 
    plt.title("X Velocity of Fish Over Time")
    plt.xlabel("Time (sec)")
    plt.ylabel("Velocity (m/s)")
    plt.legend(loc='upper center', bbox_to_anchor=(1.1, 1.016), ncol=1, prop = { "size": 7})
    plt.tight_layout()

    # FOR POSITIONS - overlays different lines together!
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
    
    # set the legend for multiple plots
    positions.legend(['Fish1', 'Fish2', "Fish3", "Fish4", "Fish5", "Fish6", "Fish7", "Fish8", "Fish9", "Fish10"], prop = { "size": 7}, loc ="upper right")

    # set title of plot
    positions.set_title('Postions')
    positions.set_xlabel('Fish X Position (m)')
    positions.set_ylabel('Fish Y Position (m)')
    positions.set_ylim(0, 0.75) # match the tank 
    positions.set_xlim(0, 0.9 ) # match the tank
    plt.show()