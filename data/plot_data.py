# opens and replots csv data

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

# referenced: https://www.tutorialspoint.com/how-to-plot-csv-data-using-matplotlib-and-pandas-in-python on 6/12/23
#              https://www.statology.org/pandas-plot-multiple-series/ on 6/13/23
#              https://stackoverflow.com/questions/44970881/matplotlib-multiple-scatter-subplots-with-shared-colour-bar

df = pd.read_csv('data/06.14.2023/13.23.csv') # read csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder
print(df['Desired Position: y (m)'])
for col in df.columns:
    print(col)


# Plot 1
fig1, ax = plt.subplots()
line1 = ax.scatter(df['Desired Position: x (m)'], df['Desired Position: y (m)'])
line2 = ax.scatter(df['Actual Position: x (m)'],df['Actual Position: y (m)'])

# set the legend for multiple plots
ax.legend(['Desired Position', 'Actual Position'])

# set title of plot
ax.set_title('Postions')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_ylim(0, 0.5)
ax.set_xlim(0, 0.5)
#ax.set_aspect(aspect=1)

# Plot 2
fig2, ax = plt.subplots()
line1 = ax.scatter(df['Theta vs. Time: time(s)'], df['Theta vs. Time: theta'])
#line2 = ax.plot(df['Actual Position: x (m)'],df['Actual Position: y (m)'])

# set the legend for multiple plots
#ax.legend(['Desired Position', 'Actual Position'])

# set title of plot
ax.set_title('Theta vs Time')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Theta')


# Plot 3
fig3, ax = plt.subplots()
line1 = ax.scatter(df['Robot Velocity: time (s)'], df['Robot Velocity: velocity (m/s)'])
#line2 = ax.plot(df['Actual Position: x (m)'],df['Actual Position: y (m)'])

# set the legend for multiple plots
#ax.legend(['Desired Position', 'Actual Position'])

# set title of plot
ax.set_title('Velocity vs Time')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Velocity (m/s)')


fig4, ax = plt.subplots()
line1 = ax.scatter(df['Theta vs. Time: time(s)'], df['Desired Position: x (m)'])
line2 = ax.scatter(df['Theta vs. Time: time(s)'], df['Actual Position: x (m)'])

# set the legend for multiple plots
#ax.legend(['Desired Position', 'Actual Position'])

# set title of plot
ax.set_title('X vs Time')
ax.set_xlabel('Time (s)')
ax.set_ylabel('X (m)')

fig5, ax = plt.subplots()
line1 = ax.scatter(df['Theta vs. Time: time(s)'], df['Desired Position: y (m)'])
line2 = ax.scatter(df['Theta vs. Time: time(s)'], df['Actual Position: y (m)'])

# set the legend for multiple plots
#ax.legend(['Desired Position', 'Actual Position'])

# set title of plot
ax.set_title('Y vs Time')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Y (m)')


## tried using pandas dataframe to plot. could not figure out overlay with pandas
#df.plot(x='Desired Position_x (m)', y = 'Desired Position_y (m)')
#df.plot(x='Actual Position_x (m)', y = 'Actual Position_y (m)')

plt.show()