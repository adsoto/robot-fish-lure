import numpy as np
import matplotlib.pyplot as plt
norm = np.linalg.norm

TANK_WIDTH = 915
TANK_HEIGHT = 540
TANK = np.array([[0, 0],
                 [TANK_WIDTH, 0],
                 [TANK_WIDTH, TANK_HEIGHT],
                 [0, TANK_HEIGHT],
                 [0, 0]])
MAX_FORCE = 10 ## Fild Dorce pushback from the tank walls
PREDATOR_K = 0.02
TARGET_DIST_SCALE = 10

QUAD_B = 800
QUAD_A = MAX_FORCE/(QUAD_B**2)
QUAD_B_TANK = 400
QUAD_A_TANK = MAX_FORCE/(QUAD_B_TANK**2)

tank_x_slope = 2*MAX_FORCE/TANK_WIDTH
tank_y_slope = 2*MAX_FORCE/TANK_HEIGHT

pred_pos = np.array([TANK_WIDTH/4, TANK_HEIGHT/4])
#pred_pos = np.array([100, 250])


def get_tank_force(robot): # assuming origin is in lower left
    x_force = (TANK_WIDTH/2 - robot[0])*tank_x_slope # This equation helps set the force of the magnetic fields of the tank.
    y_force = (TANK_HEIGHT/2 - robot[1])*tank_y_slope 
    return np.array([x_force, y_force])

def get_tank_force_quadratic(robot): # assuming origin is in lower left
    x = TANK_WIDTH/2 - robot[0]
    y = TANK_HEIGHT/2 - robot[1]
    x_force = QUAD_A*(x-QUAD_B)**2 if x < QUAD_B else 0
    y_force = QUAD_A*(y-QUAD_B)**2 if y < QUAD_B else 0
    return np.array([x_force, y_force])

def get_force(robot):
    return get_tank_force(robot)

def get_target(robot):
    force = get_force(robot)
    return robot + force*TARGET_DIST_SCALE

x,y = np.meshgrid(np.linspace(0,TANK_WIDTH,40),np.linspace(0,TANK_HEIGHT,20)) 

u = x.copy()
v = y.copy()

for row in range(0, len(x)):
    for col in range(0, len(x[0])):
        xi = x[row, col] 
        yi = y[row, col]
        tank_force = get_tank_force(np.array([xi, yi]))
        force = tank_force
        u[row, col] = force[0] #
        v[row, col] = force[1] #

plt.quiver(x,y,u,v)

plt.scatter(pred_pos[0], pred_pos[1], label="predator")
#plt.plot(TANK[:,0], TANK[:,1])

#plt.legend(loc="upper right")
plt.axis('scaled')
plt.show()