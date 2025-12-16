#!/usr/bin/env python3

from math import pi


def hole_area(diameter, n_holes=1):
    return 0.25 * pi * diameter**2 * n_holes


def velocity(flux, diameter, n_holes=1):
    return flux/hole_area(diameter, n_holes)


def p_dyn(flux, diameter, rho=1000, n_holes=1):
    return 0.5 * rho \
           * velocity(flux, diameter, n_holes)**2


def Re(flux, diameter, rho=1000, n_holes=1):
    v = velocity(flux, diameter, n_holes)
    nu = 0.6e-6
    return diameter * v / nu


def throw_length(flux, diameter, rho=1000, n_holes=1):
    v = velocity(flux, diameter, n_holes)
    v0 = 0.1
    k = 0.15
    return diameter/k/v/v0


if __name__ == '__main__':
    flowrate = 30e-3/60

    d_h = 4e-3
    n_h = 23 * 4

    d_p = 39e-3
    d_s = 31e-3

    sup_vel = velocity(flowrate, d_s)
    diff_vel = velocity(flowrate, d_p)
    hole_vel = velocity(flowrate, d_h, n_h)

    pdyn_fraction = p_dyn(flowrate, d_p, n_holes=1) \
                  / p_dyn(flowrate, d_h, n_holes=n_h)

    print(f'Hole diameter      {d_h*1000} mm')
    print(f'Number of holes    {n_h}')
    print(f'Holes area         {1e6*hole_area(d_h, n_h):0.2f} mm2')
    print(f'Pipe area          {1e6*hole_area(d_p):0.2f} m2')

    print(f'Supply velocity    {sup_vel:0.2f}')
    print(f'Diffuser velocity  {diff_vel:0.2f}')
    print(f'Holes velocity     {hole_vel:0.2f}')
    print(f'Dynamic p fraction {pdyn_fraction:0.2f}')

    Re_h = Re(flowrate, d_h, n_holes=n_h)
    jet_length = throw_length(flowrate, d_h, n_holes=n_h)

    print(f'Re holes            {Re_h:0.2f}')
    print(f'Jet length          {jet_length:0.2f}')
    print(f'Flowrate            {flowrate:0.2g}')
    print(f'Flowrate per hole   {flowrate/n_h:0.4g}')

