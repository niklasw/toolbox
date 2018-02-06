#include <iostream>
#include <stdio.h>
#include <vector>
#include "defines.h"
#include "material.h"
#include "sphere.h"
#include "bed.h"

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

    sphere s1(R, alO3);
    s1.info();

    sphereBed bed(s1,bedHeight,bedDiameter);
    bed.info();

    cout << "Heat req for 1700 K      = " << bed.heat(1700-300)
         << endl;

    double minD = 0.0025, maxD = 0.02;
    int nD = 40;

    vector<double> radii(nD);
    for (int i=0; i< nD; i++)
    {
        double dD = (maxD-minD)/nD;
        radii[i] = minD+i*dD;
    }

    sphereList spheres(radii,alO3);

    vector<double> heats(spheres.size());
    int i = 0;
    for (sphere s: spheres)
    {
        sphereBed bed(s,bedHeight,bedDiameter);
        heats[i] = bed.heat(1300);
        cout << s.R() << "\t"
             << heats[i] << "\t"
             << bed.S() << endl;
        i++;
    }
    heats[0] = heats[1];

    doPlot(argc,argv,radii,heats);
    return 0;
}
