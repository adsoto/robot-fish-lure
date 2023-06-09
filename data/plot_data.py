# opens and replots csv data

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

# referenced: https://www.tutorialspoint.com/how-to-plot-csv-data-using-matplotlib-and-pandas-in-python on 6/12/23
#              https://www.statology.org/pandas-plot-multiple-series/ on 6/13/23
#              https://stackoverflow.com/questions/44970881/matplotlib-multiple-scatter-subplots-with-shared-colour-bar

## Choose CSV file to read for plotting
df = pd.read_csv('data/06.16.2023/10.14.csv') # read csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder
# print(df['Desired Position: y (m)'])
# for col in df.columns:
#     print(col)

# ~~ PLOT 1: Positions (actual/desired) ~~
fig, ax = plt.subplots()
line1 = ax.scatter(df['Desired Position: x (m)'], df['Desired Position: y (m)'], s=5)
line2 = ax.scatter(df['Actual Position: x (m)'],df['Actual Position: y (m)'], s=5)

# set the legend for multiple plots
ax.legend(['Desired Position', 'Actual Position'])

# set title of plot
ax.set_title('Postions')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_ylim(0, 0.5)
ax.set_xlim(0, 0.5)
#ax.set_aspect(aspect=1)

## ~~ PLOT 2: X and Y (actual/desired) Positions ~~
fig1, (axs1, axs2) = plt.subplots(1, 2)
fig1.set_size_inches(10,4)
fig1.tight_layout

# make scatter subplot 1
line1 = axs1.scatter(df['Desired X-Pos vs. Time: time(s)'], df['Desired Position: x (m)'], s=5)
line2 = axs1.scatter(df['Actual X-Pos vs. Time: time(s)'], df['Actual Position: x (m)'], s=5)

# make scatter subplot 2
line1 = axs2.scatter(df['Desired X-Pos vs. Time: time(s)'], df['Desired Position: y (m)'], s=5)
line2 = axs2.scatter(df['Actual X-Pos vs. Time: time(s)'], df['Actual Position: y (m)'], s=5)
axs2.set_ylim(0,0.5)

# set title of subplot 1
axs1.set_title('X vs Time')
axs1.set_xlabel('Time (s)')
axs1.set_ylabel('X (m)')

# set title of subplot 2
axs2.set_title('Y vs Time')
axs2.set_xlabel('Time (s)')
axs2.set_ylabel('Y (m)')
axs2.legend(['Desired Position', 'Actual Position'])

## ~~ PLOT 3: Theta and Velocity ~~
fig2, (axs3, axs4) = plt.subplots(1, 2)
fig2.set_size_inches(12,4)
line1 = axs3.scatter(df['Theta vs. Time: time(s)'], df['Theta vs. Time: theta (rads)'], s=5)
line2 = axs4.scatter(df['Robot Velocity: time (s)'], df['Robot Velocity: velocity (m/s)'], s=5)

# set title of subplot 1
axs3.set_title('Theta vs Time')
axs3.set_xlabel('Time (s)')
axs3.set_ylabel('Theta')

# set title of subplot 2
axs4.set_title('Velocity vs Time')
axs4.set_xlabel('Time (s)')
axs4.set_ylabel('Velocity (m/s)')
axs4.set_ylim(0,0.3)

plt.show()