/*
 * material
 */

#include "material.h"

material::material(const double rho,const double Cp,const double kappa)
: rho_(rho), Cp_(Cp), kappa_(kappa)
{}

double material::Cp()  const { return Cp_; }
double material::rho() const { return rho_; }
double material::kappa()  const { return kappa_; }

air::air(const double rho,const double Cp,const double kappa)
: material(rho,Cp,kappa)
{}

double air::Cp(const double T, const double p) const
{
    return Cp_;
}
double air::rho(const double T, const double p) const
{
    return rho_;
}
double air::kappa(const double T, const double p) const
{
    return kappa_;
}

