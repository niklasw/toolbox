#ifndef MATERIAL_H
#define MATERIAL_H

#include "defines.h"

class material
{
    private:
        const double rho_;
        const double Cp_;
        const double kappa_;

    public:
        material(const double rho,const double Cp,const double kappa);

        //- Access
        double rho() const;
        double Cp() const;
        double kappa() const;
};

#endif

