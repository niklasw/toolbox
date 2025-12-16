#!/usr/bin/env python3

K =  273.15

T_p = 36.9            # Temp return to pump
V_p = 13.5          # Flow to pump

T_r = 35.5          # Temp radiators
T_t = 40.0       # Temp tank

V_r = V_p * (T_p - T_t)/(T_r - T_t)

print(f'Heatpump flowrate    V_p {V_p:0.1f} l/min')
print(f'Heatpump temperature T_p {T_p:0.1f} C')
print(f'Radiator temperature T_r {T_r:0.1f} C')
print(f'Tank temperature     T_t {T_t:0.1f} C')

print('\nCalculated:')
print(f'Radiator flowrate    V_r {V_r:0.1f} l/min')

Cp = 4180
T1 = 38.9
T2 = 35.2

deltaT_r = dT = T1 - T2

P = Cp * dT * V_r/60
print(f'Radiator power       {P:0.1f} W')







