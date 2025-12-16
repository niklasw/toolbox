#!/usr/bin/env python3

import numpy as np

def Darcy_Forchheimer(length, velocity, mu, rho, darcy_coefficient, forchheimer_coefficient):
    """
    Calculate the pressure drop in a porous medium using the Darcy-Forchheimer equation.

    Parameters:
    length (float): Length of the porous medium (m)
    velocity (float): Superficial velocity of the fluid (m/s)
    mu (float): Dynamic viscosity of the fluid (Pa.s)
    darcy_coefficient (float): Darcy coefficient (1/m^2)
    forchheimer_coefficient (float): Forchheimer coefficient (1/m)

    Returns:
    float: Pressure drop across the porous medium (Pa)
    """
    # Calculate Darcy term
    darcy_term = (mu * velocity * length) * darcy_coefficient

    # Calculate Forchheimer term
    forchheimer_term = forchheimer_coefficient * 0.5 * rho * velocity**2 * length

    # Total pressure drop
    pressure_drop = darcy_term + forchheimer_term

    return pressure_drop


def server_rack_flowvelocity(area,
                             power_dissipation=10e3,
                             specific_heat=1005,
                             inlet_temp=293.15,
                             outlet_temp=313.15,
                             density=1.2):
    """
    Calculate the flow velocity of air through a server rack based on power dissipation and temperature rise.

    Parameters:
    area (float): Cross-sectional area of the airflow (m^2)
    power_dissipation (float): Power dissipation of the server rack (W)
    specific_heat (float): Specific heat capacity of air (J/kg.K)
    inlet_temp (float): Inlet air temperature (K)
    outlet_temp (float): Outlet air temperature (K)
    density (float): Density of air (kg/m^3)

    Returns:
    float: Flow velocity of air through the server rack (m/s)
    """
    # Calculate mass flow rate
    delta_temp = outlet_temp - inlet_temp
    mass_flow_rate = power_dissipation / (specific_heat * delta_temp)

    # Calculate volumetric flow rate
    volumetric_flow_rate = mass_flow_rate / density

    # Calculate flow velocity
    flow_velocity = volumetric_flow_rate / area

    return flow_velocity


# Example usage
if __name__ == "__main__":
    server_rack_width = 0.5
    server_rack_height = 2 
    server_rack_depth = 1.0
    cross_sectional_area = server_rack_width * server_rack_height
    velocity = 1.0  # m/s
    mu = 18e-5    # Pa.s
    rho = 1.2     # kg/m^3
    darcy_coefficient = 10
    forchheimer_coefficient = 10

    print("Calculating pressure drop using Darcy-Forchheimer equation...")
    print(f'Cross-sectional area: {cross_sectional_area:.2f} m^2')
    print(f'Target flow velocity: {velocity:.2f} m/s')
    print(f'Darcy coefficient: {darcy_coefficient:.2f} 1/m^2')
    print(f'Forchheimer coefficient: {forchheimer_coefficient:.2f} 1/m')

    length = server_rack_depth  # Length of the porous medium (m)
    pressure_drop = Darcy_Forchheimer(length, velocity, mu, rho, darcy_coefficient, forchheimer_coefficient)
    print(f"Pressure drop across the porous medium: {pressure_drop:.2f} Pa")
    absolute_momentum_source = pressure_drop * cross_sectional_area
    print(f"Absolute momentum source: {absolute_momentum_source:.2f} N")





