
# path tracking for differential drive

# include pointTracker.py
from point_tracker import trackPoint
from paths import *
import numpy as np
import matplotlib.pyplot as plt
norm = np.linalg.norm

look_ahead = 2
spacing = 5
dt = 0.01


'''
path_points = rect_points
path_times = rect_times
path_angles = rect_angles

def fillPath(times, points, angles, spacing, turning_time):
    startPoint = points[0]
    startTime = times[0]
    startAngle = angles[0]
    newPath = []
    newTimes = []
    newAngles = []
    for i in range(1, len(points)):
        nextPoint = points[i]
        nextTime = startTime + times[i]
        nextAngle = angles[i]
        vec = nextPoint - startPoint
        dist = norm(vec)
        num = int(dist/spacing)
        vecSmall = vec/num
        dt = (nextTime-startTime)/num
        pathSection = [startPoint + i*vecSmall for i in range(0, num+1)]
        timeSection = [startTime + i*dt for i in range(0, num+1)]
        angleSection = [startAngle] * (num+1)
        newPath += pathSection
        newTimes += timeSection
        newAngles += angleSection
        startTime = nextTime + turning_time
        startPoint = nextPoint
        startAngle = nextAngle
    return [newTimes, newPath, newAngles] '''

def findTarget(robot, path, lookAhead):
    dists = [norm(robot-point) for point in path]
    closest = dists.index(min(dists))
    target = closest + lookAhead
    return target

#newPath = fillPath(path, spacing)
#numPoints = len(newPath)
#targetIndex = 0


# initial conditions
robot_pos = np.array([-50, 0])
heading = 0

remaining_dist = 10
target = np.array([0, 0])
target_heading = np.pi

while remaining_dist > 1:

    #target = newPath[targetIndex]
    #print(target)
    [v, w] = trackPoint(robot_pos, target, heading, target_heading)
    xdot = v*np.cos(heading)
    ydot = v*np.sin(heading)
    dpos = np.array([xdot, ydot])*dt

    robot_pos = robot_pos + dpos
    heading += w*dt

    #targetIndex = findTarget(robot_pos, newPath, look_ahead)
    print(v)
    print(robot_pos[0])
    plt.scatter(robot_pos[0], robot_pos[1])
    remaining_dist = norm(robot_pos - target)

#plt.plot(path[:,0], path[:,1])

plt.xlabel("x position")
plt.ylabel("y position")
plt.axis('scaled')

plt.show()
