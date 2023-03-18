#!/usr/bin/env python3

from matplotlib import pyplot as plt
from numpy import floor, ceil, sqrt
from itertools import cycle
from datetime import datetime, timedelta

months = int(90.75*12)

born = datetime(1973, 4, 9)
age = datetime.now() - born
age_in_months = age.days/30.437
father = datetime(2006, 7, 13) - born
father_in_months = father.days/30.437

nx = int(ceil(sqrt(months)))

x = months*[0]
y = months*[0]
color = months*['']
x_counter = cycle(range(nx))
for i in range(months):
    if i < father_in_months:
        color[i] = 'lightblue'
    elif i < age_in_months - 1:
        color[i] = 'olive'
    elif i < age_in_months:
        color[i] = 'red'
    else:
        color[i] = 'orange'
    x[i] = next(x_counter)
    y[i] = int(floor(i/nx))
color[0] = 'pink'
color[-1] = 'black'

_, ax = plt.subplots(1, 1)
ax.scatter(x, y, c=color)
ax.axis('equal')
ax.grid(False)
ax.set_title(f'age {age_in_months:4.2f} months')
plt.show()
