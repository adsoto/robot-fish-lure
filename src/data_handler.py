import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

class DataHandler():
    """Class to plot and/or save arbitrary data series"""

    def __init__(self, plot=True, save=True): #save_dual=True
        self._plot = plot
        self._save = save
        #self._save_dual = save_dual
        self._data = {}
        self._dualdata = {}

    def add_series(self, name, ind, dep, xlabel, ylabel):
        """Adds a new data series to the DataHandler dictionary of data series
        
        Series should take the form of an array with the independent variable, 
        an array with the corresponding dependent variable, and the labels for the plot"""

        new_series = Series(ind, dep, xlabel, ylabel)
        self._data[name] = new_series

    def add_dual_series(self, name, ind1, dep1, ind2, dep2, xlabel, ylabel):
        self._dualdata[name] = (ind1, dep1, ind2, dep2, xlabel, ylabel)

    def add_triple_series(self, name, ind1, dep1, ind2, dep2, ind3, dep3, xlabel, ylabel):
        self._tripledata[name] = (ind1, dep1, ind2, dep2, ind3, dep3, xlabel, ylabel)

    def make_plots(self):
        """Produces plots for each of the data series"""

        for index, name in enumerate(self._data):
            series = self._data[name]
            plt.figure(index)
            plt.scatter(series._ind, series._dep, label=name)
            plt.xlabel(series._xlabel)
            plt.ylabel(series._ylabel)
            plt.legend(loc="upper left")
            plt.axis('scaled')
        plt.show()

    def make_dual_plots(self):
        #fig = plt.figure()
        #ax1 = fig.add_subplot(111)
        for index, name in enumerate(self._dualdata):
            series = self._dualdata[name]
            plt.figure(index)
            plt.scatter(series[0], series[1], label = name)
            plt.scatter(series[2], series[3])
            plt.xlabel(series[4]) #check
            plt.ylabel(series[5]) #check
            plt.legend(["Desired", "Actual"])
            if name == 'Position':
                plt.ylim(-0.1, 0.5)
                #plt.axis('square')
            plt.title(label=name, loc="left")
        plt.show()
    """
    def make_triple_plots(self):
        #fig = plt.figure()
        #ax1 = fig.add_subplot(111)
        for index, name in enumerate(self._tripledata):
            series = self._tripledata[name]
            plt.figure(index)
            plt.scatter(series._ind1, series._dep1, label = name)
            plt.scatter(series._ind2, series._dep2, label = name)
            plt.scatter(series._ind3, series._dep3, label = name)
            plt.xlabel(series._xlabel) #check
            plt.ylabel(series._ylabel) #check
            plt.legend(["Desired", "Actual", "Error"])
            if name == 'Position':
                plt.ylim(-0.1, 0.5)
                #plt.axis('square')
            plt.title(label=name, loc="left")
        plt.show()
    """

    def save_data(self):
        """Saves all data series to the data directory"""

        now = datetime.now()
        data_folder = 'data/' + now.strftime("%m.%d.%Y/")
        data_filename = 'data/' + now.strftime("%m.%d.%Y/%H.%M") + '.csv'

        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        
        data = {}
        for name, series in self._data.items():
            data[name + '_ind'] = series._ind
            data[name + '_dep'] = series._dep

        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()
        df.to_csv(data_filename, index=False)
    """
    ## holly added to save data in the add_dual_series format
    def save_data_dual(self):
        

        now = datetime.now()
        data_folder = 'data/' + now.strftime("%m.%d.%Y/")
        data_filename = 'data/' + now.strftime("%m.%d.%Y/%H.%M") + '.csv'

        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        
        data = {}
        for name, series in self._dualdata.items():
            data[name + '_ind1'] = series._ind1
            data[name + '_dep1'] = series._dep1
            data[name + '_ind2'] = series._ind2
            data[name + '_dep2'] = series._dep2

        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()
        df.to_csv(data_filename, index=False)
    """

    def run(self):
        if self._plot: self.make_plots()
        if self._plot: self.make_dual_plots()
        if self._save: self.save_data()
        #if self._save_dual: self.save_data_dual()

class Series():
    """Class definition for data series"""

    def __init__(self, ind, dep, xlabel, ylabel):
        self._ind = ind
        self._dep = dep
        self._xlabel = xlabel
        self._ylabel = ylabel

if __name__ == '__main__':
    time = [1, 2, 3, 4, 5, 6, 7, 8]
    robot_x = [1, 1, 1, 1, 2, 2, 2, 2]
    robot_y = [2, 2, 2, 2, 3, 3, 4, 4]
    robot_theta = [0, 0, 0, 0, 1, 1, 0, 1]

    v = np.linalg.norm(np.diff(np.array([robot_x, robot_y])), axis=0)/np.diff(time)
    w = np.diff(robot_theta)/np.diff(time)

    dl = DataHandler(True, True)
    dl.add_series('robot position', robot_x, robot_y, 'x pos', 'y pos')
    dl.add_series('robot velocity', time[1:], v, 'time', 'velocity')
    dl.add_series('angular velocity', time[1:], w, 'time', 'ang. velocity')
    dl.run()
