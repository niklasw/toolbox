#ifndef POINT_H
#define POINT_H

#include <iostream>
#include "Array.h"

using namespace std;

class point
: public Array<double,3>
{
    public:
        point();

        point(double d);

        point(double x, double y, double z);

        point(Array<double,3> A);

        //- non-const access for components assignment
        double& x();
        double& y();
        double& z();

        //- const access needed for when used as const point& attribute
        const double& x() const;
        const double& y() const;
        const double& z() const;

        // friends are not inherited, since they don't belong to class.

        friend ostream& operator<<(ostream& os, const point& p);

        template<typename Type, size_t S>
        friend Array<Type,S> operator*(const Array<Type,S>&, const Array<Type,S>&);

        template<typename Type, size_t S>
        friend Array<Type,S> operator*(const Array<Type,S> , const Type& v);

        template<typename Type, size_t S>
        friend Array<Type,S> operator*(const Type& v, const Array<Type,S>&);
};
#endif
