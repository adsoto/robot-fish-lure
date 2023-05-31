import numpy as np
import matplotlib.pyplot as plt

"""Generate matplot of desired paths for robot"""

PIX2METERS = .842/1071

path_points = np.array([[100,700],
                       [700,700],
                       [700,550],
                       [100,550],
                       [100,400],
                       [700,400],
                       [700,250],
                       [100,250]])

path_times = [0, 5, 10, 15, 20, 25, 30, 35]

# Plotting
plt.figure(1)
plt.plot(path_points[:,0]*PIX2METERS*100, path_points[:,1]*PIX2METERS*100, label="desired path")
plt.xlabel("x position (cm)")
plt.ylabel("y position (cm)")
plt.legend(loc="upper left")
plt.axis('scaled')

plt.show()
