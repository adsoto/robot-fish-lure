"""dictates up the paths and calibration setup"""
"""setup file"""

import numpy as np
from paths import *

global setup
setup = "LAIR"

global bounds # find these with calibrate_setup.py
#LAIR: [ 687  396][1483  801]
#keck: [595,  331], [1425, 801]
if setup == "LAIR":
    bounds = np.array([[595,  331], [1425, 801]])   #CHANGE THESE! THESE ARE TANK BOUNDS
else: 
    bounds = np.array([[595,  331], [1425, 801]])

global inmeters
points = straight_line # change the robot path here
inmeters = True  # change this when path changes --> is the path in meters? if yes--> true 
