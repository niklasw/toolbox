#!/usr/bin/python

import math
from interactor2 import interactor

if __name__=='__main__':
    i=interactor()

    nCores = i.get('Number of cores', test=int, default=1)
    nCells = i.get('Number of cells', test=float, default=10000)
    cTime  = i.get('Elapsed time', test=float, default=1000)
    nSteps = i.get('Number of iterations/time steps', test=int, default=100)


    i.info('\n{0}\n'.format('='*50))
    i.info('Simulation speed index = {0:0.1f} "cell-iterations per core-second".'.format(nSteps*nCells/(nCores*cTime)))

    i.info('')


