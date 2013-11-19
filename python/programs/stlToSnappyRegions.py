#!/usr/bin/env python

import os,sys

def getArgs():
    from optparse import OptionParser
    descString = """
    Python thing to create a template snappyHexMeshDict
    based on input stl-file with solid regions.
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--file',dest='stlFile',default=None,help='Input stl file')
    parser.add_option('-o','--output',dest='output',default=None,help='Output file')
    (opt,arg)=parser.parse_args()

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)

    if not opt.stlFile: argError( 'Missing stl file argument' )

    stlIn = opt.stlFile
    stlBase = os.path.splitext(stlIn)[0]
    stlExt = os.path.splitext(stlIn)[1]
    snappyFileName = opt.output
    snappyOut = 0
    if not opt.output:
        snappyOut = sys.stdout
    else:
        snappyOut = open(snappyFileName,'w')

    argDict = { 'stlIn':stlIn,
                'snappyOut':snappyOut}

    return argDict

def getStlSolids(stlFile):
    import re
    fp = open(stlFile,'r')

    solids = []
    solidPat = re.compile('^\s*solid (.*)$')
    for line in fp:
        match = solidPat.match(line)
        if match:
            solids.append(match.groups()[0])
    return solids

class dbDict:
    def __init__(self):
        self.tab = '    '
        self.nl = '\n'
        self.nlc = ';\n'
        self.start = '{\n'
        self.end = '}\n'
        self.level = 0
        self.indent = self.level*self.tab
        self.entries=[]

    def ilevel(self,i):
        self.level += i
        self.indent = self.level*self.tab

    def startDict(self,name):
        s = self.indent+name+self.nl
        s += self.indent+self.start
        self.ilevel(1)
        return s

    def endDict(self):
        self.ilevel(-1)
        s = self.indent+self.end
        return s

    def entry(self,name,value):
        return self.indent+name+' '+value+self.nlc

    def subDict(self, name='', key='', value=''):
        self.ilevel(1)
        s = self.startDict(name)
        s+= self.entry(key,value)
        s+= self.endDict()
        self.ilevel(-1)
        return s


def composeRegions(stlFileName):
    args = getArgs()

    stlSolids = getStlSolids(stlFileName)

    stlName = os.path.basename(stlFileName)

    regionString = ''
    refString = ''
    levelString = ''

    e = dbDict()

    # Build region information string
    e.ilevel(1)
    regionString += e.startDict(stlName)+e.entry('type', 'triSurfaceMesh')
    regionString += e.startDict('regions')
    e.ilevel(-1)

    for solid in stlSolids:
        regionString += e.subDict(name=solid, key='name',value=solid)
    e.ilevel(1)

    regionString += e.endDict()
    regionString += e.endDict()

    # build refnement regions information string
    e.ilevel(1)
    refString    += e.startDict(stlName)+e.entry('level', '(0 0)')
    refString    += e.startDict('regions')
    e.ilevel(-1)

    for solid in stlSolids:
        refString    += e.subDict(name=solid, key='level',value='(1 1)')
    e.ilevel(1)

    refString    += e.endDict()
    refString    += e.endDict()

    # build layer addition information string
    e.ilevel(-1)
    for solid in stlSolids:
        levelString    += e.subDict(name=solid, key='nSurfaceLayers',value='0')
    e.ilevel(1)

    return (regionString, refString, levelString)


def applyTemplate():
    from stlToSnappyRegions import dictTemplate
    import re
    args = getArgs()
    stlFileName = args['stlIn']
    out = args['snappyOut']

    regionString, refString, levelString  = composeRegions(stlFileName)

    tmp0 = re.sub('GEOMETRY_STL', regionString, dictTemplate())
    tmp1 = re.sub('GEOMETRY_LEVELS', refString, tmp0)
    tmp2 = re.sub('WALL_LAYERS', levelString, tmp1)
    out.write(tmp2)

if __name__=='__main__':
    applyTemplate()


def dictTemplate():
    template = """FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      autoHexMeshDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

castellatedMesh true;
snap            true;
addLayers       true;


geometry
{
    /*
    box
    {
        type searchableBox;
        min (1 1 1);
        max (2 2 2);
    }
    */

GEOMETRY_STL
};



castellatedMeshControls
{
    maxLocalCells 2000000;

    maxGlobalCells 8000000;

    minRefinementCells 0;

    maxLoadUnbalance 0.10;

    nCellsBetweenLevels 1;

    features
    (
        //{
        //    file "someLine.eMesh";
        //    level 2;
        //}
    );

    refinementSurfaces
    {
        /* example try to create zones
        heater
        {
            level (1 1);
            faceZone heater;
            cellZone heater;
            zoneInside true;
        }
        */

GEOMETRY_LEVELS
    }

    resolveFeatureAngle 30;

    refinementRegions
    {
        /*
        box
        {
            mode inside;
            levels ((1.0 4));
        }
        */
    }

    locationInMesh (5 0.28 0.43);

    allowFreeStandingZoneFaces false;
}



snapControls
{
    nSmoothPatch 3;

    tolerance 1.0;

    nSolveIter 30;

    nRelaxIter 5;

    nFeatureSnapIter 20;
}



addLayersControls
{
    relativeSizes true;

    layers
    {
WALL_LAYERS
    }

    expansionRatio 1.2;

    finalLayerThickness 0.3;

    minThickness 0.25;

    nGrow 1;

    // Advanced settings

    featureAngle 60;

    nRelaxIter 5;

    nSmoothSurfaceNormals 1;

    nSmoothNormals 3;

    nSmoothThickness 10;

    maxFaceThicknessRatio 0.5;

    maxThicknessToMedialRatio 0.3;

    minMedianAxisAngle 90;

    nBufferCellsNoExtrude 0;

    nLayerIter 50;

    nRelaxedIter 20;
}



meshQualityControls
{
    maxNonOrtho 65;

    maxBoundarySkewness 20;

    maxInternalSkewness 4;

    maxConcave 80;

    minVol 1e-13;

    minTetQuality 1e-9;

    minArea -1;

    minTwist 0.05;

    minDeterminant 0.001;

    minFaceWeight 0.05;

    minVolRatio 0.01;

    minTriangleTwist -1;


    // Advanced

    nSmoothScale 4;
    errorReduction 0.75;

    relaxed
    {
        maxNonOrtho 75;
    }

}


// Advanced

debug 0;

mergeTolerance 1E-6;


// ************************************************************************* //
"""
    return template
