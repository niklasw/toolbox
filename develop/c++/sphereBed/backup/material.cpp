/*
 * material
 */

#include "material.h"

material::material(const double rho,const double Cp,const double kappa)
: rho_(rho), Cp_(Cp), kappa_(kappa)
{}

double material::rho() const { return rho_; }
double material::Cp()  const { return Cp_; }
double material::kappa()  const { return kappa_; }


