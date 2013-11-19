#!/usr/bin/python

import sre

vectorpat=sre.compile(r"""^\s*
                          \(\s*
                                (\s*\d*[.]?\d*){3,3}
                          \s*\)
                          \s*$""",sre.VERBOSE)
parenpat=sre.compile(r'(\(|\))')

def wordpat(astring):
    return sre.compile(r'^\s*'+astring+'\s*([//].*)?$')

