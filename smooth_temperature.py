import pandas as pd
import sys
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from pykalman import KalmanFilter
lowess = sm.nonparametric.lowess
filename = sys.argv[1]

cpu_data = pd.read_csv(filename, parse_dates=['timestamp'])
plt.figure(1, figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)

#LOESS Smoothing
loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'], frac=0.005)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')

#Kalman Smoothing
kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1']]
kf = KalmanFilter(
    initial_state_mean = kalman_data.iloc[0],
    observation_covariance = np.diag([0.8, 0.4, 0.4]) ** 2, # TODO: shouldn't be zero
    transition_covariance = np.diag([0.1, 0.1, 0.1]) ** 2, # TODO: shouldn't be zero
    transition_matrices = [[1, -1, 0.7], [0, 0.6, 0.03], [0, 1.3, 0.8]] # TODO
)
kalman_smoothed, _ = kf.smooth(kalman_data)
#plt.figure(2, figsize=(12, 4))
#plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
plt.legend(['raw_data', 'loess_smoothed', 'kalman_smoothed'])
plt.xlabel('time')
plt.ylabel('cpu temperature in degC')
plt.savefig('cpu.svg')
plt.show()
