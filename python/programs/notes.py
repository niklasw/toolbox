#!/usr/bin/env python

import sys

def noteToFreq(note, fA = 440):
    noteIndices = [0,2,4,5,7,9]
    notes = 'cdefgah'
    if not note in notes:
        print 'Note not a note'
        sys.exit(1)
    indexMap = dict(zip(notes,noteIndices))
    f = fA*pow(2,1./12.)**(indexMap[note]-9)
    return f

note = sys.argv[1].lower()

print noteToFreq(note)



