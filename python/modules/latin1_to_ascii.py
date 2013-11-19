#!/usr/bin/env python
"""
latin1_to_ascii -- The UNICODE Hammer -- AKA "The Stupid American"

This takes a UNICODE string and replaces Latin-1 characters with
something equivalent in 7-bit ASCII. This returns a plain ASCII string. 
This function makes a best effort to convert Latin-1 characters into 
ASCII equivalents. It does not just strip out the Latin1 characters.
All characters in the standard 7-bit ASCII range are preserved. 
In the 8th bit range all the Latin-1 accented letters are converted to 
unaccented equivalents. Most symbol characters are converted to 
something meaningful. Anything not converted is deleted.

Background:

One of my clients gets address data from Europe, but most of their systems 
cannot handle Latin-1 characters. With all due respect to the umlaut,
scharfes s, cedilla, and all the other fine accented characters of Europe, 
all I needed to do was to prepare addresses for a shipping system.
After getting headaches trying to deal with this problem using Python's 
built-in UNICODE support I gave up and decided to use some brute force.
This function converts all accented letters to their unaccented equivalents. 
I realize this is dirty, but for my purposes the mail gets delivered.
"""

def latin1_to_ascii (unicrap):
    """This takes a UNICODE string and replaces Latin-1 characters with
        something equivalent in 7-bit ASCII. It returns a plain ASCII string. 
        This function makes a best effort to convert Latin-1 characters into 
        ASCII equivalents. It does not just strip out the Latin-1 characters.
        All characters in the standard 7-bit ASCII range are preserved. 
        In the 8th bit range all the Latin-1 accented letters are converted 
        to unaccented equivalents. Most symbol characters are converted to 
        something meaningful. Anything not converted is deleted.
    """
    xlate={0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
        0xc6:'Ae', 0xc7:'C',
        0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',
        0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
        0xd0:'Th', 0xd1:'N',
        0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
        0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
        0xdd:'Y', 0xde:'th', 0xdf:'ss',
        0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
        0xe6:'ae', 0xe7:'c',
        0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
        0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
        0xf0:'th', 0xf1:'n',
        0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
        0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
        0xfd:'y', 0xfe:'th', 0xff:'y',
        0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
        0xa5:'{yen}', 0xa6:'|', 0xa7:'{section}', 0xa8:'{umlaut}',
        0xa9:'{C}', 0xaa:'{^a}', 0xab:'<<', 0xac:'{not}',
        0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
        0xb1:'{+/-}', 0xb2:'{^2}', 0xb3:'{^3}', 0xb4:"'",
        0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*', 0xb8:'{cedilla}',
        0xb9:'{^1}', 0xba:'{^o}', 0xbb:'>>', 
        0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}', 0xbf:'?',
        0xd7:'*', 0xf7:'/'
        }

    r = ''
    for i in unicrap:
        if xlate.has_key(ord(i)):
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            r += str(i)
    return r

if __name__ == '__main__':
    s = unicode('','latin-1')
    for c in range(32,256):
        if c != 0x7f:
            s = s + unicode(chr(c),'latin-1')
    plain_ascii = latin1_to_ascii(s)

    print 'INPUT type:', type(s)
    print 'INPUT:'
    print s.encode('latin-1')
    print
    print 'OUTPUT type:', type(plain_ascii)
    print 'OUTPUT:'
    print plain_ascii

