import sys
import numpy as np


def notImplemented(s):
    print('Not implemented for this material:', s)
    sys.exit(1)

def Info(s):
    print(('-->{}\n'.format(s)))

def Error(s):
    Info(s)
    Info('EXITING')
    sys.exit(1)



class PropertyTable(object):
    dataTableHeader = 'A b'
    dataTable = '''
    0 10
    1 11
    2 12
    '''

    def __init__(self, order, useKelvin):
        import numpy as np
        self.polynomeOrder = order
        self.headerNames = self.dataTableHeader.split()
        rawData = np.fromstring(self.dataTable, sep = ' ')
        nCols = len(self.headerNames)
        nRows = int(len(rawData)/nCols)
        self.properties = np.reshape(rawData, (nRows, nCols)).transpose()
        self.useKelvin = useKelvin

        self.propertyName = ''
        self.variableName = ''
        self.X = []
        self.Y = []
        self.polynome = []
        self.coeffs = []

    def mkPolynomial(self):
        self.coeffs = np.polyfit(self.X, self.Y, self.polynomeOrder)
        def polyValue(t):
            value = 0
            for i, c in enumerate(self.coeffs[::-1]):
                value += t**i*c
            return value
        self.polynome = polyValue

    def printPolynomeAsString(self,varName=''):
        if not varName:
            varName = self.variableName
        string = ''
        for i, c in enumerate(self.coeffs[::-1]):
            string+='+({0}*{2}**{1})'.format(c, i, varName)
        print('\n{} = f({})'.format(self.propertyName, varName))
        print('{}\n'.format(string))

    def getPropertyColumn(self, s):
        if not s in self.headerNames:
            Error('Cannot read property {} from table'.format(s))
        column = self.headerNames.index(s)
        return self.properties[column]

    def selectProperty(self,propertyName,variableName = 'T'):
        self.propertyName = propertyName
        self.variableName = variableName
        shift = 273.15 if self.useKelvin else 0
        self.X = self.getPropertyColumn(variableName) + shift
        self.Y = self.getPropertyColumn(propertyName)
        self.mkPolynomial()

    def showProperty(self):
        T = np.linspace(0,200,1000)
        if self.useKelvin:
            T += 273.15
        plt.plot(self.X, self.Y,'o',label=self.propertyName)
        plt.plot(T,self.polynome(T),label=self.propertyName)
        plt.legend()
        plt.grid('on')
        plt.show()

    def getPropertyValue(self, property_name,  x):
        self.selectProperty(property_name)
        if x < np.min(self.X) or x > np.max(self.X):
            Error('Data out of table bounds. (value = {})'.format(x))
        return self.polynome(x)


class WaterTable(PropertyTable):
    '''
    Table values from http://www.engineeringtoolbox.com
    With units as follows:
    T [C] Temperature
    h [kJ/kg] specific enthalpy
    nu 1e-6*[m2/s] kinematic viscosity
    Pr Prandtl number
    pabs [kN/m2] Absolute pressure
    rho [kg/m3] density
    Cp [kJ/(kg K)] Specific heat capacity
    s [kJ/(kg K)] Specific entropy
    kappa [W/m K] Thermal conductivity (incomplete values)
    beta        Thermal expansion coefficient (inclomplete values)
    '''

    dataTableHeader = 'T nu h Pr pabs rho Cp s kappa beta'
    dataTable='''
        0.01  1.792  0      13.67  0.6     999.8  4.217  0          .55575  0.000010
        10    1.304  41.9   9.47   1.2     999.8  4.192  0.15       .57864  0.000088
        20    1.004  83.8   7.01   2.3     998.3  4.182  0.296      .59803  0.000207
        30    0.801  125.7  5.43   4.3     995.7  4.178  0.438      .61450  0.000303
        40    0.658  167.6  4.34   7.7     992.3  4.179  0.581      .62856  0.000385
        50    0.553  209.6  3.56   12.5    988    4.182  0.707      .64060  0.000457
        60    0.474  251.5  2.99   20      983    4.185  0.832      .65091  0.000522
        70    0.413  293.4  2.56   31.3    978    4.191  0.966      .65969  0.000582
        80    0.365  335.3  2.23   47.5    972    4.198  1.076      .66702  0.000640
        90    0.326  377.2  1.96   70      965    4.208  1.192      .67288  0.000695
        100   0.295  419.1  1.75   101.33  958    4.219  1.307      0       0
        120   0.249  503.7  1.45   199     943    4.248  1.527      0       0
        140   0.215  588.7  1.25   361     926    4.29   1.739      0       0
        160   0.189  674.5  1.09   618     907    4.35   1.942      0       0
        180   0.17   763.1  0.98   1000    887    4.42   2.138      0       0
        200   0.158  851.7  0.92   1550    864    4.51   2.329      0       0
    '''

    def __init__(self):
        super().__init__(8, True)


class FluidProperties:
    R = 8.3144621

    def __init__(self, T=293.15, p=101325):
        self.T=T
        self.p=p

    def thermalDiffusivity(self):
        notImplemented('thermalDiffusivity')

    def kinematicViscosity(self):
        notImplemented('kinematicViscosity')

    def thermalConductivity(self):
        notImplemented('thermalConductivity')

    def density(self):
        notImplemented('density')

    def specificHeat(self):
        notImplemented('specificHeat')

    # Derived properties
    def dynamicViscosity(self):
        return self.kinematicViscosity() * self.density()

    def thermalDiffusivity(self):
        return self.thermalConductivity()/(self.density() * self.specificHeat())


class WaterProperties(FluidProperties, WaterTable):
    gamma = 1           # heat capacity ratio, not used for liquids
    M = 18.01528e-3     # kg/mol

    def __init__(self, T=293.15, p=101325):
        FluidProperties.__init__(self, T, p)
        WaterTable.__init__(self)

    def density(self):
        return self.getPropertyValue('rho', self.T)

    def kinematicViscosity(self):
        return self.getPropertyValue('nu', self.T) * 1e-6

    def specificHeat(self):
        return self.getPropertyValue('Cp', self.T) * 1e3

    def thermalConductivity(self):
        return self.getPropertyValue('kappa', self.T)

    def thermalExpansionCoefficient(self):
        return self.getPropertyValue('beta', self.T)


if __name__ == '__main__':
    
    try:
        T0 = float(sys.argv[1])
    except ValueError as e:
        # print (e)
        T0 = 293.15

    water = WaterProperties(T=T0)
    print('rho   ',water.density())
    print('nu    ', water.kinematicViscosity())
    print('mu    ', water.dynamicViscosity())
    print('Cp    ', water.specificHeat())
    print('kappa ', water.thermalConductivity())
    print('alpha ', water.thermalDiffusivity())
    print('beta  ', water.thermalExpansionCoefficient())

