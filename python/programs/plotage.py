#!/usr/bin/env python3

from matplotlib import pyplot as plt
from numpy import floor, ceil, sqrt
from itertools import cycle
from datetime import datetime, timedelta
from dateutil import rrule

born = datetime(1973, 4, 9)
dad = datetime(2006, 7, 13)
dead = born + timedelta(days=365*90)

n_months = \
    len([0 for a in rrule.rrule(rrule.MONTHLY, dtstart=born, until=dead)])
nx = int(ceil(sqrt(n_months)))
nx = 2*12

color = n_months*['']
x_counter = cycle(range(nx))
i = 0
age = 0
x = []
y = []

for dtime in rrule.rrule(rrule.MONTHLY, dtstart=born, until=dead):
    if dtime < dad:
        color[i] = 'lightblue'
    elif dtime.year == datetime.now().year and \
         dtime.month == datetime.now().month:
        color[i] = 'red'
        age = i
    elif dtime < datetime.now():
        color[i] = 'olive'
    else:
        color[i] = 'orange'
    x.append(next(x_counter))
    y.append(int(floor(i/nx)))
    i += 1


color[0] = 'pink'
color[-1] = 'black'

_, ax = plt.subplots(1, 1)
ax.scatter(x, y, c=color)
ax.axis('equal')
ax.grid(False)
ax.set_title(f'age {age} months. one row = {nx} months')
plt.show()
