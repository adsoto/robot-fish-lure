import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
# referenced: https://www.tutorialspoint.com/how-to-plot-csv-data-using-matplotlib-and-pandas-in-python on 6/12/23
#              https://www.statology.org/pandas-plot-multiple-series/ on 6/13/23
#              https://stackoverflow.com/questions/44970881/matplotlib-multiple-scatter-subplots-with-shared-colour-bar

## Choose CSV file to read for plotting
df = pd.read_csv('data/backup/07.26.2023/15.40.csv') # read csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder
# print(df['Desired Position: y (m)'])
# for col in df.columns:
#     print(col)

def to_list(string): #not a part of the Object class because it takes in a string
    list2 = list(string.split(","))
    return list2


'''Manipulate robot data'''
robot = [pos for pos in df['Robot']]  
robot = [x for x in robot if str(x) != 'nan']

robot_lists = robot
for i in range(len(robot)):
        list_version = to_list(robot[i])
        robot_lists[i]=list_version

robot_t = [None] * len(robot_lists)
robot_x = [None] * len(robot_lists)
robot_y = [None] * len(robot_lists)
robot_theta = [None] * len(robot_lists)
for i in range(len(robot_lists)):
      robot_t[i]=float(robot_lists[i][0])
      robot_x[i]=float(robot_lists[i][1])
      robot_y[i]=float(robot_lists[i][2])
      robot_theta[i]=float(robot_lists[i][3])

'''Manipulate fish data'''
fish = [pos for pos in df['Fish']]  
fish = [x for x in fish if str(x) != 'nan']

fish_lists = fish
for i in range(len(fish)):
        list_version = to_list(fish[i])
        fish_lists[i]=list_version

fish_t = [None] * len(fish_lists)
fish_x = [None] * len(fish_lists)
fish_y = [None] * len(fish_lists)
fish_theta = [None] * len(fish_lists)
for i in range(len(fish_lists)):
      fish_t[i]=float(fish_lists[i][0])
      fish_x[i]=float(fish_lists[i][1])
      fish_y[i]=float(fish_lists[i][2])
      fish_theta[i]=float(fish_lists[i][3])

'''Manipulate desired data'''
des = [pos for pos in df['Desired']]  
des = [x for x in des if str(x) != 'nan']

des_lists = des
for i in range(len(des)):
        list_version = to_list(des[i])
        des_lists[i]=list_version

des_t = [None] * len(des_lists)
des_x = [None] * len(des_lists)
des_y = [None] * len(des_lists)
des_theta = [None] * len(des_lists)
for i in range(len(des_lists)):
      des_t[i]=float(des_lists[i][0])
      des_x[i]=float(des_lists[i][1])
      des_y[i]=float(des_lists[i][2])
      des_theta[i]=float(des_lists[i][3])

'''Distance data'''
#to do 
distances = [pos for pos in df['Distances']]  
distances = [x for x in distances if str(x) != 'nan']


"PLOT DATA!"
# ~~ PLOT 1: Positions (actual/desired) ~~
fig, ax = plt.subplots()
line1 = ax.scatter(des_x, des_y)
line2 = ax.scatter(robot_x,robot_y)
line3 = ax.scatter(fish_x, fish_y)

# set the legend for multiple plots
ax.legend(['Desired Position', 'Actual Position', "Fish Position"])

# set title of plot
ax.set_title('Postions')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_ylim(-0.1, 0.65)
ax.set_xlim(0, 0.65)
#ax.set_aspect(aspect=1)



## ~~ PLOT 2: X and Y (actual/desired) Positions ~~
fig1, (axs1, axs2) = plt.subplots(1, 2)
fig1.set_size_inches(10,4)
fig1.tight_layout


# make scatter subplot 1
line1 = axs1.scatter(des_t, des_x)
line2 = axs1.scatter(robot_t, robot_x)
line3 = axs1.scatter(fish_t, fish_x)

# make scatter subplot 2
line1 = axs2.scatter(des_t, des_y)
line2 = axs2.scatter(robot_t, robot_y)
line3 = axs2.scatter(fish_t, fish_y)
axs2.set_ylim(0,0.5)

# set title of subplot 1
axs1.set_title('X vs Time')
axs1.set_xlabel('Time (s)')
axs1.set_ylabel('X (m)')

# set title of subplot 2
axs2.set_title('Y vs Time')
axs2.set_xlabel('Time (s)')
axs2.set_ylabel('Y (m)')
axs2.legend(['Desired Position', 'Actual Position', 'Fish Position'])



## ~~ PLOT 3: Theta and Velocity ~~
fig3, axs5 = plt.subplots()
line1 = axs5.scatter(des_t, des_theta)
line2 = axs5.scatter(robot_t, robot_theta)

# set the legend for multiple plots
axs5.legend(['Desired Theta', 'Actual Theta'])

# set title of plot
axs5.set_title('Theta')
axs5.set_xlabel('time (s)')
axs5.set_ylabel('theta (rad)')
#axs5.set_ylim(0, 0.6)
#axs5.set_xlim(0, 0.6)

fig4, axs6 = plt.subplots()
line1 = axs6.scatter(fish_t, distances)
axs6.legend(['Distance between robot and fish (m)'])
axs6.set_title("Distance between Robot and Closest Fish")
axs6.set_xlabel('time (s)')
axs6.set_ylabel('distance (m)')



v = np.linalg.norm(np.diff(np.array([robot_x, robot_y])), axis=0)/np.diff(robot_t) #filter velocity data. overplot desired vs. actual. change to central velocity calculations
fig2,  axs4 = plt.subplots()
#fig2.set_size_inches(12,4)
line2 = axs4.plot(robot_t[1:], v)

axs4.set_title('Velocity vs Time')
axs4.set_xlabel('Time (s)')
axs4.set_ylabel('Velocity (m/s)')
axs4.set_ylim(0,0.3)


plt.show()
    
