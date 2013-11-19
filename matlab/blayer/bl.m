#!/usr/bin/octave
u0=input('free stream U0: ');
x=input('length: ');
nu=input('nu: ');
rho=input('rho: ');

rex=u0*x/nu
d_bl=.38*x/(rex)^.2
tao_w=.03*rho*u0^2/(rex)^.2
u_tao=sqrt(tao_w/rho);
d_sub=30*nu/(u_tao)

y_plus=input('desired y_plus, in vector: ');

y_location=y_plus./(u_tao/nu)
