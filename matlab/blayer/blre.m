#!/usr/bin/octave
re=input('Re-number: ');
rho=input('Density: ');
x=input('x-stations vector: ');

u0=1;
nu=1/re;
rex=re*x;
d_bl=.37*x./(rex).^.2
tao_w=.03*rho*u0^2./(rex).^.2
Cf=.0576*rex.^(-.2)
u_tao=sqrt(tao_w/rho);
d_sub=478./(rex.^(7.0/10)).*d_bl

y_plus=input('desired y_plus, in vector: ');

y_location=y_plus./(u_tao/nu)
