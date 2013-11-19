#!/usr/bin/env python

import re,os,sys,fileinput
import Gnuplot,Gnuplot.PlotItems,Gnuplot.funcutils
from Numeric import *

g = Gnuplot.Gnuplot();

# * * * * * * * * * * * * * * * * * * * *
def wait(str=None, prompt='Press return to show results...\n'):
    if str is not None:
        print str
    raw_input(prompt)
# * * * * * * * * * * * * * * * * * * * *
#def writeData(fileName,data):
#     fh = open(fileName,'rw')
#     lines = fh.readlines()
#     fh.write(str(data))
#
# * * * * * * * * * * * * * * * * * * * *
def gnuplot(fileName,nLines):
     gnuplotFile = "/tmp/gnuplotFile"
     fh=open(gnuplotFile,'w')
     fh.write("plot ")
     for i in range(1,nLines-1):
          fh.write("'"+fileName+"' using 1:"+str(i+1)+" wi linesp, \\\n")
     fh.write("'"+fileName+"' using 1:"+str(nLines)+" wi linesp\npause 6\n")

     fh.close()
     plotCmd = "gnuplot " + gnuplotFile
     #os.popen(plotCmd)
# * * * * * * * * * * * * * * * * * * * *

# * * * * * * * * * * * * * * * * * * * *
# * * * * * * * * * * * * * * * * * * * *
def shift(v,n):
     N=size(v)
     tmp=v.copy()
     if n < 0:
          n=N+n
     tmp[n:N] = v[0:N-n]
     tmp[0:n]   = v[N-n:N]
     return tmp
# * * * * * * * * * * * * * * * * * * * *
def Dx(v,dx,d):
     N=size(v)-1
     vx = v.copy()
     if d == 0:
          vx = (shift(v,1)-shift(v,-1))/(2*dx)
          vx[N] = (v[1]-v[N-1])/(2*dx)
          vx[0] = vx[N]
     if d == -1:
          #vx = (shift(v,0)-shift(v,-1))/dx
          vx[1:N] = ( v[1:N] - v[0:N-1] )/dx
          vx[0] = (vx[0]-vx[N-1])/dx
     if d == 1:
          #vx = (shift(v,1)-shift(v,0))/dx
          vx[0:N-1] = ( v[0:N-1] - v[1:N] )/dx
          vx[N] = (vx[N]-vx[1])/dx
     return vx

# * * * * * * * * * * * * * * * * * * * *
def Dxx(v,dx):
     vxx = (Dx(v,dx,1)-Dx(v,dx,-1))/dx
     return vxx

# * * * * * * * * * * * * * * * * * * * *
def ENO():
     pass

# * * * * * * * * * * * * * * * * * * * *
def heaviside():
     pass

fileName = "convect.out"
#specify domain
N = 40
t0 = 0.0
t1 = 4.0
x0 = 0.0
x1 = x0+2.0
dx = (x1-x0)/(N-1)

X = array(arange(N)*dx)

u0 = -cos(pi*X)
ux = Dx(u0,dx,-1)
ux2 = Dx(u0,dx,1)

fh = open(fileName,'w')
for i in range(size(X)):
     fh.write(str(X[i])+"\t"+str(u0[i])+"\t"+str(ux[i])+"\t"+str(ux2[i])+"\n")

gnuplot(fileName,4)
g.plot(Gnuplot.Data(X,u0,inline=1))

