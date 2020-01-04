#!/usr/bin/env python3

"""
Demo of a line plot on a polar axis.
"""
import numpy as np
import matplotlib.pyplot as plt


r = np.arange(0, 2, 0.001)
theta = 8 * np.pi * r
alpha = np.radians(-15)*np.ones(len(r))

ax = plt.subplot(111, projection='polar')
ax.plot(theta, r)
ax.plot(alpha, r)
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)

ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()

