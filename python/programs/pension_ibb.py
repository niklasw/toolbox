#!/usr/bin/env python3
import sys
from numpy import array, where

IBB = 80600
I = IBB / 12 * 7.5  # salary breakpoint

pk1 = 0.06      # kollektivavtal 6% to Tj.pension below I
pk2 = 0.31      # kollektivavtal 31.5 % to Tjp above I
pe  = 0.1       # EQUA 10 % flat to Tjp
# L0             Salary at break even betw equa and kollektivavtal

# Algebra :-) calculate break-even salary L0
# pk1 * I + pk2 * (L0 - I) = pe * L0
# pk1 * I + pk2 * L0 - pk2 * I = pe * L0
# pk1 * I - pk2 * I = (pe - pk2) * L0

L0 = I * (pk1 - pk2)/(pe - pk2)

assert (pk1 * I + pk2 * (L0 - I) - pe * L0) < 1e-4

print(f'Breakpoint for gov. pension {I} kr/month')

print(f'Breakpoint at {L0} kr/month')

while True:
    try:
        L = float(input('My salary: '))
        break
    except:
        continue

def pos(x):
    """Pos function for arrays and floats"""
    if isinstance(x, (int, float)):
        return max(0, x)
    else:
        return where(x <= 0, 0, x)


def gmin(a, b):
    if all((isinstance(x, (int, float)) for x in (a, b))):
        return min(a, b)
    else:
        return where(array(a) < b, a, b)


Pkfunc = lambda L: pk1 * gmin(L, I) + pk2  * pos(L - I)
Pefunc = lambda L: pe * L

Pk = pk1 * I + pk2 * pos(L - I)
Pe = pe * L

print(f'Inkomstbasbelopp 2024             = {I} kr/m')
print(f'Pensionsavsättning kollektivavtal = {Pk} kr/m')
print(f'Pensionsavsättning equa           = {Pe} kr/m')
print(f'Diff                              = {Pe-Pk} kr/m')

if len(sys.argv) > 1 and sys.argv[1] == 'plot':
    from matplotlib import pyplot as plt
    from numpy import arange
    L = arange(int(20e3), int(80e3))

    plt.plot(L, Pkfunc(L), label=f'K.avtal {pk1*100}%/{pk2*100}%')
    plt.plot(L, Pefunc(L), label='EQUA')
    plt.plot([L0, L0], [0,1e4], '--', label=f'Brytp. {L0:.0f}')
    plt.legend()
    plt.grid(True)
    plt.ylabel('Avsättning, kr/mån.')
    plt.xlabel('Lön, kr/mån')
    plt.show()
