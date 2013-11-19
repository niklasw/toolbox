clear
Re=input('input Re= : ');
x0=input('input X0= : ');
L=input('domain length= : ');
dx=L/84;
x=[x0:dx:x0+L];
Rex=Re*x;

cf=.027./Rex.^(1/7);
d_bl=.37*x./(Rex).^.2;

x=[0:dx:L];

xCf(:,1)=x';
xCf(:,2)=cf';
dBl(:,1)=x';
dBl(:,2)=d_bl';
save cfx.mat xCf
save dbl.mat dBl
