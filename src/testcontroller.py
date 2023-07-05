


"""Trajectory tracking for running robotic fish. Power robot on, then run trajectory controller to carry out image processing,
velocity tracking/calculation, and transmitting speeds to robot over radio"""

"""This new (summer 2023) controller was edited to follow ORANGE dots on the robot -- it calls orange.py as the videoprocessor. This trajectory controller and orange.py saves video when save_video = True.

Declans version is called "originalcontroller.py" and utilizes videoprocessor.py to follow black dots. It also DOES NOT save video.
"""
import numpy as np
import serial
import time
from point_tracker import track_point
from paths import *
import data_handler as dh
import matplotlib.pyplot as plt
import video_processor as vp
import orange as orange
trajectory = rect_trajectory
totaltime = trajectory[len(trajectory)-1][0]

class Controller():
   """Top-level class to run the robotic fish"""

   def __init__(self, lookahead=20, spacing=.001, plot_data=True, save_data=True, camera_port=0, camera_bounds = np.array([[420, 365], [1340, 905]]),
                save_video=False, transmit_port='/dev/tty.usbmodem1402'):
       print("initializing controller")
       self._ser = serial.Serial(transmit_port, baudrate=115200)
       self._lookahead = lookahead
       self._data_handler = dh.DataHandler(plot_data, save_data)
       self._video = orange.VideoProcessor(camera_port, camera_bounds, save_video)
       self._robot_arr = []
       self._time_arr = []
       self._theta_arr = []

   def updateTraj(self, trajectory):
      for traj in trajectory:
            traj[0]=traj[0]+totaltime
      print(trajectory) 
      return trajectory

   def send_commands(self, vR, vL):
       """Sends commands to the transmit board over the serial port"""
       #print("vL = " + str(vL) + ", vR = " + str(vR))
       dict = {'vL': vL, 'vR' : vR}
       packet = str(dict) + "\r"
       self._ser.write(packet.encode())

   def find_target(self, trajectory, currentTime):
       """Finds the next target in the path for the bot to track"""
       dt = 0.08
       [head, tail] = self._video.get_coords(2)
       fish_vect = head - tail
       theta = np.arctan2(fish_vect[1], fish_vect[0])
       robot_pos = (head + tail)/2
       final_pos = [trajectory[len(trajectory)-1][1], trajectory[len(trajectory)-1][2]]
       #currentTime = time.time() - start_time
       ttrack = currentTime+dt
       for i in range(1, len(trajectory)):
           if trajectory[i-1][0] < ttrack < trajectory[i][0]:
               t1 = trajectory[i-1][0]
               t2 = trajectory[i][0]
               percentTime = (ttrack-t1)/(t2-t1)
               pos1 = [trajectory[i-1][1], trajectory[i-1][2]]
               pos2 = [trajectory[i][1], trajectory[i][2]]
               distancevector = np.subtract(pos2, pos1) 
               target = pos1 + percentTime*distancevector
               #if target[0]>final_pos[0]: #there needs to be a better check for this, will only work for forward line 
                   #target = final_pos

               #print(t1, t2, ttrack)
           elif ttrack > trajectory[len(trajectory)-1][0]:
               target = [trajectory[len(trajectory)-1][1], trajectory[len(trajectory)-1][2]]
       
            # else case for if robot trajectory time is greater than ttrack - holly
       return target


   def run(self):
       """Runs the bot"""
       #global start_time
       start_time = time.time()
       currentTime = time.time() - start_time
       #targetIndex = self._lookahead

       #trajectory = trajectory1 
       tmax = trajectory[len(trajectory)-1][0]
       #print(tmax)

       #print(len(self._path)) ###
       #print(targetIndex)
       while currentTime < tmax:
           [head, tail] = self._video.get_coords(2)
           fish_vect = head - tail
           theta = np.arctan2(fish_vect[1], fish_vect[0])
           robot_pos = (head + tail)/2
           currentTime = time.time() - start_time

           target1 = self.find_target(trajectory, currentTime)
           
           [vRight, vLeft] = track_point(robot_pos, target1, theta, 0) # note theta_des = 0
          
           #targetIndex = self.find_target(currentTime)
           #print(targetIndex) ###

           if self._video._go:
               self._time_arr.append(currentTime)
               self._robot_arr.append(robot_pos)
               self._theta_arr.append(theta)
               self.send_commands(vRight, vLeft) # go as usual
           else:
               start_time = time.time() # reset start time
           self._video.display(target1)

           print('time:', currentTime)
           print('target:', target1) 
           print('pos:', robot_pos)


  
   def end(self):
       """Closes the serial port, video player, etc. and saves data"""
       print("entered")

       for i in range(50): self.send_commands(0, 0) # sending commands is unreliable, hence the 50x
       print("finished")
       self._ser.close()
       self._video.cleanup()
       
       x = [pos[0] for pos in self._robot_arr]
       y = [pos[1] for pos in self._robot_arr]
       v = np.linalg.norm(np.diff(np.array([x, y])), axis=0)/np.diff(self._time_arr) #what does this do?
       #trajectory = trajectory1
       xdes = [pos[1] for pos in trajectory]
       ydes = [pos[2] for pos in trajectory]
       tdes = [pos[0] for pos in trajectory ]


       self._data_handler.add_series('desired path', xdes, ydes, 'x position', 'y position')
       self._data_handler.add_series('robot position', x, y, 'x position', 'y position')
       # emily commented these out


       ## overlay plots desired and actual position over time
       self._data_handler.add_dual_series('Position', xdes, ydes, x, y, 'x (m)', 'y (m)')
       self._data_handler.add_dual_series('X-Pos vs. Time', tdes, xdes, self._time_arr, x, 'time(s)', "x (m)")
       self._data_handler.add_dual_series('Y-Pos vs. Time', tdes, ydes, self._time_arr, y, 'time(s)', "y (m)")
       
        ## add series saves raw data and then creates plots through data_handler.py
       self._data_handler.add_series('Desired Position', xdes, ydes,'x (m)', 'y (m)')
       self._data_handler.add_series('Actual Position', x, y,'x (m)', 'y (m)')
       self._data_handler.add_series('Desired X-Pos vs. Time', tdes, xdes, 'time(s)', "x (m)") ## need to have this line to get the correct time array for the desired position data
       self._data_handler.add_series('Actual X-Pos vs. Time', self._time_arr, x, 'time(s)', "x (m)")

       self._data_handler.add_series('Desired Y-Pos vs. Time', tdes, ydes, 'time(s)', "y (m)")
       self._data_handler.add_series('Actual Y-Pos vs. Time', self._time_arr, y, 'time(s)', "y (m)")

       self._data_handler.add_series('Theta vs. Time', self._time_arr, self._theta_arr, 'time(s)', 'theta (rads)')
       self._data_handler.add_series('Robot Velocity', self._time_arr[1:], v, 'time (s)', 'velocity (m/s)')
       
       self._data_handler.run()
       

if __name__ == '__main__':
    #LAIR: [ 687  396][1483  801]
    #keck: [570,  311], [1442, 802]
    # keck camera 2: [[ 699    9], [1204  892]]
   bounds = np.array([[570,  311], [1442, 802]])   # find these with calibrate_setup.py

   port_t = '/dev/tty.usbmodem1302'                # find this with ls /dev/tty.usb*   Change this port as needed
   port_c = 0                                      # either 0 or 1
   c = Controller(camera_bounds = bounds, camera_port = port_c, transmit_port = port_t,
                  lookahead = 1)
   
   
   c.run()
   c.end()
