#include "point2.h"

point::point()
:
    array()
{
    fill(0);
};

point::point(double d)
:
    array()
{
    fill(d);
};

point::point(double x, double y, double z)
:
    array({x,y,z})
{
};

//- non-const access for components assignment
double& point::x() {return this->operator[](0);};
double& point::y() {return this->operator[](1);};
double& point::z() {return this->operator[](2);};

//- const access needed for when used as const point& attribute
const double& point::x() const {return this->operator[](0);};
const double& point::y() const {return this->operator[](1);};
const double& point::z() const {return this->operator[](2);};

//- operators overloading, declared as friends to point in point.h

point& point::operator+=(const point& p)
{
    x()+=p.x();
    y()+=p.y();
    z()+=p.z();
    return *this;
};

point& point::operator+=(double d)
{
    this->operator+=(point(d));
    return *this;
};

//- Friend operators
point operator+(point p1, const double& d)
{
    return p1+=d;
}

point operator+(const double& d, point p1)
{
    return p1+d;
}

point operator+(point p1, const point& p2)
{
    return p1+=p2;
}

ostream& operator<<(ostream& os, const point& p)
{
    os << '(' << p.x() << ' ' << p.y() << ' ' << p.z() << ')';
    return os;
}
