import numpy as np
import serial
import time
from point_tracker import track_point
from paths import *
import data_handler as dh
import matplotlib.pyplot as plt
import video_processor as vp
import orange as orange
import centroidTracker 
import object_state
import get_traj
import make_traj_pts
from positions_in_tank import *


class Controller():
   """Top-level class to run the robotic fish"""

   def __init__(self, plot_data=True, save_data=True, camera_port=0, camera_bounds = np.array([[420, 365], [1340, 905]]),
                save_video=True, transmit_port='/dev/tty.usbmodem1402'):
       print("initializing controller")
       self._ser = serial.Serial(transmit_port, baudrate=115200)
       self._data_handler = dh.DataHandler(plot_data, save_data)
       self._video = orange.VideoProcessor(camera_port, camera_bounds, save_video)
       self._centroidTracker = centroidTracker.centroidTracker(camera_port, camera_bounds, save_video)
       self._robot_arr = []
       self._time_arr = []
       self._theta_arr = []
       self._fish_arr = []


   def send_commands(self, vR, vL):
       """Sends commands to the transmit board over the serial port"""
       print("vL = " + str(vL) + ", vR = " + str(vR))
       dict = {'vL': vL, 'vR' : vR}
       packet = str(dict) + "\r"
       self._ser.write(packet.encode())

   def find_target(self, traj, t):
       """Finds the next target in the path for the bot to track"""
       dt = 1.5 #is this still what we want? 
       X_r = self._video.get_robot_state(t) #in orange, do we even need this in here though?
       final_pos = [traj[len(traj)-1][1], traj[len(traj)-1][2]]
       ttrack = t+dt
       for i in range(1, len(traj)):
           #print('entered0')
           print("ttrack:",ttrack)
           if traj[i-1][0] < ttrack < traj[i][0]:
               print("entered1")
               t1 = traj[i-1][0]
               t2 = traj[i][0]
               percentTime = (ttrack-t1)/(t2-t1)
               pos1 = [traj[i-1][1], traj[i-1][2]]
               pos2 = [traj[i][1], traj[i][2]]
               distancevector = np.subtract(pos2, pos1) 
               target = pos1 + percentTime*distancevector
               print("target:" , target)
               X_des = object_state.Object(t, target[0], target[1], 0)
               return X_des
           elif ttrack > traj[len(traj)-1][0]:
               print('entered2')
               target = [traj[len(traj)-1][1], traj[len(traj)-1][2]]
               print("target:" , target)
               X_des = object_state.Object(t, target[0], target[1], 0)
               return X_des
            # else case for if robot trajectory time is greater than ttrack 

    
   def run(self): #will we need to pass anything else into run? 
       #initialize clock
       start_time = time.time()
       current_time = time.time() - start_time
       max_time = 10 #change this as needed


       X_r = self._video.get_robot_state(current_time)
       #curr_time = X_r.t
       rob_pos = [X_r.x, X_r.y]
       rob_x = X_r.x
       rob_y = X_r.y
       B_x = B[0]
       B_y = B[1]
       Bxdist = np.square(B_x - rob_x)
       Bydist = np.square(B_y-rob_y)
       B_rob_dist = np.sqrt(Bxdist+Bydist)
       dist = B_rob_dist
       print("dist:", dist)
       print("rob_pos:", rob_x, rob_y)
       print("current time:", current_time)
       traj_t = make_traj_pts.straight_traj(dist, 0.05, current_time, rob_pos, 0)
       
       
       while current_time < max_time:
          current_time = time.time() - start_time
          print("current time: ", current_time)
          X_r = self._video.get_robot_state(current_time) #in orange 

          print("robot state", X_r)
          X_f = self._centroidTracker.get_closest_fish_state(current_time) #closest fish
          print("fish state" , X_f)

          #how to initialize an initial trajectory? 
          traj_t = get_traj.get_traj_function(X_r, X_f, traj_t) #how to set this up to keep feeding previous trajs?
          #put fish conditionals in get traj (is Xf null...)

          print("traj: ", traj_t)
          
          X_des = self.find_target(traj_t, current_time) #update find_target as well for these inputs
          print("X_des", X_des)
          
          [vRight, vLeft] = track_point(X_des, X_r) #update track_point function for these inputs
          
          self.send_commands(vRight, vLeft)


          if self._video._go:
               #self._time_arr.append(current_time)
               #self._robot_arr.append(X_r)
               #self._theta_arr.append(theta)
               #self._fish_arr.append(X_f)
               self.send_commands(vRight, vLeft) # go as usual
          else:
               start_time = time.time() # reset start time
          self._video.display(X_des)


   def end(self):
       pass
   
   
   #should be saving on a regular interval instead of after the fact
   #after the fact is ok for now

if __name__ == '__main__':
    #LAIR: [ 687  396][1483  801]
    #keck: [570,  311], [1442, 802]
    # keck camera 2: [[ 699    9], [1204  892]]
    camera_bounds = np.array([[590, 331], [1430, 801]]) # find these with calibrate_setup.py
    # find these with calibrate_setup.py
    port_t = '/dev/tty.usbmodem1302'                # find this with ls /dev/tty.usb*   Change this port as needed
    port_c = 0                                      # either 0 or 1
    c = Controller(camera_bounds = camera_bounds, camera_port = port_c, transmit_port = port_t)
    
    c.run()
    c.end()







