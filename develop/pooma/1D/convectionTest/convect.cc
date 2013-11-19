/*
    Niklas is testing basic things with POOMA
*/

#include "Pooma/Arrays.h"

#include <iostream>

inline Array<1> shift(const Array<1>& phi, int n)
{
    int N = phi.length(0)-1;

    Array<1> tmp(N+1);
    tmp = 0;

    if (n < 0)
    {
         n = n+N;
    }
    Interval<1> I1(n,N);
    Interval<1> I2(0,n-1);
    Interval<1> I3(0,N-n);
    Interval<1> I4(N-n+1,N);

    tmp(I1) = phi(I3);
    tmp(I2) = phi(I4);

    return tmp;
}

inline Array<1> Dx(const Array<1>& phi, const float dx,int d)
{
    int N = phi.length(0)-1;
    float w = 1.0/dx;
    Array<1> tmp(N+1);
    if (d == 0)
    {
         tmp = (shift(phi,1)-shift(phi,-1))*0.5*w;
         tmp(N) = (phi(1)-phi(N-1))*0.5*w;
         tmp(0) = tmp(N);
    }
    if (d == 1)
    {
         tmp = (shift(phi,1)-shift(phi,0))*w;
         tmp(0) = tmp(N);
    }
    if (d == -1)
    {
         tmp = (shift(phi,0)-shift(phi,-1))*w;
         tmp(N) = tmp(0);
    }
    return tmp;
}

inline Array<1> Dxx(const Array<1>& phi, const float dx)
{
    int N = phi.length(0)-1;
    Array<1> tmp(N+1);
    tmp = (Dx(phi,dx,1)-Dx(phi,dx,-1))/dx;
    return tmp;
}

inline Array<1> Dxx(const Array<1>& phi, const float dx,int d)
{
    int N = phi.length(0);
    float w = 1.0/dx;
    Array<1> tmp(N);
    tmp = Dx(phi,dx,1)-Dx(phi,dx,-1)*w;
    return tmp;
}

inline Array<1> heaviside(const Array<1>& phi)
{
    int N = phi.length(0);
    Array<1> tmp(N);
    tmp = 0;
    for (int i=0; i<N-1; ++i){
        if ( phi(i) > 0 ) tmp(i) = 1;
    }
    return tmp;
}

inline Array<1> minmod(const Array<1>& a, const Array<1>& b)
{
    std::cout << "NOT IMPLEMENTED" << std::endl;
    return a;
}


inline Array<1> rhs(const Array<1>& phi, const float& dx)
{
    int N = phi.length(0);
    Array<1> tmp(N);
    tmp = - Dx(phi,dx,0);
    return tmp;
}


int
main( int argc, char* argv[])
{
    const int size=40;
    const float x0 = -1;
    const float x1 = 1;
    const float dx = (x1-x0)/size;
    const float dt = 0.01;
    const float t0=0, t1=4;


    Pooma::initialize(argc,argv);

    Array<1> D(size), Dold(size), U(size), S(size), X(size);
    X = dx * iota(size).comp(0);
    const int N = size;
    float f = 3.14159265;
    D = cos(f*X);
    U = f*sin(f*X);
    Dold = D;

    //std::cout << "starting Runge Kutta loop" << std::endl;
    std::cout << X << std::endl;
    std::cout << D << std::endl;
    std::cout << Dx(D,dx,-1) << std::endl;
    std::cout << U << std::endl;
    //std::cout << Dx(D,dx,-1) << std::endl;
    std::cout << -Dxx(D,dx)/f/f << std::endl;


    for (float t=t0; t<=t1; t+=dt)
    {
/*
        D = Dold + dt*rhs(D,dx);
        Dold=D;
*/
        Array<1> D0 = rhs(D,dx);
        Array<1> d1(N);
        d1 = D+dt/2*rhs(D,dx);
        Array<1> d2(N);
        d2 = D+dt/2*rhs(d1,dx);
        Array<1> D1(N);
        D1 = D+dt*rhs(d2,dx);
        D = D + dt/6*(D0+2*d1+2*d2+D1);
    };

    //std::cout << D << std::endl;

    Pooma::finalize();
    return 0;
}
