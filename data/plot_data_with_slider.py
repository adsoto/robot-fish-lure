import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button

# reference: https://www.geeksforgeeks.org/matplotlib-slider-widget/#
# reference for finding closest value from df: https://www.statology.org/pandas-find-closest-value/
data_trail = 10
frame_rate = 50
interval = 50

# Create subplot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom = 0.35)
ax.set_ylim(0, 0.3)
ax.set_xlim(0, 0.5)

## Choose CSV file to read for plotting
df = pd.read_csv('data/07.12.2023/14.06.csv') # read csv file from data folder. Ex: 'data/06.13.2023/13.17.csv' reads the 13.17.csv file from the 06.13.2023 subfolder inside data folder
x0 = df['Desired Position: x (m)'][0]
y0 = df['Desired Position: y (m)'][0]
max_time = max(df['Desired X-Pos vs. Time: time(s)'])
min_time = min(df['Desired X-Pos vs. Time: time(s)'])

x_despos = df['Desired Position: x (m)']
y_despos = df['Desired Position: y (m)']
x_actpos = df['Actual Position: x (m)']
y_actpos = df['Actual Position: y (m)']



# Create scatter plot
#des_rob_pos = plt.scatter(x_despos, y_despos)
des_rob_pos = plt.scatter(x0, y0, color = "purple")

# Create slider bar
ax_tslider = plt.axes([0.22, 0.13, 0.60, 0.03])
time_slider = Slider(ax_tslider, 'Time', min_time, max_time, min_time)

# Function that is called when slider value changes
def update_slider(val):
    ax.clear()
    ax.set_ylim(0, 0.3)
    ax.set_xlim(0, 0.5)
    tslider = time_slider.val
    # finds the df row with a time (in column 'Desired X-Pos vs. Time: time(s)') that most closely matches the slider time value 
    closest_df_row_from_time = df.iloc[(df['Desired X-Pos vs. Time: time(s)']-tslider).abs().argsort()[:data_trail]]
    #print(closest_df_row_from_time)
    # pulls out the int value time from the df row
    closest_time = closest_df_row_from_time['Desired X-Pos vs. Time: time(s)'].tolist()[0]
    
    # gets the row index of the time on the slider
    t_idx_despos = df.loc[df['Desired X-Pos vs. Time: time(s)'] == closest_time].index[0]
    #
    for i in range(0, abs(data_trail)):
        ax.scatter(x_despos[t_idx_despos - data_trail + i], y_despos[t_idx_despos - data_trail + i], color = "#d8e0e3", alpha = max(0, (i/data_trail)) )
        ax.scatter(x_actpos[t_idx_despos - data_trail + i], y_actpos[t_idx_despos - data_trail + i], color = '#506cb9', alpha = max(0, (i/data_trail))) 

    #ax.scatter(x_despos[t_idx_despos], y_despos[t_idx_despos])
    

# Call update function when slider is changed
time_slider.on_changed(update_slider)

# Create reset button
ax_reset = plt.axes([0.5, 0.025, 0.1, 0.04])
reset_button = Button(ax_reset, 'Reset', color = 'steelblue', hovercolor = 'lightsteelblue')

# Function that resets slider to initial values when reset button is clicked
def reset_slider(event):
    time_slider.reset()
    ax.clear()
    ax.set_ylim(0, 0.3)
    ax.set_xlim(0, 0.5)
    
# Call reset_slider func
reset_button.on_clicked(reset_slider)

# Create a play button for animation
# ax_play = plt.axes([0.35, 0.025, 0.1, 0.04])
# play_button = Button(ax_play, 'Play', color = 'lightblue', hovercolor = 'skyblue')

# def animate_data(i):
#     # update data
#     x1 = df['Desired Position: x (m)'][:i]
#     y1 = df['Desired Position: y (m)'][:i]
#     x2 = df['Actual Position: x (m)'][:i]
#     y2 = df['Actual Position: y (m)'][:i]
#     # x3 = df['Fish Position: x (m)'][:i]
#     # y3 = df['Fish Position: y (m)'][:i]

#     ax.clear()
#     ax.scatter(x1, y1)
#     ax.scatter(x2,y2)

#     for i in range(0, abs(data_trail)):
#         ax.scatter(x2[i-data_trail:], y2[i-data_trail:], color = '#506cb9', alpha = max(0, (i/data_trail)))
#         ax.scatter(x1[i-data_trail:], y1[i-data_trail:], color = "#d8e0eb", alpha = max(0,(i/data_trail)))
#         #ax.scatter(x3[i-data_trail:], y3[i-data_trail:], color = "#f4c792", alpha = max(0, (i/data_trail)))
#     ax.set_ylim(0, 0.3)
#     ax.set_xlim(0, 0.5)
#     # set title of plot
#     ax.set_title('Postions')
#     ax.set_xlabel('X (m)')
#     ax.set_ylabel('Y (m)')
    

# def play_animation(event):
#     anim = animation.FuncAnimation(fig = fig, func = animate_data, repeat=False, frames = frame_rate, interval = interval)
#     plt.show()

# play_button.on_clicked(play_animation)

# Function that plays animation when play button is clicked
#def play_animation(event):



# Show graph
ax.clear()
plt.show()
