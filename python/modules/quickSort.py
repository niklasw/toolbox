#!/usr/bin/python

def quicksort(lst):
    if len(lst) == 0:
        return []
    else:
        return quicksort([x for x in lst[1:] if x < lst[0]]) + \
               [lst[0]] + quicksort([x for x in lst[1:] if x >= lst[0]])

def checkArgs(alist):
    if len(sys.argv) > 1:
        try:
            nvals = int(sys.argv[1])
            return nvals
        except:
            print "No valid input, using 10"
    return 10

if __name__=='__main__':
    import random,sys
    nvals=checkArgs(sys.argv)

    unsorted=[random.random() for i in range(nvals)]
    sorted=quicksort(unsorted)

    for i,unsrt in enumerate(unsorted): #formatted output
        print '%20.14f %20.14f' % (unsrt, sorted[i])


