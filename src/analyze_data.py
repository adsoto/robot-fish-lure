import pandas as pd
import numpy as np
from kalman import KalmanFilter
import matplotlib.pyplot as plt
from paths import *

# This file may be useful for post-processing and analyzing data after the fact

df = pd.read_csv("data/05.05.2023/09.41.csv")

T = df['robot velocity_ind']
X = df['robot position_ind']
Y = df['robot position_dep']

T = T[:147]
X = X[:148]
Y = Y[:148]

plt.scatter(X, Y, label='robot position')
plt.plot(rect_points[:,0], rect_points[:,1], color="orange", label='desired path')
plt.xlabel('x position (m)')
plt.ylabel('y position (m)')
plt.axis('scaled')
plt.legend()
plt.show()

# Filter position and plot

start_pos = np.array([[X[0]], [Y[0]]])
start_var = np.array([[5, 0], [0, 5]])
kf = KalmanFilter(start_pos, start_var)

for i in range(0, len(X)):
    kf._predict(1)
    meas = np.array([[X[i]], [Y[i]]])
    kf._correct(meas)

kf._plot()

x = [state[0][0] for state in kf._state_hist]
y = [state[1][0] for state in kf._state_hist]

V = np.linalg.norm(np.diff(np.array([X[:-1], Y[:-1]])), axis=0)/np.diff(T)
v = np.linalg.norm(np.diff(np.array([x[:147], y[:147]])), axis=0)/np.diff(T)

plt.plot(T[:-1],V, label='raw velocity')
plt.plot(T[:-1],v, label='filtered velocity')
plt.xlabel('time (s)')
plt.ylabel('velocity (m/s)')
plt.legend()
plt.show()