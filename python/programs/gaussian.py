#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import array,linspace,exp
from matplotlib import pyplot as plt

class gaussian:
    def __init__(self,a,b,c,x=array([]),y=array([])):
        self.__dict__.update(locals())
        del self.__dict__['self']

    def func(self,x):
        self.x = x
        a = self.a
        b = self.b
        c = self.c
        return a*exp(-(x-b)**2/(2*c**2))

    def plot(self,x):
        plt.plot(x,self.func(x))



if __name__ == "__main__":
    G1 = gaussian(1,0,4)
    G2 = gaussian(1,0,4)
    x = linspace(0,10,100)
    y = G1.func(x)/G2.func(x)
    G1.plot(x)
    G2.plot(x)
    #plt.plot(x,y)
    plt.grid('on')
    plt.show()
