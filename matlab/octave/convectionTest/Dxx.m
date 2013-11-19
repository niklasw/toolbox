function out=Dxx(u,dx)
%
%    Central difference approx of second derivative (1D)
%    Cyclic boundaries. Uses Dx.m
%

     out = (Dx(u,dx,1)-Dx(u,dx,-1))/dx;

