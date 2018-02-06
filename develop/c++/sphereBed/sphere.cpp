#include <iostream>
#include <stdio.h>
#include <math.h>
#include "sphere.h"


using namespace std;

/*
 * sphere
 */

sphere::sphere(const double r, const material mat)
: r_(r), mat_(mat)
{}

double sphere::V() const
{
    return 4*M_PI*pow(r_,3)/3;
}

double sphere::S() const
{
    return 4*M_PI*pow(r_,2);
}

double sphere::mass() const
{
    return this->V()*mat_.rho();
}

void sphere::info() const
{
    cout << "sphere info" << tnl
         << "Volume = " << V() << tnl
         << "Area   = " << S() << tnl
         << "Mass   = " << mass() << endl;
}

/*
 * sphereList
 */

sphereList::sphereList()
: vector<sphere>()
{}

sphereList::sphereList(const vector<double>& radiis, const material& mat)
: vector<sphere>()
{
    for(double r: radiis)
    {
        sphere s(r,mat);
        this->push_back(s);
    }
}

void sphereList::append(const sphere& s)
{
    this->push_back(s);
}

void sphereList::append(const double r, const material& mat)
{
    sphere s(r,mat);
    this->push_back(s);
}

vector<double> sphereList::radii() const
{
    vector<double> rr(this->size());
    for (const sphere& s: *this)
    {
        rr.push_back(s.R());
    }
    return rr;
}
