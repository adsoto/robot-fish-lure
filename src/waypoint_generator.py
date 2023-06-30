# creates functions that will take user input and run straight or turn 
import numpy as np

start_pos = np.array([0,0])
start_time = 0
dt = 1
start_theta = -np.pi/2

def straight_wypt(dist, vel, start_time, start_pos, theta_dir): # theta_dir is the direction that you want the line to be in 
    """generates a single trajectory waypoint for the robot to move the desired distance at the desired speed """
    
    total_time = dist/vel
    num_pts = round(total_time/dt)
    print(num_pts)
    wypts = np.empty([])
    for i in range(1,num_pts+1):
        new_x = ( start_pos[0] + (i/num_pts * np.cos(theta_dir)) )
        new_y = ( start_pos[1] + (i/num_pts) * np.sin(theta_dir) ) 
        new_time = start_time + i*dt
        wypts = np.array([new_time, new_x, new_y, theta_dir])
        print(wypts)
        ### !! How do i return this in an array of arrays when array sizes cannot be changed??
        #wypts[i] = [new_time, new_x, new_y, theta_dir]
    

    # new_x = round(start_pos[0]+dist*np.cos(theta_dir), 4)
    # new_y = round(start_pos[1]+dist*np.sin(theta_dir),4)
    # new_time = start_time+dist/vel
    # new_theta = round(theta_dir, 4) # idk if des_theta in the trajectory actually does anything
    # new_wypt = np.array([new_time, new_x, new_y, new_theta])
    
    start_pos = [new_x, new_y]
    start_time = total_time
    # returns a waypoint and the start_pos and start_time required as input for a following waypoint
    return wypts, start_time, start_pos, theta_dir

### straight
wp1, start_time1, start_pos1, start_theta1 = straight_wypt(1, 0.2, start_time, start_pos, start_theta)
#print(wp1)
# wp2 = straight_wypt(1, 0.2, start_time1, start_pos1, start_theta1)[0]
# print(wp2)



# waypoint format: [time, x, y, theta]



def turn(radians, angular_vel, start_time, start_pos, current_theta):
    """turns the robot by _ radians at __ angular_velocity"""
    # + radians CCW
    # - radians CW
    total_t = abs(radians/angular_vel)
    num_pts = round(total_t/dt)
    d_theta = dt*angular_vel
    print(num_pts)
    final_theta = np.mod(radians,np.pi*2)

    new_start_time = start_time+total_t

    wypts = np.empty([])
    for i in range(1, num_pts+1):
        new_time = start_time+i*dt
        ## if current_theta is + 
        ## check when current_theta is negative

        # for CCW roatation (+ radians)

        new_theta = current_theta + (radians)*(i/num_pts)
        
        # angle wrapping
        if new_theta > np.pi:
            new_theta = -np.pi*2 + new_theta

        elif new_theta < -np.pi:
            new_theta = new_theta + np.pi*2

        wypts = np.array([new_time, start_pos[0], start_pos[1], new_theta])
        print(wypts)
        #print(wypts)
    return wypts, new_start_time, start_pos, final_theta  

#wp3, start_time3, start_pos3, start_theta3 = turn(np.pi, np.pi/4, start_time, start_pos, start_theta)
wp3 = turn(-2*np.pi, np.pi/4, start_time, start_pos, start_theta)[0]
#print(wp3)







