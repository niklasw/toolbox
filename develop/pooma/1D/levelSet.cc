/*
    Niklas is testing basic things with POOMA
*/

#include "Pooma/Arrays.h"

#include <iostream>

const int N=201;
const float dx = 0.1;
const float dt = 0.01;
const float t0=0, t1=1;

Interval<1> I(1, N-2);

inline Array<1> sign(const Array<1>& phi)
{
    int L = phi.length(0);
    Array<1> tmp(L);
    tmp = 0;
    for (int i=0; i<L-1; ++i){
        if ( phi(i) > 0 ) tmp(i) = 1;
    }
    return tmp;
}

inline Array<1> d1_c2(const Array<1>& phi, const float& dx)
{
    int L = phi.length(0);
    Interval<1> J(1,L-2);
    Array<1> tmp(L);
    tmp(J) = (phi(J+1)-phi(J-1))/dx;
    return tmp;
}
inline Array<1> d1_b1(const Array<1>& phi, const float& dx)
{
    int L = phi.length(0);
    Interval<1> J(1,L-2);
    Array<1> tmp(L);
    tmp(J) = (phi(J)-phi(J-1))/dx;
    return tmp;
}
inline Array<1> d1_f1(const Array<1>& phi, const float& dx)
{
    int L = phi.length(0);
    Interval<1> J(1,L-2);
    Array<1> tmp(L);
    tmp(J) = (phi(J+1)-phi(J))/dx;
    return tmp;
}
inline Array<1> d1_b2(const Array<1>& phi, const float& dx)
{
    int L = phi.length(0);
    Interval<1> J(2,L-3);
    Array<1> tmp(L);
    tmp(J) = (3*phi(J)-4*phi(J-1)+phi(J-2))/(2*dx);
    return tmp;
}
inline Array<1> d1_f2(const Array<1>& phi, const float& dx)
{
    int L = phi.length(0);
    Interval<1> J(2,L-3);
    Array<1> tmp(L);
    tmp(J) = (-3*phi(J)+4*phi(J+1)-phi(J+2))/(2*dx);
    return tmp;
}
inline Array<1> d1_uw1
(
    const Array<1>& phi,
    const float& dx,
    const Array<1>& flux
)
{
    int L = phi.length(0);
    Interval<1> J(1,L-2);
    Array<1> tmp(L);
    tmp(J) = 0.5*(sign(flux)-1)*d1_b1(phi,dx)
        + 0.5*(sign(flux)+1)*d1_f1(phi,dx);
    return phi;
}
inline Array<1> d2_c2(const Array<1>& phi, const float& dx)
{
    int L = phi.length(0);
    Interval<1> J(2,L-3);
    Array<1> tmp(L);
    tmp(J) = (phi(J-1)-2*phi(J)+phi(J+1))/(dx*dx);
    return tmp;
}

inline Array<1> minmod(const Array<1>& a, const Array<1>& b)
{
    std::cout << "NOT IMPLEMENTED" << std::endl;
    return a;
}

// Eval the RHS
inline Array<1> flux(const Array<1>& phi, const float& dx)
{
    int L = phi.length(0);
    Interval<1> J(1,L-2);
    Array<1> tmp(L);
    tmp = sign(phi)*d1_c2(phi,dx)/abs(d1_c2(phi,dx));
    return tmp;
}

inline Array<1> rhs(const Array<1>& phi, const float& dx)
{
    int L = phi.length(0);
    Interval<1> J(1,L-2);
    Array<1> tmp(L);
    tmp(J) = sign(phi)*( 1 - abs(d1_uw1(phi,dx,flux(phi,dx))));
    return tmp;
}

int
main( int argc, char* argv[])
{
    Pooma::initialize(argc,argv);

    Array<1> D(N), U(N), S(N), X(N);
    X = dx * iota(N).comp(0);
    float f = 1.0;
    D = sin(f*X);

    // Runge-Kutta 4: time loop

    for (float t=t0; t<=t1; t+=dt){
        //        std::cout << "time = " << t << std::endl;
        Array<1> tmp(N);
        Array<1> k1 = rhs(D,dx);
        tmp = D+dt/2*k1;
        Array<1> k2 = rhs(tmp, dx);
        tmp = D+dt/2*k2;
        Array<1> k3 = rhs(tmp, dx);
        tmp = D+dt*k2;
        Array<1> k4 = rhs(tmp, dx);
        D = D + dt/6*(k1+2*k2+2*k3+k4);
    };

    std::cout << D << std::endl;
    std::cout << flux(D,dx) << std::endl;

    Pooma::finalize();
    return 0;
}
