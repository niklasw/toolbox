#!/usr/bin/env python3

listSize = 107
chunkSize = 20

theList = list(range(listSize))

# Yttersta parenteserna här (...) betyder att slicedList är en
# "generator" (iterator). Den är effektiv att loopa över,
# men saknar index-operator []. 
sliceGenerator = ( theList[i:i+chunkSize] for i in range(0, len(theList), chunkSize) )

# Eller samma sak som en ny lista av listor, men den allokerar mer minne
sliceList      = [ theList[i:i+chunkSize] for i in range(0, len(theList), chunkSize) ]

for chunk in sliceGenerator:
    print(len(chunk),': ', chunk)
