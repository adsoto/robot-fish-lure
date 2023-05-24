import numpy as np
import matplotlib.pyplot as plt

class KalmanFilter():
    """Kalman Filter to smooth out CV state estimate"""

    def __init__(self, start_state, start_var):
        self._state = start_state
        self._variance = start_var
        self._A = np.array([[1, 0], [0, 1]]) # state transition matrix
        self._meas_var = np.array([[10, 0], [0, 10]]) # measurement variance matrix
        self._sys_var = np.array([[1, 0], [0, 1]]) # system variance matrix
        self._state_hist = [start_state]
        self._var_hist = [start_var]
        self._meas_hist = [start_state]

    def _predict(self, dt):
        """Prediction step"""

        self._state = self._A @ self._state
        self._variance = self._A @ self._variance @ np.transpose(self._A) + self._sys_var
    
    def _correct(self, meas):
        """Correction step"""
        
        K = self._variance @ np.linalg.inv(self._variance + self._meas_var)
        self._state = self._state + K @ (meas - self._state)
        self._variance = (np.identity(2) - K) @ self._variance
        self._state_hist.append(self._state)
        self._var_hist.append(self._variance)
        self._meas_hist.append(meas)

    def _plot(self):
        x = [state[0] for state in self._state_hist]
        y = [state[1] for state in self._state_hist]
        xm = [state[0] for state in self._meas_hist]
        ym = [state[1] for state in self._meas_hist]
        plt.figure(1)
        plt.plot(x, y, label='estimates')
        plt.plot(xm, ym, label='measurements')
        plt.xlabel('x position (m)')
        plt.ylabel('y position (m)')
        plt.legend()
        plt.axis('scaled')
        plt.show()



if __name__ == '__main__':
    start_pos = np.array([[0], [0]])
    start_var = np.array([[5, 0], [0, 5]])
    kf = KalmanFilter(start_pos, start_var)

    for i in range(0, 40):
        kf._predict(1)
        meas = np.array([[i], [0]]) + np.random.normal(0,1,[2,1])
        kf._correct(meas)
    
    kf._plot()

