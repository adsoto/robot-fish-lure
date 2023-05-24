import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

class DataHandler():
    """Class to plot and/or save arbitrary data series"""

    def __init__(self, plot=True, save=True):
        self._plot = plot
        self._save = save
        self._data = {}

    def add_series(self, name, ind, dep, xlabel, ylabel):
        """Adds a new data series to the DataHandler dictionary of data series
        
        Series should take the form of an array with the independent variable, 
        an array with the corresponding dependent variable, and the labels for the plot"""

        new_series = Series(ind, dep, xlabel, ylabel)
        self._data[name] = new_series

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

    def run(self):
        if self._plot: self.make_plots()
        if self._save: self.save_data()

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
