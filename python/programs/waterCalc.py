#!/usr/bin/python
import sys
mass = float(sys.argv[1])
deltaT = float(sys.argv[2])

CpH20=4181.3 #J/kgK

E = CpH20*deltaT*mass

kWh = E / (3600*1000)

print "\n%4d kg water at deltaT = %2d\n" % (mass,deltaT)
print "kJ    = %4.1e" % E
print "kWh   = %4.2e\n" % kWh
