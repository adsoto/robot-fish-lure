# gain constants
K_R = 1
K_A = 1.5 #3 # 1.7 gain improves the overshoot during turns 
K_B = 0 #0 # desired angle tracking not implemented

# stability criteria:
# K_R > 0, K_B < 0, K_A - K_R > 0

L = .108 # robot dimensions
R = .034

import numpy as np
#import object_state

# def track_point(robot, dest, theta, theta_des): #what were robot and dest formats here?
#     """Point tracking using proportional control for a differential drive robot"""

#     # geometry
#     r2dest = dest-robot
#     rho = np.linalg.norm(r2dest)
#     alpha = -theta + np.arctan2(r2dest[1], r2dest[0])
#     beta = theta_des - theta - alpha
#     if alpha < -np.pi: alpha = alpha + np.pi*2 # keep alpha within -pi to pi
#     elif alpha >  np.pi: alpha = alpha - np.pi*2
#     if beta < -np.pi: beta = beta + np.pi*2 # keep beta within -pi to pi
#     elif beta >  np.pi: beta = beta - np.pi*2

#     # proportional control
#     v = K_R*rho
#     w = K_A*alpha + K_B*beta

#     # control signals
#     vRight = (2*v + w*L)/(2*R)
#     vLeft = (2*v - w*L)/(2*R)

#     # scaling to 64ths of a rotation per second, bounded from -120 to 120 rpm
#     vRight = max(-128, min(128, 64*vRight/(2*np.pi)))
#     vLeft = max(-128, min(128, 64*vLeft/(2*np.pi)))

#     return np.array([vRight, vLeft])



def track_point(desired_state, current_state):
    """Point tracking using proportional control for a differential drive robot"""
    theta = current_state.theta
    theta_des = desired_state.theta
    deltay = desired_state.y - current_state.y
    deltax = desired_state.x - current_state.x

    print("desired state from track point: ", desired_state.x, desired_state.y)

    # i think we will have to redo these slightly 
    # rho should be distance to?
    # need to revise lecture videos
    #r2dest = desired_coords - current_coords
    #rho = np.linalg.norm(r2dest) #is this going to work now? 
    rho = current_state.distance_to(desired_state)
    print("rho: ", rho)
    #alpha = -theta + np.arctan2(r2dest[1], r2dest[0])
    alpha = -theta + np.arctan2(deltay, deltax) #think there is an issue with alpha - ask 
    print("alpha: ", alpha)
    beta = theta_des - theta - alpha
    
    if alpha < -np.pi: alpha = alpha + np.pi*2 # keep alpha within -pi to pi
    elif alpha >  np.pi: alpha = alpha - np.pi*2
    if beta < -np.pi: beta = beta + np.pi*2 # keep beta within -pi to pi
    elif beta >  np.pi: beta = beta - np.pi*2

    # proportional control
    v = K_R*rho
    w = K_A*alpha + K_B*beta

    # control signals
    vRight = (2*v + w*L)/(2*R)
    vLeft = (2*v - w*L)/(2*R)

    # scaling to 64ths of a rotation per second, bounded from -120 to 120 rpm
    vRight = max(-128, min(128, 64*vRight/(2*np.pi)))
    vLeft = max(-128, min(128, 64*vLeft/(2*np.pi)))

    return np.array([vRight, vLeft])
