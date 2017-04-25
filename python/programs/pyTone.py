#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.io import wavfile as wav
from matplotlib import pyplot as plt
from subprocess import Popen,PIPE
import sys

samplingRate=44100

# -----------------------------------------------------------------



notes= { 'C': 261.63*0.5,
         'C#':277.18*0.5,
         'D': 293.66*0.5,
         'D#':311.13*0.5,
         'E': 329.63*0.5,
         'F': 349.23*0.5,
         'F#':369.99*0.5,
         'G': 392*0.5,
         'G#':415.3*0.5,
         'A': 440*0.5,
         'A#':466.16*0.5,
         'B': 493.88*0.5,
         '2C' : 261.63,
         '2C#':277.18,
         '2D' : 293.66,
         '2D#':311.13,
         '2E' : 329.63,
         '2F' : 349.23,
         '2F#':369.99,
         '2G' : 392,
         '2G#':415.3,
         '2A' : 440,
         '2A#':466.16,
         '2B' : 493.88 }


def makeSpectrum(kind,*args):
    if kind == 'notes':
        selection = args[0]
        freqs = []
        tmpTone = []
        for note in selection:
            if note.upper() in notes.keys():
                f = notes[note.upper()]
                print '--> {0}\t{1}'.format(note,f)
                freqs.append(f)
                time,tone = makeTone([f],0.4,samplingRate)
                tmpTone.extend(tone)
            else:
                print "!! Not a valid note: {}".format(note)
                continue
        p=play(tmpTone)
        p.wait()
        return freqs
    elif kind == 'noise':
        import random
        print args
        low = float(args[0][0])
        bandWidth = float(args[0][1])
        freqs = [ low+random.random()*bandWidth for i in range(1000) ]
        return freqs
    elif kind == 'freqs':
        return map(float,args[0])
    else:
        print 'Arg 1 is not "notes", "noise" or "freqs"'
        sys.exit(1)


def makeTone(freqs, toneLength, sr):
    t=np.linspace(0,toneLength,toneLength*sr)
    tone = 0.0*t;

    for frq in freqs:
        tone += np.sin(frq*2*np.pi*t)

    return t,tone

def play(tone,volume=32767):
    def setVolume(tone):
        return np.int16(tone/np.max(np.abs(tone)) * volume)

    wav.write('tone.wav', samplingRate, setVolume(tone))
    return Popen(['aplay','tone.wav'],stdout=PIPE,stderr=PIPE)

def show(time,tone):
    L=len(time)/4
    sec = [ t for t in time if t <= 1.0 ]
    plt.plot(sec,tone[0:len(sec)])
    plt.grid('on')
    plt.show()

def usage():
    print 'Usage: pyTone.py <notes|noise|freqs> <c e g|50 200| 400 440 500>'
    sys.exit(1)

# -----------------------------------------------------------------

try:
    if not sys.argv[1] in ['freqs','notes','noise']:
        usage()
except:
    usage()


freqs = makeSpectrum(sys.argv[1],sys.argv[2:])

time,tone = makeTone(freqs, 4, samplingRate)

play(tone)

show(time,tone)

