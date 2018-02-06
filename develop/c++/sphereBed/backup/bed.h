#ifndef BED_H
#define BED_H

#include <math.h>
#include "defines.h"
#include "sphere.h"

class sphereBed
{
    private:
        const double packingDensity_;
        const sphere spheres_;
        const double r_;
        const double h_;
        const double volume_;
        const double baseArea_;

    public:
        sphereBed(const sphere s, const double h, const double d);

        const sphere& pebble() {return spheres_;};
        double volume() {return volume_;};

        int N() const;

        double S() const;
        double mass() const;
        double heat(double T) const;

        void info() const;
};
#endif
