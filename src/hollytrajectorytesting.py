import numpy as np

# Testing code for def make_trajectory function within trajectory controller. 
# not finished with trajectory making
# last edited 6/27/23 by Holly Chen hachen@hmc.edu
# current problems: - still needs to add trajectories from within the for loop into a saved trajectory array that can be returned
#                   - repeats poistion points at middle waypoints. 
#                   - lower priority for project so will not be continuing until we figure out robot point turns 

straight_line = np.array([[1, 1],
                       [2, 2],
                       [3, 3],
                       [4,4]])

straight_line_times = [0, 2, 6, 8]
delta_t = 1

traj_waypoints = straight_line # trajectory waypoints for the robot to follow from trajectory.py file
traj_times = straight_line_times # make in the trajectory.py file
       ### For loop for the # of times in waypoint_times (length of desired_times array)
       
times = np.array([])
for i in range(0, len(traj_times)-1):
    num_time_pts = int((traj_times[i+1]-traj_times[i])/delta_t)  ## the number of time pts for the robot to run trajectory between 2 waypoints. total_time is to help calculate the spacing of intermediate points and does not reflect actual overall time for robot to run trajectory
    print(num_time_pts)
    segment_times = (np.linspace(traj_times[i], traj_times[i+1], num_time_pts)) ## creates an array for intermediate time points betweeen 2 trajectory waypoint times 
    traj_segment = (np.linalg.norm(traj_waypoints[i+1] - traj_waypoints[i])/num_time_pts) ## genereates distance robot should travel between each intermediate time point
            ## adds intermediate positions for trajectory between 2 waypoints to the overall trajectory array. 
    #print("segment times = " + str(segment_times) + "type: " + str(type(segment_times)))
    #print("trajectory segment = " + str(traj_segment))
    times = np.append(times, segment_times) ## appends segment_times to the overall trajectory time array
print("times: "+ str(times))
traj_array_length = len(times)
trajectory = np.empty([traj_array_length,2]) ## initializes a trajectory position array
       
for i in range(0, len(traj_times)-1):
    #start_idx = 
    for j in range(0, num_time_pts): ## repeats position point close to the intermediate waypoints 
        trajectory=(traj_waypoints[i]+j*traj_segment) # creates intermediate trajectory position array between each waypoint
        #print(trajectory)

"""      for i in range(0, len(points)-1):
           start_idx = sum(lengths[0:i])
           self._path[start_idx:start_idx+lengths[i],:] = np.linspace(points[i], points[i+1], lengths[i], endpoint=False)
           print(self._path) ## 
"""