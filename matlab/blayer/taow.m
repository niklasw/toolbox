clear
Re=input('input Re= : ');
%u=input('input [u0 u1 u2]: ');
%h=input('input mean grid size: ');
%nu=input('input nu: ');
u=input('input u2: ');
h=input('input grid size: ');
nu=1.14e-6;
nu=1/Re;
%dudx=(-3*u(1)+4*u(2)-u(3))/(2*h);
%rho=1000;
%taow=nu*rho*dudx
%utao=sqrt(taow/rho)
%yplus=(h*utao/nu)
yplus=sqrt(h*u/nu)
