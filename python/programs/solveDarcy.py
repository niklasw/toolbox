#!/usr/bin/env python3

import numpy as np

nu = 1e-6
rho = 1
u1 = 0.1
u2 = 0.2
R1 = 0.03
R2 = 0.11

A = np.array([[nu*u1, 0.5*u1**2],
             [nu*u2, 0.5*u2**2]])
B = np.array([[R1],[R2]])
X = np.linalg.inv(A).dot(B)
print(f'Darcy = {X[0][0]}, Forschheimer = {X[1][0]}')
