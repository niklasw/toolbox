#!/usr/bin/python

def interpolatedDataSet(sourcePoints,sourceData,interpolationPoints):
    from scipy import interpolate,asarray
    # Source and interpolatoin points in ascending order!
    oldp=-1e9
    for p in sourcePoints:
        if not p > oldp:
            sp=list(sourcePoints)
            sd=list(sourceData)
            sp.reverse()
            sd.reverse()
            sourcePoints=asarray(sp)
            sourceData=asarray(sd)
            break
        oldp=p
    spline=interpolate.splrep(sourcePoints,sourceData)
    return interpolate.splev(interpolationPoints,spline)

def test(nByTwoData,nPoints):
    from pylab import plot,show
    from scipy import linspace
    data=nByTwoData
    x=list(data[:,0])
    cp=list(data[:,1])
    x2=linspace(min(x),max(x),nPoints)

    cp2=interpolatedDataSet(x,cp,x2)
    plot(x,cp,'g-o',x2,cp2,'r')
    show()

if __name__=="__main__":
    import sys
    from pylab import load
    datafile=sys.argv[1]
    data=load(datafile)
    test(data,100)


