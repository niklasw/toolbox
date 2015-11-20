import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
#gg = salome.ImportComponentGUI("GEOM")
geompy = geomBuilder.New(salome.myStudy)

from numpy import linspace

#
# Wigley hull eqn:
#   y(x,z) =  B/2*(1-(2*x/L)**2)*(1-(z/T)**2)
#

def buildExpr(B,L,T,x,z):
    s = '{0}/2*(1-(2*{3}/{1})**2)*(1-({4}/{2})**2)'.format(B,L,T,x,z)
    return s

L = 1.0
B = L*0.1
T = L*0.0625
freeBoard = T/5.0

nCurves = 25

print 'Genereating Wigley hull geometry using {0} curves.'.format(nCurves)
print 'L = {0:0.3f}, B = {1:0.3f}, T = {2:0.3f}.'.format(L,B,T)
print 'Freeboard heigth = {0:0.3f}.'.format(freeBoard)

xRange = (0,0.5)

z = linspace(0,T,nCurves)

polylines = []
IDs = []

yzPlane = geompy.MakePlaneLCS(None,1,2)
xzPlane = geompy.MakePlaneLCS(None,1,3)

geompy.addToStudy(yzPlane,'yzPlane')
geompy.addToStudy(xzPlane,'xzPlane')

# Create a set of polyLines at constant Z values
for i,Z in enumerate(z):
    X = "t"
    Y = buildExpr(B,L,T,X,Z)
    Z = str(Z)

    polylines.append(geompy.MakeCurveParametric(X, Y, Z, xRange[0], xRange[1], 500, GEOM.Polyline, theNewMethod=True))
    geompy.addToStudy(polylines[i], 'Polyline Parametric_{0:03d}'.format(i))

# Create vertical free board
freeboardPolyLines = []
X="t"
Z0 = z[0]
Y = buildExpr(B,L,T,X,Z0)
Z1 = str(Z0-freeBoard)

freeboardPolyLines.append(geompy.MakeCurveParametric(X, Y, Z1,xRange[0], xRange[1], 500, GEOM.Polyline, theNewMethod=True))
geompy.addToStudy(freeboardPolyLines[0],'Polyline Parametric_freeboard0')
    

# Create surfaces, mirror and glue
hullSurface_1 = geompy.MakeFilling(polylines)
hullSurface_2 = geompy.MakeFilling([freeboardPolyLines[0],polylines[0]])

HullFwd       = geompy.MakeGlueEdges([hullSurface_1,hullSurface_2], 1e-7)
HullAft       = geompy.MakeMirrorByPlane(HullFwd, yzPlane)
HullStb       = geompy.MakeGlueEdges([HullFwd, HullAft], 1e-07)
HullPrt       = geompy.MakeMirrorByPlane(HullStb, xzPlane)

geompy.addToStudy(hullSurface_1,'hullSurface_1')
geompy.addToStudy(hullSurface_2,'hullSurface_2')
geompy.addToStudy(HullFwd,'HullFwd')
geompy.addToStudy(HullAft,'HullAft')
geompy.addToStudy(HullStb,'HullStb')
geompy.addToStudy(HullPrt,'HullPrt')

print 'Writing iges geometry file WigleyHullStb.igs'
print 'Writing iges geometry file WigleyHullPrt.igs'
geompy.ExportIGES(HullStb,"WigleyHullStb.igs")
geompy.ExportIGES(HullPrt,"WigleyHullPrt.igs")
#geompy.ExportSTL(HullPrt,"WigleyHullPrt.stl")

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)

