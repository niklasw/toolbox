#ifndef SPHERE_H
#define SPHERE_H

#include <list>
#include <vector>
#include <memory>
#include "defines.h"
#include "material.h"

using namespace std;

class sphere
{
    private:
        const double r_;
        const material mat_;

    public:
        sphere(const double r, const material mat);

        double V() const;

        double S() const;

        double mass() const;

        const material& mat() const { return mat_;};

        const double R() const {return r_;};

        void info() const;
};

class sphereList : public list<sphere>
{
    private:

    public:
        sphereList();
        sphereList(const list<double>& radiis, const material& mat);
        sphereList(const vector<double>& radiis, const material& mat);

        void append(const sphere& s);
        void append(const double r, const material& mat);

        list<double> radii() const;

};

#endif
