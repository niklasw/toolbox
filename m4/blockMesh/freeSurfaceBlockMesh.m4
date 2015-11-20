/*--------------------------------*- C++ -*----------------------------------*\\
|==========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  2.0.0                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

divert(-1)
changecom(//)changequote([,])
define(calc, [esyscmd(perl -e 'print ($1)')])
//define(icalc, [esyscmd(perl -e 'printf("%d",$1)')])
define(icalc, [esyscmd(python -c 'from math import *; import sys; sys.stdout.write(str(int(round($1))))')])
define(calcStretch, [esyscmd(stretchCalculator.py --length=$1 --first=$2 --last=$3 --shortOutput)])
define(VCOUNT, 0)
define(vlabel, [[// ]Vertex $1 = VCOUNT define($1, VCOUNT)define([VCOUNT], incr(VCOUNT))])
define(pi, 3.14159265)
define(Hex, hex (v1$1 v2$1 v3$1 v4$1 v1$2 v2$2 v3$2 v4$2))

define(L, 1.0)
define(baseSize,calc(L/16))

define(baseThickness,calc(baseSize/1))
define(midThickness, calc(baseSize/8))
define(thinThickness,calc(baseSize/16))

define(xMin, calc(-3*L))
define(xMax, calc(5*L))
define(yMin, calc(-2*L))
define(yMax, calc(2*L))

// Remember to change here as well as Min Max values
// since cannot use calc for xMax-xMin. Some "--" expansion issue.
define(Nx,calc(8*L/baseSize))
define(Ny,calc(4*L/baseSize))

// 'Xh' refers to height of block X
define(zSurf, 0.0)
define(hSurf, 0.05)
define(Ah,   1.5)
define(Bh,   0.5)
define(BBh,  0.25)
define(Ch, hSurf)
define(CCh,  0.15)
define(Dh,   Bh)
define(Eh,   0.5)

define(stretchFactor,calc(baseThickness/midThickness))
define(stretchNz, calcStretch(Bh,midThickness,baseThickness))

define(NzA, icalc(Ah/baseThickness))
define(NzB, stretchNz )
define(NzBB,icalc(BBh/midThickness))
define(NzC, icalc(Ch/thinThickness))
define(NzCC, icalc(CCh/midThickness))
define(NzD, stretchNz)
define(NzE, icalc(Eh/baseThickness))
define(stretchB, calc(1/stretchFactor))
define(stretchC, stretchFactor)

define(Ax0, xMin)
define(Ay0, yMin)
define(Az0, calc(zSurf-hSurf/2.0-Bh-BBh-Ah))
define(Ax1, xMax)
define(Ay1, yMax) 
define(Az1, calc(zSurf-hSurf/2.0-Bh-BBh)) 

define(Bx0, xMin)
define(By0, yMin)
define(Bz0, Az1)
define(Bx1, xMax)
define(By1, yMax) 
define(Bz1, calc(zSurf-hSurf/2.0-BBh))

define(BBx0, xMin)
define(BBy0, yMin)
define(BBz0, Bz1)
define(BBx1, xMax)
define(BBy1, yMax) 
define(BBz1, calc(zSurf-hSurf/2.0))

define(Cx0, xMin)
define(Cy0, yMin)
define(Cz0, BBz1)
define(Cx1, xMax)
define(Cy1, yMax) 
define(Cz1, calc(zSurf+hSurf/2.0))

define(CCx0, xMin)
define(CCy0, yMin)
define(CCz0, Cz1)
define(CCx1, xMax)
define(CCy1, yMax) 
define(CCz1, calc(zSurf+hSurf/2.0+CCh))

define(Dx0, xMin)
define(Dy0, yMin)
define(Dz0, CCz1)
define(Dx1, xMax)
define(Dy1, yMax) 
define(Dz1, calc(zSurf+hSurf/2.0+CCh+Dh))

define(Ex0, xMin)
define(Ey0, yMin)
define(Ez0, Dz1)
define(Ex1, xMax)
define(Ey1, yMax) 
define(Ez1, calc(zSurf+hSurf/2.0+CCh+Dh+Eh))

define(Fx0, xMin)
define(Fy0, yMin)
define(Fz0, Ez1)
//define(Fx1, xMax)
//define(Fy1, yMax) 
//define(Fz1, calc(zSurf+hSurf/2.0)+Dh+Eh)

define(bvert, ($1x$2 $1y0 $1z0))
define(tvert, ($1x$2 $1y0 $1z1))

divert(1)

convertToMeters 1;

vertices
(

    (Ax0 Ay0 Az0)    vlabel(v1A)
    (Ax1 Ay0 Az0)    vlabel(v2A)
    (Ax1 Ay1 Az0)    vlabel(v3A)
    (Ax0 Ay1 Az0)    vlabel(v4A)
                               
    (Ax0 Ay0 Bz0)    vlabel(v1B)
    (Ax1 Ay0 Bz0)    vlabel(v2B)
    (Ax1 Ay1 Bz0)    vlabel(v3B)
    (Ax0 Ay1 Bz0)    vlabel(v4B)
                               
    (Bx0 By0 BBz0)    vlabel(v1BB)
    (Bx1 By0 BBz0)    vlabel(v2BB)
    (Bx1 By1 BBz0)    vlabel(v3BB)
    (Bx0 By1 BBz0)    vlabel(v4BB)

    (BBx0 BBy0 Cz0)    vlabel(v1C)
    (BBx1 BBy0 Cz0)    vlabel(v2C)
    (BBx1 BBy1 Cz0)    vlabel(v3C)
    (BBx0 BBy1 Cz0)    vlabel(v4C)

    (Cx0 Cy0 CCz0)    vlabel(v1CC)
    (Cx1 Cy0 CCz0)    vlabel(v2CC)
    (Cx1 Cy1 CCz0)    vlabel(v3CC)
    (Cx0 Cy1 CCz0)    vlabel(v4CC)

    (CCx0 CCy0 Dz0)    vlabel(v1D)
    (CCx1 CCy0 Dz0)    vlabel(v2D)
    (CCx1 CCy1 Dz0)    vlabel(v3D)
    (CCx0 CCy1 Dz0)    vlabel(v4D)

    (Dx0 Dy0 Ez0)    vlabel(v1E)
    (Dx1 Dy0 Ez0)    vlabel(v2E)
    (Dx1 Dy1 Ez0)    vlabel(v3E)
    (Dx0 Dy1 Ez0)    vlabel(v4E)

    (Ex0 Ey0 Fz0)    vlabel(v1F)
    (Ex1 Ey0 Fz0)    vlabel(v2F)
    (Ex1 Ey1 Fz0)    vlabel(v3F)
    (Ex0 Ey1 Fz0)    vlabel(v4F)

);

blocks
(
    Hex(A,B)  (Nx Ny NzA) simpleGrading (1 1 1)
    Hex(B,BB)  (Nx Ny NzB) simpleGrading (1 1 stretchB) 
    Hex(BB,C) (Nx Ny NzBB) simpleGrading (1 1 1) 
    Hex(C,CC)  (Nx Ny NzC) simpleGrading (1 1 1) 
    Hex(CC,D)  (Nx Ny NzCC) simpleGrading (1 1 1) 
    Hex(D,E)  (Nx Ny NzD) simpleGrading (1 1 stretchC) 
    Hex(E,F)  (Nx Ny NzE) simpleGrading (1 1 1) 
);

edges ();
boundary
(
    symmetryPort
    {
        type symmetryPlane;
        faces
        (
            (v1A  v2A  v2B  v1B)
            (v1B  v2B  v2BB v1BB)
            (v1BB v2BB v2C  v1C)
            (v1C  v2C  v2CC  v1CC)
            (v1CC  v2CC  v2D  v1D)
            (v1D  v2D  v2E  v1E)
            (v1E  v2E  v2F  v1F)
        );
    }
    symmetryStarbord
    {
        type symmetryPlane;
        faces
        (
            (v3A  v4A  v4B  v3B)
            (v3B  v4B  v4BB v3BB)
            (v3BB v4BB v4C  v3C)
            (v3C  v4C  v4CC v3CC)
            (v3CC v4CC v4D  v3D)
            (v3D  v4D  v4E  v3E)
            (v3E  v4E  v4F  v3F)
        );
    }

    inlet
    {
        type patch;
        faces
        (
            (v1A  v1B  v4B  v4A)
            (v1B  v1BB v4BB v4B)
            (v1BB v1C  v4C  v4BB)
            (v1C  v1CC v4CC v4C)
            (v1CC v1D  v4D  v4CC)
            (v1D  v1E  v4E  v4D)
            (v1E  v1F  v4F  v4E)
        );
    }
    outlet
    {
        type patch;
        faces
        (
            (v2A  v3A  v3B  v2B)
            (v2B  v3B  v3BB v2BB)
            (v2BB v3BB v3C  v2C)
            (v2C  v3C  v3CC  v2CC)
            (v2CC  v3CC  v3D  v2D)
            (v2D  v3D  v3E  v2E)
            (v2E  v3E  v3F  v2F)
        );
    }
    symmetryBottom
    {
        type symmetryPlane;
        faces
        (
            (v1A v4A v3A v2A)
        );
    }
    atmosphere
    {
        type patch;
        faces
        (
            (v1F v2F v3F v4F)
        );
    }
);

mergePatchPairs ();

/*
BaseSize       baseSize
StretchHeight  Bh
BaseThickness  baseThickness
MidThickness   midThickness
ThinThickness  thinThickness
NStretchLayers stretchNz

Uniform min Z  calc(zSurf-hSurf/2-BBh)
Uniform max Z  calc(zSurf+hSurf/2+CCh)
*/


