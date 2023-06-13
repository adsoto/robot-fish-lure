"""Main file for running robotic fish. Power robot on, then run controller to carry out image processing,
velocity tracking/calculation, and transmitting speeds to robot over radio"""

"""This new (summer 2023) controller was edited to follow ORANGE dots on the robot -- it calls orange.py as the videoprocessor. This controller and orange.py saves video when save_video = True.

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

class Controller():
   """Top-level class to run the robotic fish"""

   def __init__(self, lookahead=20, spacing=.001, plot_data=True, save_data=True,
                total_time=30, camera_port=0, camera_bounds = np.array([[420, 365], [1340, 905]]),
                save_video=True, transmit_port='/dev/tty.usbmodem14102'):
       print("initializing controller")
       self._ser = serial.Serial(transmit_port, baudrate=115200)
       self._lookahead = lookahead
       self._data_handler = dh.DataHandler(plot_data, save_data)
       self._video = orange.VideoProcessor(camera_port, camera_bounds, save_video)
       self._make_path(spacing, total_time)
       self._robot_arr = []
       self._time_arr = []
       self._theta_arr = []

   def _make_path(self, spacing, total_time):
       """Interpolates points to construct a continuous path for the bot to follow"""
      
       points = line_points_m #change what path the robot follows from paths.py file here
       lengths = []
       for i in range(0, len(points)-1):
           lengths.append(int(np.linalg.norm(points[i+1]-points[i])/spacing)) ##the spacing constant scales the lengths.
       total_length = sum(lengths)
       ## chsange self._times = to some time vector that is dependent on theta (amount robot needs to turn)
       self._times = np.linspace(0, total_time, total_length) ## np.linspace creates evenly spaced intervals over specified interval.
       self._path = np.empty([total_length, 2])

       for i in range(0, len(points)-1):
           start_idx = sum(lengths[0:i])
           self._path[start_idx:start_idx+lengths[i],:] = np.linspace(points[i], points[i+1], lengths[i], endpoint=False)
      
   def send_commands(self, vR, vL):
       """Sends commands to the transmit board over the serial port"""
       print("vL = " + str(vL) + ", vR = " + str(vR))
       dict = {'vL': vL, 'vR' : vR}
       packet = str(dict) + "\r"
       self._ser.write(packet.encode())

   def find_target(self, currentTime):
       """Finds the next target in the path for the bot to track"""

       timeDists = [abs(time-currentTime) for time in self._times]
       timeDistance = min(timeDists)
       closest = timeDists.index(timeDistance)
       return closest + self._lookahead

   def run(self):
       """Runs the bot"""
       start_time = time.time()
       targetIndex = self._lookahead


       while targetIndex < len(self._path):
           [head, tail] = self._video.get_coords(2)
           fish_vect = head - tail
           theta = np.arctan2(fish_vect[1], fish_vect[0])
           robot_pos = (head + tail)/2
           currentTime = time.time() - start_time


           target = self._path[targetIndex]
           [vRight, vLeft] = track_point(robot_pos, target, theta, 0) # note theta_des = 0
          
           targetIndex = self.find_target(currentTime)


           if self._video._go:
               self._time_arr.append(currentTime)
               self._robot_arr.append(robot_pos)
               self._theta_arr.append(theta)
               self.send_commands(vRight, vLeft) # go as usual
           else:
               start_time = time.time() # reset start time
           self._video.display(target)
  
   def end(self):
       """Closes the serial port, video player, etc. and saves data"""


       for i in range(50): self.send_commands(0, 0) # sending commands is unreliable, hence the 50x
       self._ser.close()
       self._video.cleanup()


       x = [pos[0] for pos in self._robot_arr]
       y = [pos[1] for pos in self._robot_arr]
       v = np.linalg.norm(np.diff(np.array([x, y])), axis=0)/np.diff(self._time_arr) #what does this do?
       xdes = [pos[0] for pos in self._path]
       ydes = [pos[1] for pos in self._path]


       #self._data_handler.add_series('desired path', xdes, ydes, 'x position', 'y position')
       #self._data_handler.add_series('robot position', x, y, 'x position', 'y position')
       # emily commented these out


       ## working plots but not saving data properly
       self._data_handler.add_dual_series('Position', xdes, ydes, x, y, 'x (m)', 'y (m)')
       self._data_handler.add_dual_series('X-Pos vs. Time', self._times, xdes, self._time_arr, x, 'time(s)', "x (m)")
       self._data_handler.add_dual_series('Y-Pos vs. Time', self._times, ydes, self._time_arr, y, 'time(s)', "y (m)")
       self._data_handler.add_series('Theta vs. Time', self._time_arr, self._theta_arr, 'time(s)', 'theta')
       self._data_handler.add_series('Robot Velocity', self._time_arr[1:], v, 'time (s)', 'velocity (m/s)')
       self._data_handler.run()
       

if __name__ == '__main__':
   bounds = np.array([[720,  435], [1592, 778]])   # find these with calibrate_setup.py
   port_t = '/dev/tty.usbmodem14102'                # find this with ls /dev/tty.usb*   Change this port as needed
   port_c = 0                                      # either 0 or 1
   c = Controller(camera_bounds = bounds, camera_port = port_c, transmit_port = port_t,
                  lookahead = 10, total_time = 10)
   c.run()
   c.end()