



# new get_traj function for refactored code. calculates theta_des and dist based on most recent waypoint and next waypoint
# last edited: 7/12/23 12pm
# contact: alisha - achulani@hmc.edu and holly - hachen@hmc.edu
import numpy as np
from positions_in_tank import *
from make_traj_pts import straight_traj, rot_traj
import time


v_rect = 0.05
v_diagonal = 0.08




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
  A_rob_dist = np.sqrt(np.square(A_x - rob_x) + np.square(A_y-rob_y))


  B_x = B[0]
  B_y = B[1]
  B_rob_dist = np.sqrt(np.square(B_x - rob_x) + np.square(B_y - rob_y))


  C_x = C[0]
  C_y = C[1]
  C_rob_dist = np.sqrt(np.square(C_x - rob_x) + np.square(C_y - rob_y))


  D_x = D[0]
  D_y = D[1]
  D_rob_dist = np.sqrt(np.square(D_x - rob_x) + np.square(D_y - rob_y))


  A_B_dist = np.sqrt(np.square(B_y - A_y) + np.square(B_x - A_x))
  A_C_dist = np.sqrt(np.square(C_y - A_y) + np.square(C_x - A_x))


  B_C_dist = np.sqrt(np.square(C_y - B_y) + np.square(C_x - B_x))
  B_D_dist = np.sqrt(np.square(B_y - D_y) + np.square(B_x - D_x))


  C_D_dist = np.sqrt(np.square(C_y - D_y) + np.square(C_x - D_x))
  A_D_dist = np.sqrt(np.square(D_y - A_y) + np.square(D_x - A_x))


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
          dist =  A_C_dist#C_rob_dist
          theta = np.arctan2((C_y - A_y), (C_x - A_x))
          new_traj = straight_traj(dist, v_diagonal, curr_time, A, theta) # dart diag. across tank
          return new_traj
      else: # fish not close. contine wander mode
          #A->B
          print('continuing A to B')
          dist = A_B_dist
          theta = np.arctan2((B_y - A_y), (B_x - A_x))
          new_traj = straight_traj(dist, v_rect, curr_time, A, theta)
          return new_traj
      # same code format for checking robot at pts B, C, D
      # # if at pos B
  elif B_rob_dist <= radius_about_pt:
      print("within B")
      # if fish close
      if robot2fish <= fish_alert_radius:
          print("fish in B - evade to D")
      # B->D
          dist = B_D_dist
          theta = np.arctan2((D_y - B_y), (B_x - B_x))
          new_traj = straight_traj(dist, v_diagonal, curr_time, B, theta) # dart diag. across tank
          return new_traj
      else: # fish not close
          #B->C
          print("no fish in B - continue to C")
          dist = B_C_dist
          theta = np.arctan2((C_y - B_y), (C_x - B_x))
          new_traj = straight_traj(dist, v_rect, curr_time, B, theta)
          return new_traj
          # if at pos C
  elif C_rob_dist <= radius_about_pt:
      # if fish close
      if robot2fish <= fish_alert_radius:
      # C->A
          dist = A_C_dist
          theta = np.arctan2((A_y - C_y), (A_x - C_x))
          new_traj = straight_traj(dist, v_diagonal, curr_time, C, theta) # dart diag. across tank
          return new_traj
      else: # fish not close
          #C->D
          dist = C_D_dist
          theta = np.arctan2((D_y - C_y), (D_x - C_x))
          new_traj = straight_traj(dist, v_rect, curr_time, C, -theta)
          return new_traj
      # if at pos D
  elif D_rob_dist <= radius_about_pt:
      # if fish close
      if robot2fish <= fish_alert_radius:
      # D->B
          dist = B_D_dist
          theta = np.arctan2((B_y - D_y), (B_x - D_x))
          new_traj = straight_traj(dist, v_diagonal, curr_time, D, theta) # dart diag. across tank
          return new_traj
      else: # fish not close
          print("continuing from D to A")
          #D->A
          dist = A_D_dist
          theta = np.arctan2((A_y - D_y), (A_x - D_x))
          new_traj = straight_traj(dist, v_rect, curr_time, D, theta)
          return new_traj