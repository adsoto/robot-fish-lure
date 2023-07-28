
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button


# referenced: https://www.tutorialspoint.com/how-to-plot-csv-data-using-matplotlib-and-pandas-in-python on 6/12/23
# https://www.statology.org/pandas-plot-multiple-series/ on 6/13/23
# https://stackoverflow.com/questions/44970881/matplotlib-multiple-scatter-subplots-with-shared-colour-bar
# referenced: https://matplotlib.org/stable/tutorials/introductory/animation_tutorial.html
# reference: https://pythonforundergradengineers.com/live-plotting-with-matplotlib.html


## Choose CSV file to read for plotting
df = pd.read_csv('data/07.12.2023/14.06.csv') # read csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder

interval = 200
frame_rate = len(df['Desired Position: x (m)'])-1


###########################################
# ~~ PLOT 1: Positions (actual/desired) ~~
fig, ax = plt.subplots()

# creates scatter plots 
des_rob_pos = ax.scatter(df['Desired Position: x (m)'], df['Desired Position: y (m)'])
act_rob_pos = ax.scatter(df['Actual Position: x (m)'],df['Actual Position: y (m)'])
#fish_pos = ax.scatter(df['Fish Position: x (m)'], df['Fish Position: y (m)'])

# set the legend for multiple plots
ax.legend(['Desired Position', 'Actual Position', "Fish Position"])


# reference: https://matplotlib.org/3.1.1/gallery/widgets/slider_demo.html
axtime = plt.axes([0.22, 0.13, 0.60, 0.03])
stime = Slider(axtime, 'Time', 0, 60, 0.5)


def animate(i):
    data_trail = 10 # set amount of data points behind current that remain showing
    # update data
    x1 = df['Desired Position: x (m)'][:i]
    y1 = df['Desired Position: y (m)'][:i]
    x2 = df['Actual Position: x (m)'][:i]
    y2 = df['Actual Position: y (m)'][:i]
    # x3 = df['Fish Position: x (m)'][:i]
    # y3 = df['Fish Position: y (m)'][:i]
    
    ax.scatter(x1, y1)
    ax.scatter(x2,y2)

    ax.clear()
    ax.set_ylim(0, 0.3)
    ax.set_xlim(0, 0.5)
    
    

    for i in range(0, abs(data_trail)):
        ax.scatter(x2[i-data_trail:], y2[i-data_trail:], color = '#506cb9', alpha = max(0, (i/data_trail)))
        ax.scatter(x1[i-data_trail:], y1[i-data_trail:], color = "#d8e0eb", alpha = max(0,(i/data_trail)))
        #ax.scatter(x3[i-data_trail:], y3[i-data_trail:], color = "#f4c792", alpha = max(0, (i/data_trail)))
    
    # set title of plot
    ax.set_title('Postions')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    return (des_rob_pos, act_rob_pos)#, fish_pos)

# creates animation 
ani = animation.FuncAnimation(fig = fig, func = animate, repeat=True, frames = frame_rate, interval = interval)

ax.clear()
plt.show()



 