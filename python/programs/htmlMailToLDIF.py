#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os,sys,re
from string import Template


def template():
    ts="""
objectclass: top
objectclass: person
givenName: $NAME
sn: $SURNAME
cn: $SURNAME $NAME
mail: $PRIMARYMAIL
telephoneNumber: $MOBILE
"""
    return Template(ts)

def parseHtml(fileName):
    pat = re.compile(r'face="helvetica,arial">\s*?(.*?)\s&nbsp;.*<a\s*href="mailto:(.*?)"')
    out = []
    with open(fileName,'r') as fp:
        for line in fp:
            match = pat.search(line)
            if match:
                yield (match.group(1).strip(), match.group(2).strip())


if __name__=="__main__":
    htmlFile = sys.argv[1]

    result = parseHtml(htmlFile)
    with open('FOI.ldif','w') as fp:
        for item in result:
            t = template()
            names = item[0].split()
            name = names[1]
            surname = names[0]
            entry = t.safe_substitute(NAME=name,SURNAME=surname,PRIMARYMAIL=item[1],MOBILE='')
            fp.write(entry+'\n')




