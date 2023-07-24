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
    
    def read_bigcsv(self, filename):
        bigdata = pd.read_csv(filename)# read BIG csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder
        return bigdata
    
    def allfish_axis(self, name):
        # creates a list of columns to plot for al fishh. ex: finds the x positions of all fish and outputs a list to plot them
        axisplot = []
        for i in list(range(1,self._numfish)):
            axisplot += [name + str(i)]
        return axisplot

    # def createplots(self,x):
        
    #     fig, (ax1, ax2) = plt.subplots(1, 2)
    #     fig = plt.figure()
    #     gs = fig.add_gridspec(3, hspace=0)
    #     # axs = gs.subplots(sharex=True, sharey=True)

    #     fig.suptitle("Fish" + str(x) +' ' + "X and Y position versus time")
    #     ax1.plot(dataframe["Time"], dataframe["Xpositions"])
    #     ax2.plot(dataframe["Time"], dataframe["Ypositions"])
    #     plt.show()
        # plt.title("Fish" +str(x) + ' ' + "X position v. Time", fontdict=None, loc='center', pad=None )
        # plt.plot()
        # plt.plot()


        # plt.title("Fish" +str(x) + ' ' + "Position Graph" , fontdict=None, loc='center', pad=None )
        # plt.plot(dataframe["Xpositions"], dataframe["Ypositions"])

        # plt.show()

if __name__ == '__main__':

    plotter = Plotter(5) # input length +1 becuase of zeor indexing
    bigcsv = plotter.read_bigcsv('/Users/loaner/Documents/GitHub/robot-fish-lure/data/07.24.2023/total_data_set14.54.csv')
    print(bigcsv)

    # creates a smart list of how many fish we have, then creates a series of all of the things we want
    yvelaxis = plotter.allfish_axis("Ypositions")   # creates a list of all of the Y position columns for easy graphing
    xvelaxis = plotter.allfish_axis("Xpositions")   # same thing, in X direction

    print(yvelaxis)
    # vY versus time
    bigcsv.plot.line(x="Time1", y=yvelaxis, alpha=0.5)
    bigcsv.plot.line(x="Time1", y=xvelaxis, alpha=0.5)

    plt.show()

    #vX versus time

    # 