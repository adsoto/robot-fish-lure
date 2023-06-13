# opens and replots csv data

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

# referenced: https://www.tutorialspoint.com/how-to-plot-csv-data-using-matplotlib-and-pandas-in-python on 6/12/23
#              https://www.statology.org/pandas-plot-multiple-series/ on 6/13/23

df = pd.read_csv('data/06.13.2023/14.44.csv') # read csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder
print(df)

# Plot 1
fig1, ax = plt.subplots()
line1 = ax.plot(df['Desired Position: x (m)'], df['Desired Position: y (m)'])
line2 = ax.plot(df['Actual Position: x (m)'],df['Actual Position: y (m)'])

# set the legend for multiple plots
ax.legend(['Desired Position', 'Actual Position'])

# set title of plot
ax.set_title('Postions')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')

# Plot 2
fig2, ax = plt.subplots()
line1 = ax.plot(df['Theta vs. Time: time(s)'], df['Theta vs. Time: theta'])
#line2 = ax.plot(df['Actual Position: x (m)'],df['Actual Position: y (m)'])

# set the legend for multiple plots
#ax.legend(['Desired Position', 'Actual Position'])

# set title of plot
ax.set_title('Theta vs Time')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Theta')



## tried using pandas dataframe to plot. could not figure out overlay with pandas
#df.plot(x='Desired Position_x (m)', y = 'Desired Position_y (m)')
#df.plot(x='Actual Position_x (m)', y = 'Actual Position_y (m)')

plt.show()