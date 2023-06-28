# implements a point turn when the robot is within a certain distances of a waypoint  
# gain constants 1.8, 2.5, -0.001
K_R = 1.8
K_A = 2.5 #3 # 1.7 gain improves the overshoot during turns
K_B = -0.001 #0 # desired angle tracking not implemented


# stability criteria:
# K_R > 0, K_B < 0, K_A - K_R > 0


L = .108 # robot dimensions
R = .034


import numpy as np


def track_point(robot, dest, theta, theta_des):
    """Point tracking using proportional control for a differential drive robot"""


    # geometry
    r2dest = dest-robot
    rho = np.linalg.norm(r2dest)
    alpha = -theta + np.arctan2(r2dest[1], r2dest[0])
    beta = theta_des - theta - alpha
    if alpha < -np.pi: alpha = alpha + np.pi*2 # keep alpha within -pi to pi
    elif alpha > np.pi: alpha = alpha - np.pi*2
    if beta < -np.pi: beta = beta + np.pi*2 # keep beta within -pi to pi
    elif beta > np.pi: beta = beta - np.pi*2


    ### edits: point turns if robot within waypoint radius
    K_rot = 1.4 # 1.5 csv:15.39, # 1 csv: 
    wypt_radius = 0.05 # 3 cm
    accep_angle_error = 0.01 #radian
    #dt =0.08

    # checks if robot is near waypoint and if angle error is larger than desired ---> if yes, results in point turn
    print(alpha)
    if np.linalg.norm(robot - dest) < wypt_radius and alpha > accep_angle_error:
        v = 0 
        w = K_rot*alpha # + K_A*alpha + K_B*beta
        print(np.linalg.norm(robot - dest))
        print('rot only')


    else: # normal control gains
        v = K_R*rho
        w = K_A*alpha + K_B*beta
        print('normal')
    # control signals
    vRight = (2*v + w*L)/(2*R)
    vLeft = (2*v - w*L)/(2*R)


    # scaling to 64ths of a rotation per second, bounded from -120 to 120 rpm
    vRight = max(-128, min(128, 64*vRight/(2*np.pi)))
    vLeft = max(-128, min(128, 64*vLeft/(2*np.pi)))

    return np.array([vRight, vLeft])

#def turn_near_wypt(robot, dest, theta, theta_des)
