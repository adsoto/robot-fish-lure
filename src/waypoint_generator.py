# creates functions that will take user input and run straight or turn 
import numpy as np

start_pos = np.array([0,0])
start_time = 0
dt = 0.05

def straight_wypt(dist, vel, theta_dir, start_pos, start_time): # theta_dir is the direction that you want the line to be in 
    """generates a single trajectory waypoint for the robot to move the desired distance at the desired speed """
    new_x = round(start_pos[0]+dist*np.cos(theta_dir), 4)
    new_y = round(start_pos[1]+dist*np.sin(theta_dir),4)
    new_time = start_time+dist/vel
    new_theta = round(theta_dir, 4) # idk if des_theta in the trajectory actually does anything
    new_wypt = np.array([new_time, new_x, new_y, new_theta])
    
    start_pos = [new_x, new_y]
    start_time = new_time
    # returns a waypoint and the start_pos and start_time required as input for a following waypoint
    return np.array(new_wypt), start_pos, start_time

### straight waypoints
wp1, start_pos, start_time = straight_wypt(1, 0.2, 0, start_pos, start_time)
print(wp1)
wp2 = straight_wypt(1, 0.2, 0, start_pos, start_time)[0]
print(wp2)

# def turn(radians, angular_vel, currrent_theta, start_pos, start_time):
#     """turns the robot by _ radians at __ angular_velocity"""

#     new_theta = current_theta
#     new_wypt = np.array()

"""
wypt1 = straight(1, 1, np.pi/2, start_pos, start_time)
print(wypt1)

def gen_wypts(wypt):
"""





