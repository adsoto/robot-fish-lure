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
                save_video=False, transmit_port='/dev/tty.usbmodem1402'):
       print("initializing controller")
       self._ser = serial.Serial(transmit_port, baudrate=115200)
       self._data_handler = dh.DataHandler(plot_data, save_data)
       self._video = orange.VideoProcessor(camera_port, camera_bounds, save_video)
       self._centroidTracker = centroidTracker.centroidTracker(camera_port, camera_bounds, save_video)
       self._robot_arr = []
       self._time_arr = []
       self._theta_arr = []
       self._fish_arr = []
       self._des_arr = []


   def send_commands(self, vR, vL):
       """Sends commands to the transmit board over the serial port"""
       print("vL = " + str(vL) + ", vR = " + str(vR))
       dict = {'vL': vL, 'vR' : vR}
       packet = str(dict) + "\r"
       self._ser.write(packet.encode())

   def find_target(self, traj, t):
       """Finds the next target in the path for the bot to track"""
       dt = 1 #is this still what we want? 
       X_r = self._video.get_robot_state(t) #in orange, do we even need this in here though?
       final_pos = [traj[-1][1], traj[-1][2]]
       ttrack = t+dt
       for i in range(1, len(traj)):
           #print('entered0')
           print("ttrack:",ttrack)
           if traj[i-1][0] <= ttrack <= traj[i][0]:
               print("entered1")
               t1 = traj[i-1][0]
               t2 = traj[i][0]
               percentTime = (ttrack-t1)/(t2-t1)
               pos1 = [traj[i-1][1], traj[i-1][2]]
               pos2 = [traj[i][1], traj[i][2]]
               distancevector = np.subtract(pos2, pos1) 
               target = pos1 + percentTime*distancevector
               print("target:" , target)
               X_des = object_state.Object(t, target[0], target[1], traj[-1][3])
               return X_des
           elif ttrack > traj[-1][0]:
               print('entered2')
               target = [traj[-1][1], traj[-1][2]]
               print("target:" , target)
               X_des = object_state.Object(t, target[0], target[1], traj[-1][3])
               return X_des
            # else case for if robot trajectory time is greater than ttrack 

    
   def run(self): #will we need to pass anything else into run? 
       #initialize clock
       start_time = time.time()
       current_time = time.time() - start_time
       max_time = 5 #change this as needed


       X_r = self._video.get_robot_state(current_time)
       #curr_time = X_r.t
       rob_pos = [X_r.x, X_r.y]
       rob_x = X_r.x
       rob_y = X_r.y

       B_x = B[0]
       B_y = B[1]
       A_x = A[0]
       A_y = A[1]

       #B_rob_dist = np.sqrt(np.square(B_x - rob_x) + np.square(B_y-rob_y))
       a_b_dist = np.sqrt(np.square(B_x - A_x) + np.square(B_y - A_y))
       dist = a_b_dist
       theta = np.arctan2((B_y - A_y), (B_x - A_x))
       #print("dist:", dist)
       print("rob_pos:", rob_x, rob_y)

       traj_t = make_traj_pts.straight_traj(dist, 0.05, current_time, A, theta)
       
       
       while current_time < max_time:
          #hard code Xdes to be 0.5 
          current_time = time.time() - start_time
          print("current time: ", current_time)
          X_r = self._video.get_robot_state(current_time) #in orange 

          print("robot state", X_r.x, X_r.y)
          X_f = self._centroidTracker.get_closest_fish_state(current_time) #closest fish
          #print("fish state" , X_f.x, X_f.y)

          #how to initialize an initial trajectory? 
          traj_t = get_traj.get_traj_function(X_r, X_f, traj_t) #how to set this up to keep feeding previous trajs?

          #traj_t = [[1, 0.1, 0.08, 0], [2, 0.25, 0.08, 0], [3, 0.5, 0.08, 0]]
          #put fish conditionals in get traj (is Xf null...)

          print("traj: ", traj_t)
          
          X_des = self.find_target(traj_t, current_time) #update find_target as well for these inputs

          #X_des = object_state.Object(current_time, 0.35, 0.08, 0)
          #print("X_des", X_des.x, X_des.y)
          #distance = X_r.distance_to(X_des)
          #print('distance: ', distance)

          
          [vRight, vLeft] = track_point(X_des, X_r) #update track_point function for these inputs
          #[vRight, vLeft] = [15, 15]
          
          self.send_commands(vRight, vLeft)


          if self._video._go:
               #self._time_arr.append(current_time)
               self._robot_arr.append(X_r)
               #self._theta_arr.append(theta)
               self._fish_arr.append(X_f)
               self._des_arr.append(X_des)
               self.send_commands(vRight, vLeft) # go as usual
          else:
               start_time = time.time() # reset start time
          self._video.display(X_des)


   def end(self):
    """Closes the serial port, video player, etc. and saves data"""
    print("entered")

    for i in range(50): self.send_commands(0, 0) # sending commands is unreliable, hence the 50x
    print("finished")
    self._ser.close()
    self._video.cleanup()


    t = [pos.t for pos in self._robot_arr]   
    x = [pos.x for pos in self._robot_arr]
    y = [pos.y for pos in self._robot_arr]
    theta = [pos.theta for pos in self._robot_arr]
    v = np.linalg.norm(np.diff(np.array([x, y])), axis=0)/np.diff(t) #what does this do?
    #trajectory = trajectory1
    xdes = [pos.x for pos in self._des_arr]
    ydes = [pos.y for pos in self._des_arr]
    tdes = [pos.t for pos in self._des_arr]
    thetades = [pos.theta for pos in self._des_arr]


    self._data_handler.add_series('desired path', xdes, ydes, 'x position', 'y position')
    self._data_handler.add_series('robot position', x, y, 'x position', 'y position')
       # emily commented these out


       ## overlay plots desired and actual position over time
    self._data_handler.add_dual_series('Position', xdes, ydes, x, y, 'x (m)', 'y (m)')
    self._data_handler.add_dual_series('X-Pos vs. Time', tdes, xdes, t, x, 'time(s)', "x (m)")
    self._data_handler.add_dual_series('Y-Pos vs. Time', tdes, ydes, t, y, 'time(s)', "y (m)")
    self._data_handler.add_dual_series('Theta vs. Theta Des', tdes, thetades, t, theta, 'time(s)', 'theta (rad)')
       
        ## add series saves raw data and then creates plots through data_handler.py
    self._data_handler.add_series('Desired Position', xdes, ydes,'x (m)', 'y (m)')
    self._data_handler.add_series('Actual Position', x, y,'x (m)', 'y (m)')

    self._data_handler.add_series('Desired X-Pos vs. Time', tdes, xdes, 'time(s)', "x (m)") ## need to have this line to get the correct time array for the desired position data
    self._data_handler.add_series('Actual X-Pos vs. Time', t, x, 'time(s)', "x (m)")

    self._data_handler.add_series('Desired Y-Pos vs. Time', tdes, ydes, 'time(s)', "y (m)")
    self._data_handler.add_series('Actual Y-Pos vs. Time', t, y, 'time(s)', "y (m)")

    self._data_handler.add_series("Desired Theta vs. Time", tdes, thetades, 'time(s)', "theta (rads)")
    self._data_handler.add_series('Theta vs. Time', t, theta, 'time(s)', 'theta (rads)')

    self._data_handler.add_series('Robot Velocity', t[1:], v, 'time (s)', 'velocity (m/s)')
       
    self._data_handler.run()
       
   
   
   #should be saving on a regular interval instead of after the fact
   #after the fact is ok for now

if __name__ == '__main__':
    #LAIR: [ 687  396][1483  801]
    #keck: [570,  311], [1442, 802]
    # keck camera 2: [[ 699    9], [1204  892]]
    camera_bounds = np.array([[590, 331], [1430, 801]]) # find these with calibrate_setup.py
    # find these with calibrate_setup.py
    port_t = '/dev/tty.usbmodem141302'                # find this with ls /dev/tty.usb*   Change this port as needed
    port_c = 0                                      # either 0 or 1
    c = Controller(camera_bounds = camera_bounds, camera_port = port_c, transmit_port = port_t)
    
    c.run()
    c.end()







