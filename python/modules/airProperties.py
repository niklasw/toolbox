#!/usr/bin/env python

class AirProperties:
    gamma = 7./5    # Adiabatic index)
    M = 0.0289645   # kg/mol

    def __init__(self,T=293.15,p=1e5,R=287.05):
        self.R=R
        self.T=T
        self.p=p

    def thermalDiffusivity(self):
        return 9.1018E-11*self.T**2 + 8.8197E-08*self.T - 1.0654E-05

    def kinematicViscosity(self):
        return -1.1555E-14*self.T**3 + 9.5728E-11*self.T**2 + 3.7604E-08*self.T - 3.4484E-06

    def dynamicViscosity(self):
        return self.kinematicViscosity()*self.densityIdealGasLaw()

    def SutherlandDynamicViscosity(self):
        mu_0 = 18.27e-6
        T_0  = 291.15
        C = 120
        return mu_0*(T_0+C)/(self.T+C)*(self.T/T_0)**(3.0/2)

    def thermalConductivity(self):
        return 1.5207E-11*self.T**3 - 4.8574E-08*self.T**2 + 1.0184E-04*self.T - 3.9333E-04

    def densityIdealGasLaw(self):
        p0=1.0e5
        R=287.05
        return p0/R/self.T

    def densityPolynomial(self):
        return 360.77819*self.T**(-1.00336)

    def specificHeat(self):
        return 1.9327E-10*self.T**4 - 7.9999E-07*self.T**3 + 1.1407E-03*self.T**2 - 4.4890E-01*self.T + 1.0575E+03

    def speedOfSound(self):
        import math
        return math.sqrt(self.gamma*self.R*self.T)

    def __str__(self):

        p = 'T = %f\n\n'% self.T
        p +=  "\t%30s: %2.3e\n" % (self.thermalDiffusivity.__name__,self.thermalDiffusivity())
        p +=  "\t%30s: %2.3e\n" % (self.kinematicViscosity.__name__,self.kinematicViscosity())
        p +=  "\t%30s: %2.3e\n" % (self.dynamicViscosity.__name__,self.dynamicViscosity())
        p +=  "\t%30s: %2.3e\n" % (self.SutherlandDynamicViscosity.__name__,self.SutherlandDynamicViscosity())
        p +=  "\t%30s: %2.3e\n" % (self.thermalConductivity.__name__,self.thermalConductivity())
        p +=  "\t%30s: %2.3e\n" % (self.densityIdealGasLaw.__name__,self.densityIdealGasLaw())
        p +=  "\t%30s: %2.3e\n" % (self.densityPolynomial.__name__,self.densityPolynomial())
        p +=  "\t%30s: %2.3e\n" % (self.specificHeat.__name__,self.specificHeat())
        p +=  "\t%30s: %2.3e\n" % (self.speedOfSound.__name__,self.speedOfSound())
        return p

if __name__=='__main__':
    import sys
    temperatures = sys.argv[1:]
    tList=[]
    for s in temperatures:
        try:
            tList.append(float(s))
        except:
            print "\nCould not read input: ",s

    for t in tList:
        air = AirProperties(T=t)
        print air
