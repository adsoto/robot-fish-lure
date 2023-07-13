# gain constants
K_R = 1.2
K_A = 1.5 #3 # 1.7 gain improves the overshoot during turns - tracks path forward
K_B = -0.3 #0 # desired angle tracking not implemented - tracks theta 

# stability criteria:
# K_R > 0, K_B < 0, K_A - K_R > 0

L = .108 # robot dimensions
R = .034

import numpy as np
#import object_state

def track_point(desired_state, current_state):
    """Point tracking using proportional control for a differential drive robot"""
    theta = current_state.theta
    theta_des = desired_state.theta
    deltay = desired_state.y - current_state.y
    deltax = desired_state.x - current_state.x

    rho = current_state.distance_to(desired_state)
    #alpha = -theta + np.arctan2(r2dest[1], r2dest[0])
    alpha = -theta + np.arctan2(deltay, deltax) #think there is an issue with alpha - ask 
    beta = theta_des - theta - alpha
    
    if alpha < -np.pi: alpha = alpha + np.pi*2 # keep alpha within -pi to pi
    elif alpha >  np.pi: alpha = alpha - np.pi*2
    if beta < -np.pi: beta = beta + np.pi*2 # keep beta within -pi to pi
    elif beta >  np.pi: beta = beta - np.pi*2

    ### edits: point turns if robot within waypoint radius
    K_rot = 1.2 # 1.5 csv:15.39, # 1 csv: 
    wypt_radius = 0.05 # _ cm 
    accep_angle_error = 0.01 #radian 
    curr_to_des_dist = np.sqrt(np.square(deltay) + np.square(deltax))

    # checks if robot is near waypoint and if angle error is larger than desired ---> if yes, results in point turn
    if curr_to_des_dist < wypt_radius and alpha > accep_angle_error:
        v = 0 
        w = K_rot*alpha # + K_A*alpha + K_B*beta
        #print('rot only')
        print(alpha)
    else: # normal control gains
        v = K_R*rho
        w = K_A*alpha + K_B*beta

    # control signals
    vRight = (2*v + w*L)/(2*R)
    vLeft = (2*v - w*L)/(2*R)

    # scaling to 64ths of a rotation per second, bounded from -120 to 120 rpm
    vRight = max(-128, min(128, 64*vRight/(2*np.pi)))
    vLeft = max(-128, min(128, 64*vLeft/(2*np.pi)))

    return np.array([vRight, vLeft])
