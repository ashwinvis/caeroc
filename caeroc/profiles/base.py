# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:52:11 2015

@author: ashwin
"""
import pylab as pl
import numpy as np

class ProfilesBase:
    def __init__(self, N, length, bodytype=None):
        self.N = N
        self.L = length
        if bodytype is 'airfoil':
            self.X, self.Y, self.angle = self.airfoil()
        else:
            self.X, self.Y, self.angle = self.circle()
        pl.plot(self.X, self.Y)
        pl.axis([-length,length,-length,length])
        self._non_dimensionalize(length)

    def _non_dimensionalize(self, scale):
        """Non dimensionalize all geometric parameters with the scale"""
        self.L = self.L/scale
        self.X = self.X/scale
        self.Y = self.Y/scale

class Nozzle(ProfilesBase):
    def nozzle(self):
        """Converging/Diverging Nozzle"""
        pass

    def lavalnozzle(self):
        """Conv. and Div. Nozzle"""
        pass

class Airfoil(ProfilesBase):
    def airfoil(self):
        """Biconvex airfoil"""
        L = self.L
        N = self.N
        R = 210
        theta_arc = np.arcsin(L/2 / R) * 2
        pi = np.pi
        theta_up = np.linspace((pi+theta_arc) / 2,
                               +(pi-theta_arc) / 2, N)
        #theta_up = theta[::-1]
        theta_down =np.linspace((3*pi-theta_arc) / 2,
                               +(3*pi+theta_arc) / 2, N)
        
        X_up = R * np.cos(theta_up)
        Y_up = R * np.sin(theta_up)
        X_down = R * np.cos(theta_down)
        Y_down = R * np.sin(theta_down)
        
        shift_r = X_up[0]
        X_up -= shift_r
        X_down -= shift_r
        shift_up = Y_up[0]
        shift_down = Y_down[0]
        Y_up = Y_up - shift_up
        Y_down = Y_down - shift_down
        
        X = np.concatenate((X_up, X_down))
        Y = np.concatenate((Y_up, Y_down))
        slope_up = np.gradient(Y_up,1)/np.gradient(X_up,1)
        slope_down = np.gradient(Y_down,1)/np.gradient(X_down,1)
        angle = np.arctan(np.concatenate((slope_up, slope_down)))
        return X, Y, angle

    def circle(self):
        theta = np.linspace(0, 2*np.pi, self.N)
        R = self.L / 2
        X = R * np.cos(theta)
        Y = R * np.sin(theta)
        angle = (theta - np.pi / 2)
        return X, Y, angle

class Duct(ProfilesBase):
    def duct(self):
        """Constant area duct/pipe for Fanno & Rayleigh flows"""
        pass

