
import numpy as np
from positions_in_tank import *
from make_traj_pts import straight_traj, rot_traj
import time

def get_traj(X_r, X_f, current_traj):
    """gets the next trajectory of the lure based on the current position of the lure, the fish and the current trajectory"""
    # robot state: [time, x, y, theta]
    curr_time = X_r[0]
    rob_pos = [X_r[1], X_r[2]]
    fish_pos = [X_f[1], X_f[2]]
    radius_about_pt = 0.05 # 5 cm
    fish_alert_radius = 0.08 # 8 cm
    theta = 0; # desired theta currently defaulting to 0
    # start_time initialized in c.run = gloabl computer time = wonky number
    # current_time initialized in c.run = corrected robot start time
    current_time = 0 # placeholder until it is called in c.run

    # lure not done with current trajectory
    if curr_time < current_traj[-1][0]:
        return current_traj
    
    # lure at point A and done with the current trajectory --> needs new traj
    elif np.linalg.norm(rob_pos - A) <= radius_about_pt:
        # if fish close
        if np.linalg.norm(fish_pos - rob_pos) <= fish_alert_radius:
            # !! need to update this to give trajectory instead of just a single destination traj point
            # A->C
            dist = np.linalg.norm(rob_pos-C)
            new_traj =  straight_traj(dist, 0.08, current_time, rob_pos, 0)  # dart diag. across tank
            return new_traj
        else: # fish not close
            #A->B
            dist = np.linalg.norm(rob_pos-B)
            new_traj =  straight_traj(dist, 0.05, current_time, rob_pos, 0)
            return new_traj
        
    # same code format for checking robot at pts B, C, D
    # if at pos B
    elif np.linalg.norm(rob_pos - B) <= radius_about_pt:
        # if fish close
        if np.linalg.norm(fish_pos - rob_pos) <= fish_alert_radius:
            # !! need to update this to give trajectory instead of just a single destination traj point
            # B->D
            dist = np.linalg.norm(rob_pos-D)
            new_traj =  straight_traj(dist, 0.05, current_time, rob_pos, 0) # dart diag. across tank
            return new_traj
        else: # fish not close
            #B->C
            dist = np.linalg.norm(rob_pos-C)
            new_traj =  straight_traj(dist, 0.05, current_time, rob_pos, 0)
            return new_traj
    
    # if at pos C   
    elif np.linalg.norm(rob_pos - C) <= radius_about_pt:
        # if fish close
        if np.linalg.norm(fish_pos - rob_pos) <= fish_alert_radius:
            # !! need to update this to give trajectory instead of just a single destination traj point
            # C->A
            dist = np.linalg.norm(rob_pos-A)
            new_traj =  straight_traj(dist, 0.05, current_time, rob_pos, 0) # dart diag. across tank
            return new_traj
        else: # fish not close
            #C->D
            dist = np.linalg.nomr(rob_pos-D)
            new_traj =  straight_traj(dist, 0.05, current_time, rob_pos, 0)
            return new_traj

    # if at pos D    
    elif np.linalg.norm(rob_pos - D) <= radius_about_pt:
        # if fish close
        if np.linalg.norm(fish_pos - rob_pos) <= fish_alert_radius:
            # !! need to update this to give trajectory instead of just a single destination traj point
            # D->B
            dist = np.linalg.norm(rob_pos-B)
            new_traj =  straight_traj(dist, 0.05, current_time, rob_pos, 0) # dart diag. across tank
            return new_traj
        else: # fish not close
            #D->A
            dist = np.linalg.norm(rob_pos-A)
            new_traj =  straight_traj(dist, 0.05, current_time, rob_pos, 0)
            return new_traj

