#!/usr/bin/python

from pylab import *

def interactor(astring,f,default=""):
    prompt="Input > %s [%s] (q to quit)" % (astring, default)
    sys.stdout.write(prompt+": ")
    out = sys.stdin.readline().strip()
    if out=="":
        out=default
    if out == 'q' or out == 'Q':
        sys.exit(0)

    try:
        checked=f(out)
    except:
        sys.stdout.write("\nType error:")
        checked=interactor(astring,f,default)
    return checked


M = 44.04e-3        # Molar mass (kg/mole)
A =  1e-6           # Discharge Area
T = 273.15+118      # Inside Temp.
P = 23e5            # Inside Pressure
k = 1.4             # cp/cv
R = 8.3145          # Universal gas constant Nm/moleK
C = 1.0             # Discharge coeff.

M = interactor("\tmolar mass",float,M)
A = interactor("\tdischarge area",float,A)
T = interactor("\tinside temp",float,T)
P = interactor("\tinside pressure",float,P)
k = interactor("\tcp/cv",float,k)
C = interactor("\tdischarge coeff.",float,C)


Z = 1.0             # Compressibility factor


P_atm = 1.013e5
T_atm = 273.15+30


massFlux = C*A*P*sqrt( (k*M/(Z*R*T)) * (2.0/(k+1))**((k+1)/(k-1)) )
rho_in = P*M/(R*T)
rho_atm = P_atm*M/(R*T_atm)

print ''
print 'Inside density = %.2e kg/m3' % rho_in
print 'NTP density = %.2e kg/m3' % rho_atm
print 'massFlux = %.2e kg/s' % massFlux
print 'Outside density = %.2e kg/m3' % rho_atm
print 'Volume flow outside = %.2e m3' % (massFlux/rho_atm)
print ''

