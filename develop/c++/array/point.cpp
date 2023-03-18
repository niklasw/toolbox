#include "point.h"

point::point()
:
    Array<double,3>()
{
    fill(0);
};

point::point(double d)
:
    Array<double,3>()
{
    fill(d);
};

point::point(Array<double,3> A)
:
    Array<double,3>(A)
{
};

point::point(double x, double y, double z)
:
    Array<double,3>()
{
    this->operator[](0) = x;
    this->operator[](1) = y;
    this->operator[](2) = z;
};

//- non-const access for components assignment
double& point::x() {return this->operator[](0);};
double& point::y() {return this->operator[](1);};
double& point::z() {return this->operator[](2);};

//- const access needed for when used as const point& attribute
const double& point::x() const {return this->operator[](0);};
const double& point::y() const {return this->operator[](1);};
const double& point::z() const {return this->operator[](2);};

std::ostream& operator<<(std::ostream& os, const point& p)
{
    os << '(' << p[0];
    for(int i=1; i<p.size(); i++)
    {
        os << ' ' << p[i];
    }
    os << ')';

    return os;
}

