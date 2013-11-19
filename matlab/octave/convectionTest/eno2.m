function out = eno2(u,dx)

     N=length(u);
     bd =  Dx(u,dx,-1);
     dxx = Dxx(u,dx);
     mask = heaviside(abs(Shift(dxx,-1))-abs(Shift(dxx,0)),0);
     dxx = (1-mask).*Shift(dxx,-1)+mask.*Shift(dxx,0);

     out = bd+dxx*dx/2;
     %out(N)=out(1);
