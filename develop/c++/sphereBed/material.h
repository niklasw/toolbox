#ifndef MATERIAL_H
#define MATERIAL_H

#include "defines.h"

class material
{
    protected:
        const double rho_;
        const double Cp_;
        const double kappa_;

    public:
        material(const double rho,const double Cp,const double kappa);

        //- Access
        double Cp() const;
        double rho() const;
        double kappa() const;
};


class air : public material
{
    private:
        static constexpr double R_ = 8.3144598;

    public:
        air(const double rho,const double Cp,const double kappa);

        double Cp(const double T, const double p) const;
        double rho(const double T, const double p) const;
        double kappa(const double T, const double p) const;
};
#endif

