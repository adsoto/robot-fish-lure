
import numpy as np
from positions_in_tank import *


def get_traj(Xr, Xf, current_traj):
    """gets the next trajectory of the lure based on the current position of the lure, the fish and the current trajectory"""
    # robot state: [time, x, y, theta]
    curr_time = Xr[0]
    rob_pos = [Xr[1], Xr[2]]
    fish_pos = [Xf[1], Xf[2]]
    radius_about_pt = 0.05 # 5 cm
    fish_alert_radius = 0.08 # 8 cm
    time_to_pt = 2 # time to add for new trajectory
    theta = 0; # desired theta currently defaulting to 0

    # lure not done with current trajectory
    if curr_time < current_traj[-1][0]:
        return current_traj
    
    # lure at point A and done with the current trajectory --> needs new traj
    elif np.linalg.norm(rob_pos - A) <= radius_about_pt:
        # if fish close
        if np.linalg.norm(fish_pos - rob_pos) <= fish_alert_radius:
            # !! need to update this to give trajectory instead of just a single destination traj point
            # A->C
            new_traj = np.append((curr_time + time_to_pt), C, theta) # dart diag. across tank
            return new_traj
        else: # fish not close
            #A->B
            new_traj = np.append((curr_time + time_to_pt), B, theta)
            return new_traj
        
    # same code format for checking robot at pts B, C, D
    # if at pos B
    elif np.linalg.norm(rob_pos - B) <= radius_about_pt:
        # if fish close
        if np.linalg.norm(fish_pos - rob_pos) <= fish_alert_radius:
            # !! need to update this to give trajectory instead of just a single destination traj point
            # B->D
            new_traj = np.append((curr_time + time_to_pt), D, theta) # dart diag. across tank
            return new_traj
        else: # fish not close
            #B->C
            new_traj = np.append((curr_time + time_to_pt), C, theta)
            return new_traj
    
    # if at pos C   
    elif np.linalg.norm(rob_pos - C) <= radius_about_pt:
        # if fish close
        if np.linalg.norm(fish_pos - rob_pos) <= fish_alert_radius:
            # !! need to update this to give trajectory instead of just a single destination traj point
            # C->A
            new_traj = np.append((curr_time + time_to_pt), A, theta) # dart diag. across tank
            return new_traj
        else: # fish not close
            #C->D
            new_traj = np.append((curr_time + time_to_pt), D, theta)
            return new_traj

    # if at pos D    
    elif np.linalg.norm(rob_pos - D) <= radius_about_pt:
        # if fish close
        if np.linalg.norm(fish_pos - rob_pos) <= fish_alert_radius:
            # !! need to update this to give trajectory instead of just a single destination traj point
            # D->B
            new_traj = np.append((curr_time + time_to_pt), B, theta) # dart diag. across tank
            return new_traj
        else: # fish not close
            #D->A
            new_traj = np.append((curr_time + time_to_pt), A, theta)
            return new_traj

