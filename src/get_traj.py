

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
  
   # conditional that checks if there are fish in tank/frame. If not, then always set robot as being too far from a fish. this disables any conditional where a fish state is checked
   if X_f == None:
       #print("there is no fish")
       robot2fish = fish_alert_radius + 1
   else: # fish is present and X_f state can be found
       #print("there is a fish")
       robot2fish = X_r.distance_to(X_f)
       print("robot2fish:", robot2fish)




   rob_x = X_r.x
   rob_y = X_r.y


   A_x = A[0]
   A_y = A[1]
   Axdist = (A_x - rob_x)
   Aydist = (A_y-rob_y)
   A_rob_dist = np.sqrt(np.square(Axdist) + np.square(Aydist))


   B_x = B[0]
   B_y = B[1]
   Bxdist = (B_x - rob_x)
   Bydist = (B_y-rob_y)
   B_rob_dist = np.sqrt(np.square(Bxdist) + np.square(Bydist))


   C_x = C[0]
   C_y = C[1]
   Cxdist = (C_x - rob_x)
   Cydist = (C_y-rob_y)
   C_rob_dist = np.sqrt(np.square(Cxdist) + np.square(Cydist))


   D_x = D[0]
   D_y = D[1]
   Dxdist = (D_x - rob_x)
   Dydist = (D_y-rob_y)
   D_rob_dist = np.sqrt(np.square(Dxdist) + np.square(Dydist))


   # lure not done with current trajectory
   if curr_time < current_traj[-1][0]:
       print("continue on current traj")
       return current_traj
   # lure done w current trajectory:
   # lure at point A and done with the current trajectory --> needs new traj
   if A_rob_dist <= radius_about_pt:
       print('in A')
       # if fish close
       if robot2fish <= fish_alert_radius:
           print('evading from A')
           # # A->C
           dist = C_rob_dist
           new_traj = straight_traj(dist, 0.08, curr_time, rob_pos, 0) # dart diag. across tank
           return new_traj
       else: # fish not close. contine wander mode
           #A->B
           print('continuing A to B')
           dist = B_rob_dist
           new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0)
           return new_traj
       # same code format for checking robot at pts B, C, D
       # # if at pos B
   elif B_rob_dist <= radius_about_pt:
       # if fish close
       if robot2fish <= fish_alert_radius:
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
       # D->B
           dist = B_rob_dist
           new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0) # dart diag. across tank
           return new_traj
   else: # fish not close
       #D->A
       dist = A_rob_dist
       new_traj = straight_traj(dist, 0.05, curr_time, rob_pos, 0)
       return new_traj















