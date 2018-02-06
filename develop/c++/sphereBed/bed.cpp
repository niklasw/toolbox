/*
 * sphereBed
 */

#include <iostream>
#include "bed.h"

using namespace std;

sphereBed::sphereBed(const sphere s, const double h, const double d)
: spheres_(s), r_(d/2), h_(h), packingDensity_(0.74),
  baseArea_(M_PI*pow(d/2,2)),
  volume_(M_PI*pow(d/2,2)*h)
{}

int sphereBed::N() const
{
    return floor(volume_/spheres_.V()*packingDensity_);
}

double sphereBed::S() const
{
    return N()*spheres_.S();
}

double sphereBed::mass() const
{
    return N()*spheres_.mass();
}

double sphereBed::heat(double deltaT) const
{
    return mass()*spheres_.mat().Cp()*deltaT;
}


void sphereBed::info() const
{
    cout << "bed info" << tnl
         << "# spheres in bed  = " << N() << tnl
         << "Bed surface area  = " << S() << tnl
         << "Bed mass          = " << mass() <<endl;
}
