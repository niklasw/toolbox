#!/bin/bash
# Just to remember the steps, albeit not too many...

(
    cd c-stuff/
    g++ -shared -fPIC -o ../libfunctions.so functions.cpp
)

sbcl --script alien-routine.lisp
