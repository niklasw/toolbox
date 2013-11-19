#!/bin/env python

import sys
from xml.dom.ext.reader import Sax2
from xml.dom.ext import Print, PrettyPrint, Node
from xml import xpath
from xml.dom.NodeFilter import NodeFilter

from rpcClasses import *

# Argument handling
if len(sys.argv) != 2:
    print "Usage:",sys.argv[0],"<file.xml>"
    sys.exit(1)

xmlFile = sys.argv[1]

# create Reader object
reader = Sax2.Reader()
# parse the document
doc = reader.fromStream(xmlFile)

rpc = RPC(doc, 'Fry')
rpc.connect()
rpc.setplayer('Nicke')
rpc.addAttribute('styrka','12')
rpc.addAttribute('karisma','16')
rpc.addSkill('Climb','13')
rpc.addWeapon('Long sword','15','1t10+1','really cool sword')
rpc.addItem('blanket','Magic')
rpc.addItem('back pack','Large as hell')
rpc.finish()
rpc.Print()

rpc2 = RPC(doc,'Bettan')
rpc2.new()
rpc2.setplayer('John Doe')
rpc2.addAttribute('styrka','12')
rpc2.addAttribute('karisma','16')
rpc2.addSkill('Climb','13')
rpc2.addWeapon('Battle sword','15','1t10+1','really cool sword')
rpc2.addWeapon('Tiny sword','15','1','rather flimsy sword')
rpc2.addItem('blanket','Magic')
rpc2.addItem('back pack','Large')
rpc2.finish()
rpc2.Print()

PrettyPrint(doc)
