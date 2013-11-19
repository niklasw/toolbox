clear all
ms=[0 4 15 41 88 160 245]*1e-3;
phi=[0 5 10 15 20 25 30]*pi/180;
gm=2.0;
m1=1000;
h=5*pi/180;
gz=gm*sin(phi)+ms;

e(1)=0;
e(2)=h*(ms(1)+ms(2))/2;
e(3)=h/3*dot([1 4 1],ms(1:3));
e(4)=e(3)+h*(ms(3)+ms(4))/2;
e(5)=h/3*dot([1 4 2 4 1],ms(1:5));
e(6)=e(5)+h*(ms(5)+ms(6))/2;
e(7)=h/3*dot([1 4 2 4 2 4 1],ms);

depl=1350;

e=e+gm*(1-cos(phi));

cmp=...
[depl*(e(7)-e(3)),m1*(phi(7)-phi(3));...
 depl*(e(6)-e(3)),m1*(phi(6)-phi(3));...
 depl*(e(5)-e(3)),m1*(phi(5)-phi(3));...
 depl*(e(4)-e(3)),m1*(phi(4)-phi(3));...
 depl*(e(3)-e(3)),m1*(phi(3)-phi(3))]


mr=depl*gz