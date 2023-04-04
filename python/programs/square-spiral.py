#!/usr/bin/env python3

from matplotlib import pyplot as plt
from numpy import array
import sys

# Drawing a square spiral with equidistant points
# Took me a f..ng day

try:
    n_steps = int(sys.argv[1])
except Exception:
    print('You may give n_steps as argument')
    n_steps = 10

origin = array([0, 0])
ds = 1.0


def walk_dir(n, axis: int = 0):
    """Returns list of tuples, (direction, n_steps).
    direction tells if the step size should be -1, 0 or 1 along the axis
    defined by the axis attribute (0 or 1 for x or y respectively).
    n_steps tells how many steps to taken."""
    sign = 1
    steps = 0
    for i in range(n):
        d = ((i + axis) % 2) * sign
        if i % 2 == 0:
            sign *= -1
            steps += 1
        yield (d, steps)


def walk(n, ds=1):
    xy = [[0], [0]]
    for d in [0, 1]:
        for i, step in enumerate(walk_dir(n, d)):
            for j in range(step[1]):
                c = xy[d]
                c.append(c[-1] + step[0])
    return xy


coords = array(walk(n_steps))
print(f'Number of points = {len(coords[0])}')

fig, axes = plt.subplots(1, 2)
ax1 = axes[0]
ax2 = axes[1]
ax1.plot(coords[0], coords[1], 'r-o')
ax2.plot(coords[0], -coords[1], 'g-o')
ax1.axis('equal')
ax2.axis('equal')
plt.show()
