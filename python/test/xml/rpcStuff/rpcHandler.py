#!/bin/env python
import sys
from xml.dom.ext.reader import Sax2
from xml.dom.ext import Print, PrettyPrint, Node
from xml import xpath
from xml.dom.NodeFilter import NodeFilter

# Argument handling
if len(sys.argv) != 2:
    print "Usage:",sys.argv[0],"<file.xml>"
    sys.exit(1)

xmlFile = sys.argv[1]

# create Reader object
reader = Sax2.Reader()
# parse the document
doc = reader.fromStream(xmlFile)

walker = doc.createTreeWalker(doc.documentElement, NodeFilter.SHOW_TEXT, None, 0)

while 1:
    print walker.currentNode
    next = walker.nextNode()
    if next is None: break

def errorInParser(astring):
    print 'FATAL ERROR: ',astring
    sys.exit(0)

def getRpcByName(name):
    for node in doc.getElementsByTagName('rpc'):
        if node.getAttribute('rpcName') == name:
            return node
    errorInParser('getRpcByName')

def getRpcByPlayer(name):
    for node in doc.getElementsByTagName('rpc'):
        if node.getAttribute('player') == name:
            return node
    errorInParser('getRpcByPlayer')

def addAttribute(rpcName, att,value='0'):
    attributeN = doc.createElement('attribute')
    attributeN.setAttribute('name',att)
    attributeN.appendChild(doc.createTextNode(value))
    rpcNode = getRpcByName(rpcName)
    xpath.Evaluate('attributes', rpcNode)[0].appendChild(attributeN)
    return

def getAttributeNode(rpcName, att):
    rpcNode = getRpcByName(rpcName)
    attributesN = xpath.Evaluate('attributes',rpcNode)[0].childNodes
    for node in attributesN:
        print node.data
        if node.getAttribute('name') == att:
            return out
    errorInParser('getAttributeNode')

def readAttributeValue(rpcName,att):
    node = getAttributeNode(rpcName, att)
    return node.firstChild

def setRpcAttribute(rpcName,att,value):
    rpcNode = getRpcByName(rpcName)
    xp = 'attributes/'+att
    xpath.Evaluate(xp, rpcNode)[0].childNodes[0].data = value

def increaseRpcAttribute(rpcName,att,incr):
    value = int(getRpcAttribute(rpcName,att))
    value += int(incr)
    setRpcAttribute(rpcName,att,str(value))

def addSkill(rpcName,skillName,skillValue,type='a'):
    skillNameN = doc.createElement('skill')
    skillNameN.setAttribute('name',skillName)
    skillNameN.appendChild(doc.createTextNode(skillValue))
    rpcNode = getRpcByName(rpcName)
    xpath.Evaluate('skills', rpcNode)[0].appendChild(skillNameN)

def addWeapon(rpcName,weaponName,weaponSkillValue,weaponDamage,comment=''):
    rpcNode = getRpcByName(rpcName)
    weaponN = doc.createElement('weapon')
    weaponN.setAttribute('name',weaponName)
    skillN = doc.createElement('skill')
    skillN.appendChild(doc.createTextNode(weaponSkillValue))
    damageN = doc.createElement('dmg')
    damageN.appendChild(doc.createTextNode(weaponDamage))
    commentN = doc.createElement('comment')
    commentN.appendChild(doc.createTextNode(comment))
    weaponN.appendChild(skillN)
    weaponN.appendChild(damageN)
    weaponN.appendChild(commentN)
    xp = 'weapons'
    xpath.Evaluate(xp, rpcNode)[0].appendChild(weaponN)

def removeWeapon(rpcName,weaponName):
    rpcNode = getRpcByName(rpcName)
    xp = 'weapons'
    weaponRoot = xpath.Evaluate(xp,rpcNode)[0]
    for weapon in weaponRoot.getElementsByTagName('weapon'):
    #    if node.getAttribute('name') == weaponName:
        pass
        print weapon

addAttribute('Fry','sty','15')
#print readAttributeValue('Fry','sty')
setRpcAttribute('Bender','strength','-3')
addSkill('Fry','Climb','10')
addSkill('Bender','Cooking','15')
addSkill('Bender','Hiding','15')
addWeapon('Bender','Axe','14','3t6')
addWeapon('Fry','knife','5','1t6')
removeWeapon('Bender','Battle Axe')
PrettyPrint(doc)


