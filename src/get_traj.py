

# new get_traj function for refactored code
# last edited: 7/5/23 3:06pm
# holly hachen@hmc.edu
import numpy as np
from positions_in_tank import *
from make_traj_pts import straight_traj, rot_traj
import time


def get_traj_function(X_r, X_f, current_traj):
    """gets the next trajectory of the lure based on the current position of the lure, the fish and the current trajectory"""
    # robot state: [time, x, y, theta]
    curr_time = X_r.t
    rob_pos = [X_r.x, X_r.y]
    if X_f:
        fish_pos = [X_f.x, X_f.y]
    radius_about_pt = 0.05 # 5 cm
    fish_alert_radius = 0.08 # 8 cm
    theta = 0; # desired theta currently defaulting to 0
    # start_time initialized in c.run = gloabl computer time = wonky number
    # current_time initialized in c.run = corrected robot start time
    #current_time = 0 # placeholder until it is called in c.run

    robot2fish = X_r.distance_to(X_f)

    rob_x = X_r.x
    rob_y = X_r.y

    A_x = A[0]
    A_y = A[1]
    Axdist = np.square(A_x - rob_x)
    Aydist = np.square(A_y-rob_y)
    A_rob_dist = np.sqrt(Axdist+Aydist)

    B_x = B[0]
    B_y = B[1]
    Bxdist = np.square(B_x - rob_x)
    Bydist = np.square(B_y-rob_y)
    B_rob_dist = np.sqrt(Bxdist+Bydist)

    C_x = C[0]
    C_y = C[1]
    Cxdist = np.square(C_x - rob_x)
    Cydist = np.square(C_y-rob_y)
    C_rob_dist = np.sqrt(Cxdist+Cydist)

    D_x = D[0]
    D_y = D[1]
    Dxdist = np.square(D_x - rob_x)
    Dydist = np.square(D_y-rob_y)
    D_rob_dist = np.sqrt(Dxdist+Dydist)

    # lure not done with current trajectory
    if curr_time < current_traj[(len(current_traj)-1)][0]:
        return current_traj
    # lure at point A and done with the current trajectory --> needs new traj
    elif A_rob_dist <= radius_about_pt:
        # if fish close
        if robot2fish <= fish_alert_radius:
            # !! need to update this to give trajectory instead of just a single destination traj point
            # # A->C
            dist = C_rob_dist
            new_traj = straight_traj(dist, 0.08, curr_time, rob_pos, 0) # dart diag. across tank
            return new_traj
        else: # fish not close
            #A->B
            dist = B_rob_dist
            new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0)
            return new_traj
        # same code format for checking robot at pts B, C, D
        # # if at pos B
    elif B_rob_dist <= radius_about_pt:
        # if fish close
        if robot2fish <= fish_alert_radius:
        # !! need to update this to give trajectory instead of just a single destination traj point
        # B->D
            dist = D_rob_dist
            new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0) # dart diag. across tank
            return new_traj
        else: # fish not close
            #B->C
            dist = C_rob_dist
            new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0)
            return new_traj
            # if at pos C
    elif C_rob_dist <= radius_about_pt:
        # if fish close
        if robot2fish <= fish_alert_radius:
        # !! need to update this to give trajectory instead of just a single destination traj point
        # C->A
            dist = A_rob_dist
            new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0) # dart diag. across tank
            return new_traj
        else: # fish not close
            #C->D
            dist = D_rob_dist
            new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0)
            return new_traj
        # if at pos D
    elif D_rob_dist <= radius_about_pt:
        # if fish close
        if robot2fish <= fish_alert_radius:
        # !! need to update this to give trajectory instead of just a single destination traj point
        # D->B
            dist = B_rob_dist
            new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0) # dart diag. across tank
            return new_traj
    else: # fish not close
        #D->A
        dist = A_rob_dist
        new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0)
        return new_traj





