/*
 * sphereBed
 */

#include <iostream>
#include "bed.h"

using namespace std;

sphereBed::sphereBed(const sphere s, const double h, const double d)
: spheres_(s), r_(d/2), h_(h), packingDensity_(0.74),
  baseArea_(M_PI*pow(r_,2)),volume_(baseArea_*h)
{
}

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
    cout << "# spheres in bed  = " << N() << nl
         << "Bed surface area  = " << S() << nl
         << "Bed mass          = " << mass() <<endl;
}
