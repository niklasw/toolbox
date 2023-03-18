#include <iostream>
#include <array>

using namespace std;

class point
: public array<double,3>
{
    public:
        point();

        point(double d);

        point(double x, double y, double z);

        //- non-const access for components assignment
        double& x();
        double& y();
        double& z();

        //- const access needed for when used as const point& attribute
        const double& x() const;
        const double& y() const;
        const double& z() const;

        //- unary operators should belong to class
        point& operator+=(const point& p);
        point& operator+=(double d);

        //- binary operators shoudl be friends (not belong to class)
        friend point operator+(point p1, const double& d);
        friend point operator+(const double& d, point p1);
        friend point operator+(point p1, const point& p2);
        friend ostream& operator<<(ostream& os, const point& p);
};

