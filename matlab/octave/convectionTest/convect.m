%
% Convection test of a sine function
%
% nikwik, magber and matlie
%

clear all;

N=128;
t0=0;
t1=input("Enter end Time: ")
scheme=input("Enter spatial scheme:\n 1: upwind\n 2: central\n 3: eno O(2)\n 4: blended\n 5: corrected upwind\n");
dt=0.002;

X = linspace(-1,1,N);
dx= 2/(N-1);
u0= cos(pi*X);
u0 = heaviside(u0,0);
u0(N) = u0(1);

visc = 1;

T=dt;
u = u0
uOld = u0;
uOldOld = uOld;

axis([-1,1,-1,1.2])
while (T<=t1)
    if scheme == 1
        ux = Dx(uOld,dx,-1);
    elseif scheme == 2
        ux = Dx(uOld,dx,0);
    elseif scheme == 4
        ux = 0.5*Dx(uOld,dx,0) + 0.5*Dx(uOld,dx,-1);
    elseif scheme == 5
        ux = Dx(uOld,dx,-1)+Shift(Dxx(uOld,dx),-1)*dx/2;
    elseif scheme == 3
        ux = eno2(uOld,dx);
    else
        ok=input("Unknown selection");
        exit
    end

    u=uOld - dt*( ux );

    uOldOld = uOld;
    uOld = u;

    T=T+dt;
plot(X,u,'-@x',X,u0)
end
plot(X,u,'-@x',X,u0)



