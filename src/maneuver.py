import numpy as np
from make_traj_pts import straight_traj, rot_traj

class Maneuver():
    
    def __init__(self,type = 'straight', dist = 0.2, angle = 0, v = 0.05, w = 0):
        """Maneuver constructor method"""
        print('initializing maneuver')
        # default values 
        self.type = 'straight' #not sure how to initialize a string 
        self.dist = 0.2
        self.angle = 0
        self.v = 0.05
        self.w = 0

    def to_traj(self, type, X_r, move_dir):
        if type == 'straight':
            return straight_traj(self.dist, self.v, X_r, move_dir) # move_dir is the direction the robot will move for the line. ex: if move_dir = 0, robot will move strictly to the right. if move_dir = pi/2, robot will move straight up no matter the starting facing of the robot. 
        elif type == "rotate":
            return rot_traj(self.angle, self.w, X_r)

if __name__ == '__main__':
    # not sure if these objects should be created here or in the controller file when 
    straight1 = Maneuver('straight', 0.1, 0, 0.05, 0, 0) #(type, dist, angle, v, w)
    rot1 = Maneuver('rotate', 0, np.pi/2, 0, np.pi/32) #(type, dist, angle, v, w)

