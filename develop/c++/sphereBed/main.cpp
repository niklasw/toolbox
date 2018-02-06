#include <iostream>
#include <stdio.h>
#include <vector>
#include "defines.h"
#include "material.h"
#include "sphere.h"
#include "bed.h"

#include "utils.h"
#include "qtPlot.h"

using namespace std;

int main(int argc, char** argv)
{
    double D = 0.02;
    if (argc == 2)
    {
        D = atof(argv[1]);
    }

    double R = D/2;
    double bedDiameter = 0.7;
    double bedHeight   = 1.0;

    material alO3(2000,4000,0.9);

    double minD = 0.0025, maxD = 0.02;
    int nD = 400;

    vector<double> radii = linspace(minD,maxD,nD);

    sphereList spheres(radii,alO3);

    double bedEnergy = sphereBed(spheres[0],bedHeight,bedDiameter).heat(1300);
    vector<int> nBalls(spheres.size());
    vector<double> areas(spheres.size());
    vector<double> mass(spheres.size());

    int i = 0;
    for (sphere s: spheres)
    {
        sphereBed bed(s,bedHeight,bedDiameter);
        areas[i] = bed.S();
        i++;
    }

    doPlot(argc,argv,radii,areas);
    return 0;
}
