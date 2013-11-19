#!/usr/bin/env python

import sys,os,re,math
import interactor2

def usage():
    print """
        Program to help approximate turbulet inlet conditons.
        It is interactive and will ask about far field velocity,
        and assumed turbulent length scale. 

                      k^2                   3
            nut = Cmu*--- ,             k=  - (ti*U_inf)^2
                      eps                   2 
       
                           k^(3/2)                   k^(3/2)
            lt  = Cmu^0.75*-------,  eps = Cmu^0.75 *------
                             eps                        lt
       
                     k     eps                k^(1/2)
            omega = --- = ----- = Cmu^(-1/4)* -------
                    nut   Cmu*k                 lt

                           3                     k
            nuTilda = sqrt(-)(U_inf*ti*lt) = ------------
                           2                 omega*Cmu^1/4

        If a negative number is supplied (nothing is entered) the
        value will not be used in any calculation and the assumption
        is made that other data will be enough to give a result...

                                            /Niklas
    """


def turbulenceProperties():
    usage()
    def Info(t):
        print "\n\t%30s = %4e" % t

    i = interactor2.interactor()

    U = i.get("\tfar field velocity, U_inf",test=float,default=1.0)
    ti= i.get("\tturbulent intensity, ti (%)",test=float,default=-1)
    lt= i.get("\tturbulent length scale, lt",test=float,default=-1)
    nut= i.get("\tturbulent viscosity, nut",test=float,default=-1 )
    eps= i.get("\tturbulent dissipation rate, eps",test=float,default=-1 )
    
    Cmu=0.09
    tke=-1.0

    if ti >=0:
        tke = 3.0/2*(ti/100.0*U)**2.0
        Info(("turbulent kinetic energy",tke))
        if lt >= 0:
            eps = Cmu**(3.0/4)*tke**(3.0/2)/lt
            nut = Cmu*tke**(2.0)/eps
            omega = tke/nut
            nuTilda = (3.0/2)**0.5*(U*ti*lt)
            Info(("epsilon", eps))
            Info(("turbulent viscosity",nut))
            Info(("omega",omega))
            Info(("nuTilda",nuTilda))
            Info(("turbulent viscosity",nut))
        elif nut > 0:
            eps = Cmu*tke**(2.0)/nut
            lt = Cmu*tke**(3.0/2)/eps
            omega = eps/(Cmu*tke)
            Info(("turbulent length scale",lt))
            Info(("epsilon",eps))
            Info(("omega",omega))
        elif eps > 0:
            lt = Cmu*tke**(3.0/2)/eps
            nut = Cmu*tke**(2.0)/eps
            omega = tke/nut
            Info(("turbulent length scale",lt))
            Info(("turbulent viscosity",nut))
            Info(("omega",omega))
        else:
            print "\n\t!NOT ENOUGH INPUT!"
    else:
        if lt>=0 and nut>=0:
            tke=Cmu**0.25*(nut/lt)**2
            eps=Cmu**0.75*tke**(3.0/2)/lt
            omega=tke/nut
            ti=100*math.sqrt(2.0/3*tke)/U

            Info(("turbulent length scale",lt))
            Info(("turbulent viscosity",nut))
            Info(("turbulent kinetic energy",tke))
            Info(("turbulent intensity (%)",ti))
            Info(("epsilon",eps))
            Info(("omega",omega))
        else:
            print "\n\t!NOT ENOUGH INPUT!"

    print "\nEnd.\n"
        

if __name__=="__main__":
    turbulenceProperties()

