#!/usr/bin/python


import sys,os

ext="_ext"

def interactor(astring,f,default=""):
    prompt="%s [%s]" % (astring, default)
    sys.stdout.write(prompt+": ")
    out = sys.stdin.readline().strip()
    if out=="":
        out=default

    try:
        checked=f(out)
    except:
        sys.stdout.write("\nType error:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          