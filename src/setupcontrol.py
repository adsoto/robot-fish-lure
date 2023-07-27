"""setup file"""
import numpy as np
from paths import *

global setup
setup = "KECK"

global bounds # find these with calibrate_setup.py
#LAIR: [ 687  396][1483  801]
#keck: [595,  331], [1425, 801]
if setup == "LAIR":
    bounds = np.array([[601, 362], [1414, 782]])   #CHANGE THESE! THESE ARE TANK BOUNDS
else: 
    bounds = np.array([[570,  300], [1450, 820]])

global inmeters
points = straight_line # change the robot path here
inmeters = True  # change this when path changes --> is the path in meters? if yes--> true 