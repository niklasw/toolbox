#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import *

x=linspace(-pi,pi,100)
plt.plot(x,tanh(x)+1)



plt.grid('on')
plt.show()
