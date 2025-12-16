#!/usr/bin/env python3


car_gas_consumption = 0.07                  #l/km
electric_car_consumption = 0.25 * 3.6e6     #J/km
car_gas_consumption = 0.7 / 10              #l/km
gasoline_energy_density = 34.2              #J/l
gasoline_cost = 16.5                        #kr/l
electricity_cost = 1/3.6e6                  #kr/J

gas_cost_per_km = car_gas_consumption * gasoline_cost
electricity_cost_per_km = electric_car_consumption * electricity_cost

print(f'Running on gas [kr/km]: {gas_cost_per_km:.2f}, running electric: {electricity_cost_per_km:.2f}')

print(f'Break even electricity cost = {gas_cost_per_km / electricity_cost_per_km:.2f} kr/kWh')


