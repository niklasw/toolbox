#!/usr/bin/python

import interactor2
from math import sqrt

i = interactor2.interactor()
u0 = i.get('\tFree stream velocity magnitude',test=float,default=1.0)
x  = i.get('\tlength',test=float,default=1)
nu = i.get('\tKinematic viscosity, nu',test=float,default=1e-6)
rho= i.get('\tDensity', test=float, default=1000)

rex=u0*x/nu
d_bl=.38*x/(rex)**0.2 # 99% of free stream velocity
tao_w=.03*rho*u0**2/(rex)**0.2
u_tao=sqrt(tao_w/rho)
d_sub=30*nu/(u_tao)

y_plus = i.get('\tDesired y+',test=float, default=1)

firstCell = y_plus*nu/u_tao

print ''

i.info('Re_x = {0:2.3e}'.format(rex))
i.info('BL thickness = {0}'.format(d_bl))
i.info('First cell height for y+ = {1} is {0}'.format(firstCell, y_plus))
