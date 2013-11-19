function out = Dx(u,dx,d)
%
%    Central, backward or forward difference approximation (1D).
%    Cyclic boundaries.
%    Third argument 0,-1 or 1 -> CD, BD, FD
%
     N=length(u);
     if d == 0
%    central difference
          ux = (Shift(u,1)-Shift(u,-1))/(2*dx);
          ux(N)=(u(2)-u(N-1))/(2*dx);
          ux(1)=ux(N);

     elseif d == -1
%    backward difference
          ux = (Shift(u,0)-Shift(u,d))/dx;
          ux(1) = ux(N);

     else
%    forward difference
          ux = (Shift(u,d)-Shift(u,0))/dx;
          ux(N) = ux(1);

     end

     out = ux;
