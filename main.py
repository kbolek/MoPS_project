"""Main program contains, calculation of river discharge, level of water in the river
    and river cross section"""

import json
import math
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import time
from scipy.special import logsumexp

class MainApplication(object):
    def __init__(self):
        self.dx = None
        self.L = None
        self.Mt = None
        self.Tt = None
        self.Tw = None
        self.x = None
        self.Nx = None
        self.R = None
        with open('settings.json') as self.file:
            self.parameters = json.load(self.file)

    def calculateVariables(self):
        # number of cross sections:
        self.L = self.parameters['L']
        self.dx = self.parameters['dx']
        self.Nx = int(self.L / self.dx) + 1
        # number of cross section stations
        self.x = np.arange(0, (self.Nx)*self.dx, self.dx, dtype=int)
        # [hours] flood wave period
        self.Tpw = self.parameters['Tpw']
        # maximum time required for the entrance of the flood wave into the channel
        self.Tw = self.Tpw / 2
        # [hours] time required for steady state to be established
        self.Ts = self.parameters['Ts']
        # total time of simulation
        self.Tt = self.Ts + self.Tw + self.parameters['Ta']
        # total number of time steps
        self.Mt = math.floor(self.Tt * 3600 / self.parameters['Dt'])
        self.Qt1 = self.parameters['Qt1']
        self.Q0 = self.parameters['Q0']
        self.At1 = self.parameters['At1']
        # [seconds] - time step
        self.Dt = self.parameters['Dt']
        # width of the channel
        self.B = self.parameters['B']
        # [m3/s] discharge of the river
        self.Q = np.zeros(shape=(self.Nx, self.Mt))
        # [m2] cross section area
        self.A = np.zeros(shape=(self.Nx, self.Mt))
        # depth
        self.h = np.zeros(shape=(self.Nx, self.Mt))
        # Initial conditions
        self.Q[:, 0] = self.Qt1
        self.A[:, 0] = self.At1
        # water levels
        self.h[:, 0] = self.A[:, 0]/self.B
        # time step
        self.T = np.arange(0, (self.Mt)*self.Dt, self.Dt, dtype=int)
        # [m/s2] - gravitational acceleration
        self.g = self.parameters['g']
        # [m^(-1/3) s] - Manning roughness coefficient
        self.n = self.parameters['n']
        # [m/m] - slope of the bottom of the channel
        self.S0 = self.parameters['S0']
        # water amplitude
        self.a = self.parameters['a']

    def update_plot_data(self):
        plt.ion()
        fig, axs = plt.subplots(2)
        for t in range(0, self.Mt-1):
            for i in range(0, self.Nx):
                if i == 0:
                    # FIRST TIME PERIOD:  the river flows without flood => the system stabilizes itself
                    if (self.T[t] >= 0) and (self.T[t] < self.Ts * 3600):
                        self.Q[i, t + 1] = self.Q0
                        # initial condition based on the row above
                        self.A[i, t + 1] = self.A[i, t] - self.Dt / self.dx * (self.Q[i + 1, t] - self.Q[i, t])

                        # SECOND TIME PERIOD: flood wave is entering the channel - upstream boundary condition
                    elif (self.T[t] >= self.Ts * 3600) and (self.T[t] <= (self.Tw + self.Ts) * 3600):
                        # application of sinus function which represents the wave
                        self.Q[i, t + 1] = self.Q0 * (2.0 + self.a * np.sin(2 * np.pi * self.T[t] / self.Tpw * 3600))
                        self.A[i, t + 1] = self.A[i, t] - self.Dt / self.dx * (self.Q[i + 1, t] - self.Q[i, t])

                        # THRID PERIOD: flood wave left the channel
                    elif self.T[t] > ((self.Tw + self.Ts) * 3600):
                        self.Q[i, t + 1] = self.Q0
                        self.A[i, t + 1] = self.A[i, t] - self.Dt / self.dx * (self.Q[i + 1, t] - self.Q[i, t])

                    self.R = self.A[i, t + 1] / (2.0 * self.A[i, t + 1] / self.B + self.B)
                    self.h[i, t + 1] = self.A[i, t + 1] / self.B

                else:
                    self.R = self.A[i, t] / (self.A[i, t] / self.B * 2.0 + self.B)
                    alpham = (2.0 * self.Q[i, t] / self.A[i, t]) + (
                            (self.g * self.A[i, t] / self.B) - (self.Q[i, t] ** 2 / self.A[i, t] ** 2)) / (
                                     (self.Q[i, t] / self.A[i, t]) * (5.0 / 3.0 - (4.0 / 3.0) * (self.R / self.B)))
                    betam = self.g * self.A[i, t] * (
                            (self.Q[i, t] ** 2) * self.n ** 2 / ((self.A[i, t] ** 2) * self.R ** (4.0 / 3.0)) - self.S0)
                    self.Q[i, t + 1] = (self.Q[i, t] + self.Dt / self.dx * alpham * self.Q[
                        i - 1, t + 1] - betam * self.Dt) / (1.0 + alpham * self.Dt / self.dx)
                    self.A[i, t + 1] = self.A[i, t] - self.Dt / self.dx * (self.Q[i, t + 1] - self.Q[i - 1, t + 1])
                    self.h[i, t + 1] = self.A[i, t + 1] / self.B

                    self.R = self.A[i, t + 1] / (self.A[i, t + 1] / self.B * 2.0 + self.B)

            fig.suptitle(f'Time = {self.T[t]/3600} (h)')
            axs[0].cla()
            axs[1].cla()
            axs[0].plot(self.x[:], self.h[:, t])
            axs[0].set(xlabel='x [m]', ylabel='h [m]')
            axs[1].plot(self.x[:], self.Q[:, t])
            axs[1].set(xlabel='x [m]', ylabel='Q [m^3\s]')

            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.1)

if __name__ == "__main__":
    flood_simulation = MainApplication()
    flood_simulation.calculateVariables()
    flood_simulation.update_plot_data()
