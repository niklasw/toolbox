#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def U(u_ref, z_ref, z, z_g, z_0, kappa):
    u_star = kappa*u_ref/np.log((z_ref + z_0)/z_0)
    return u_star/kappa*np.log((z-z_g + z_0)/z_0)


h_bld = 33      # building height used for Cp in IDA ICE (?)
u_ref = 4.35 
z_ref = 10
z_0 = 0.1
z_g = 0
kappa = 0.41

z = np.linspace(0, 50, 100)


plt.plot(U(u_ref, z_ref, z, z_g, z_0, kappa), z, label='U_ref={}, z_ref={}'.format(u_ref,z_ref))  
#z_ref = 20
#plt.plot(U(u_ref, z_ref, z, z_g, z_0, kappa), z, label='U_ref={}, z_ref={}'.format(u_ref,z_ref))  
#z_ref = 10
#u_ref = 8.703
#plt.plot(U(u_ref, z_ref, z, z_g, z_0, kappa), z, 'o', label='U_ref={}, z_ref={}'.format(u_ref,z_ref))  

plt.grid(True)
plt.legend()
plt.suptitle('Atmospheric boundary layer')
plt.title('(OpenFOAM implementation)')
plt.xlabel('U [m/s]')
plt.ylabel('z [m]')

print('U_ref = {} m/s'.format(u_ref))
print('z_ref = {} m'.format(z_ref))
print('h_bld = {} m'.format(h_bld))
print('U_roof ={} m/s'.format(U(u_ref,z_ref,h_bld,z_g,z_0,kappa)))


plt.show()
