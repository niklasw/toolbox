region0 = getRegion()
region0.decimate(targetEdgeLength=20, limitDihedralAngle=1, dihedralAngle=5, swapAngle=10, splitAngle=15, minAngle=5, maxAngle=175, clpsFcRotAng=15, clpsEdRotAng=15, clpsShrtThan=0, shrtRatio=0, sizePropagationFactor=0.5, gradeMesh=1, noisyMesh=0, freezeBndryEdges=1)
region0.clearFreeEdgeHighlights()
region0.clearSharedEdgeHighlights()
region0.clearPenetrationHighlights()
nPenetrations = region0.computePenetrations(inBodiesOnly=1)
region0.highlightPenetrations()
region0.clearFreeEdgeHighlights()
region0.clearSharedEdgeHighlights()
nFreeE   = region0.nFreeEdges()
nSharedE = region0.nSharedEdges()
region0.clearFreeEdgeHighlights()
region0.clearSharedEdgeHighlights()

print "Number of penetrations =", nPenetrations
print "Number of free edges = ",nFreeE
print "Number of shared edges = ",nSharedE
#region0.exportSTL(filename="/home/fluidsim/UhTM/320_NCG_Studie_200/PRE/models/2010-11/NOISE/splitGeom/NOISE_EP_LHS_AW_PP.stl", isBinary=False)
