#!/usr/bin/env python3

import numpy as np

def get_quaternion(lst1,lst2,matchlist=None):
    if not matchlist:
        matchlist=range(len(lst1))
    M=np.matrix([[0,0,0],[0,0,0],[0,0,0]])

    for i,coord1 in enumerate(lst1):
        x=np.matrix(np.outer(coord1,lst2[matchlist[i]]))
        M=M+x

    N11=float(M[0][:,0]+M[1][:,1]+M[2][:,2])
    N22=float(M[0][:,0]-M[1][:,1]-M[2][:,2])
    N33=float(-M[0][:,0]+M[1][:,1]-M[2][:,2])
    N44=float(-M[0][:,0]-M[1][:,1]+M[2][:,2])
    N12=float(M[1][:,2]-M[2][:,1])
    N13=float(M[2][:,0]-M[0][:,2])
    N14=float(M[0][:,1]-M[1][:,0])
    N21=float(N12)
    N23=float(M[0][:,1]+M[1][:,0])
    N24=float(M[2][:,0]+M[0][:,2])
    N31=float(N13)
    N32=float(N23)
    N34=float(M[1][:,2]+M[2][:,1])
    N41=float(N14)
    N42=float(N24)
    N43=float(N34)

    N=np.matrix([[N11,N12,N13,N14],\
              [N21,N22,N23,N24],\
              [N31,N32,N33,N34],\
              [N41,N42,N43,N44]])


    values,vectors=np.linalg.eig(N)
    w=list(values)
    mw=max(w)
    quat= vectors[:,w.index(mw)]
    #quat=np.array(quat).reshape(-1,).tolist()
    return quat

if __name__ == '__main__':
    c1 = [np.array(v) for v in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
    c2 = [np.array(v) for v in [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]]
    Q = get_quaternion(c1, c2)
    print(Q)

