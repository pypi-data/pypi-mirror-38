#!/usr/bin/env python

""" This program wil calculate the electromagnetic properties of cpw resonators
"""

import numpy as np
import csv
from scipy import constants as sp

class CPW:
    """
    CPW contains the methods for calculating electromagntic properties of cpw resonator
    """
    version = '0.1'

    def __init__(self,x,l,w,t,pen,Z,omega):
        """
        Initializes the cpw geometry, penetration depth, Z, resonant frequency, and voltage

        :type x: float
        :param x: width of substrate

        :type l: int
        :param l: length of superconductor

        :type w: int
        :param w: width of superconductor

        :type t: int
        :param t: thickness of superconductor

        :type pen: int
        :param pen: penetration depth of superconductor

        :type Z: int
        :param Z: characteristic impedance or cpw

        :type omega: int
        :param omega: resonant frequency

        :type V: int
        :param l: voltage

        """
        self.x = x
        self.l = l
        self.w = w
        self.t = t
        self.pen = pen
        self.Z = Z
        self.omega = omega
        self.V = 1
    
    def J(self):
        """
        Calculates un-normalized vacuum current density
        """
        ans = []
        for i in self.x:
            if abs(i) > self.w/2.:
                ans.append(0)
            elif abs(i) == self.w/2.:
                ans.append(1.165/self.pen*(self.w*self.t)**.5)
            elif abs(i) < self.w/2. and abs(i) > self.w/2. - self.pen**2/(2*self.t):
                ans.append(1.165/self.pen*(self.w*self.t)**.5*np.exp(-(self.w/2. - abs(i))*self.t/self.pen**2))
            else:
                ans.append((1 - (2*abs(i)/self.w)**2)**-.5)
        return np.asarray(ans)
    
    def normalize_J(self):
        """
        Normalizes vacuum current density
        """
        #normalise 
        Js = self.J()
        dI = self.omega*(sp.hbar/(2*self.Z))**.5
        dx = self.x[1] - self.x[0]
        Jnorm = dI*Js/(self.t*dx*np.sum(Js))
        return Jnorm
    
    def current(self,*args,**kwargs):
        """ 
        Calculates critical current
        """
        norm = kwargs.get('norm','yes')

        if norm=='yes':
            I = self.l * self.normalize_J()
        else:
            I = self.l * self.J()
        return I
    
    def resistance(self):
        """
        calculates resistance of superconductor
        """
        R = self.V / self.current()
        return R
    
    def resistivity(self):
        """
        Calculates resistivity of superconductor
        """
        A = self. w * self.t # Cross-sectional area of cpw
        rho = self.resistance() * (A / self.l)
        return rho
        
    def conductivity(self):
        """
        Calculates conductivity of superconductor
        """
        G = 1/self.resistivity()
        return G
    
    def E(self):
        """
        Calculates electroc field of supercodnuctor
        """
        E = self.normalize_J() * self.conductivity()
        return E
