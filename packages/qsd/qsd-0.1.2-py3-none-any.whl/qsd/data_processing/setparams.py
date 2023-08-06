#!/usr/bin/env python
"""
This program sets the parameters required for simulation. 
"""

import numpy as np
import os
from subprocess import call

class SetParams:
    """
        This class allows a user to set the relevant parameters of the cpw. This needs refactorinng, but is sufficient for now. 
    """
    def __init__(self):
        """
            Initialize with parameters
            
            :type w: float
            :param w: width of substrate

            :type t: float
            :param t: thickness of superconductor

            :type l: float
            :param l: length of supercondducting wire

            :type pen: float
            :param pen: penetration depth

            :type omega: float
            :param omega: cavity resonant frequency

            :type Z: float
            :param w: characteristic impedance
        """
        self.w = None
        self.t = None
        self.l = None
        self.pen = None
        self.omega = None
        self.Z = None
        self.N = 2

    def set_params(self,infile):
        """
            Returns simulation parameters as a dictionary
        """
        # Define geometry of the superconductor
        paramfile=open(infile,"r")
        filestring = paramfile.read()
        filelist = filestring.split("\n")

        pd = {}
        for fl in filelist:
            l = fl.split()
            pd[l[0]] = l[2]
        paramfile.close()

        self.w = float(pd["w"])
        self.t = float(pd["t"])
        self.l = float(pd["l"])
        self.pen = float(pd["pen"])
        self.omega = float(pd["omega"])
        self.Z = float(pd["Z"])
        
        params = {'w':self.w,
            't':self.t,
            'l':self.l,
            'pen':self.pen,
            'omega':self.omega,
            'Z':self.Z
        }
        return params

    def param_list(self,x,I,Jnorm,paramfile):
        """
        Generates a text file which holds the parameters requiured for the COMSOL simulation
        """
        n = [abs(i) for i in x]
        idx = n.index(min(n))

        I0 = I[idx]
        J0 = I0/(2*(self.w+self.t)*self.pen)
        pen_perp = self.pen**2 / (2*self.t)
        C = (0.506*np.sqrt(self.w/(2*pen_perp)))**0.75
        l1 = self.pen*np.sqrt(2*self.pen/pen_perp)
        l2 = 0.774*self.pen**2/pen_perp + 0.5152*pen_perp
        J2overJ1 = (1.008/np.cosh(self.t/self.pen)*np.sqrt(self.w/pen_perp/
            (4*pen_perp/self.pen - 0.08301*self.pen/pen_perp)))
        J1 = Jnorm[idx]
        w_sub = 4*self.w
        h_sub = 25e-06

        f = open(paramfile,'w')
        f.write('w ' + str(self.w) + '[m] width_of_superconductor\n'
           't ' + str(self.t) + '[m] thickness_of_superconductor\n'
           'pen ' + str(self.pen) + '[m] penetration_depth\n'
           'I0 ' + str(I0) + '[A/m] current_at_x=0\n'
           'J0 ' + str(J0) + '[A/m^3] current_density_at_x=0\n'
           'N ' + str(self.N) + '\n'
           'w_sub ' + str(w_sub) + '[m] substrate_width\n'
           'h_sub ' + str(h_sub) + '[m] substrate_height\n'
           'pen_perp ' + str(pen_perp) + '[m] perpendicular_pen_depth\n'
           'C ' + str(C) + ' capacitance\n'
           'l1 ' + str(l1) + '[m]\n'
           'l2 ' + str(l2) + '[m]\n'
           'J2overJ1 ' + str(J2overJ1) + '\n'
           'J1 ' + str(J1) + '[A/m]'
           )

        f.close()


