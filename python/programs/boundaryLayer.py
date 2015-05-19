#!/usr/bin/python

import interactor2
from math import sqrt

def calcBL():
    i = interactor2.interactor()

    u0  = i.get("\tfar field velocity", test=float, default=1.0)
    x   = i.get("\tflat plate length", test=float, default=1.0)
    nu  = i.get("\tkinematic viscosity", test=float,default=15e-6)
    rho = i.get("\tfluid density", test=float, default=1.2)
    y_p = i.get("\tdesired y_plus", test=float,default=50)

    rex  = u0*x/nu
    d_bl  = .38*x/(rex)**.2
    tau_w = .03*rho*u0**2/(rex)**.2
    u_tau = sqrt(tau_w/rho)
    d_sub = 30*nu/(u_tau)

    print ''
    print '{0:8s} = {1:0.3e}'.format('Re_x', rex)
    print '{0:8s} = {1:0.3e}'.format('d_bl', d_bl)
    print '{0:8s} = {1:0.3e}'.format('d_sub', d_sub)




if __name__ == "__main__":
    calcBL()


