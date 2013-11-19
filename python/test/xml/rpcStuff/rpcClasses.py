#!/bin/env python

import sys
from xml.dom.ext.reader import Sax2
from xml.dom.ext import Print, PrettyPrint, Node
from xml import xpath
from xml.dom.NodeFilter import NodeFilter

def errorInParser(astring):
    print 'FATAL ERROR: ',astring
    sys.exit(0)

class RPC:
    def __init__(self,db,name):
        self.db = db
        self.name = name
        self.player = ''
        self.dmaster = ''
        self.group = ''
        self.node = Node
        self.attpath = 'attributes'
        self.skillpath = 'skills'
        self.weaponpath = 'weapons'
        self.equipmentpath = 'equipment'

    def Print(self):
        PrettyPrint(self.node)

    def new(self):
        rpcN = self.db.createElement('rpc')
        rpcN.setAttribute('rpcName',self.name)
        attN = self.db.createElement('attributes')
        wpnN = self.db.createElement('weapons')
        skillsN = self.db.createElement('skills')
        eqN = self.db.createElement('equipment')
        rpcN.setAttribute('player','nn')
        rpcN.setAttribute('rpcName','nn')
        rpcN.setAttribute('dmaster','nn')
        rpcN.appendChild(attN)
        rpcN.appendChild(wpnN)
        rpcN.appendChild(skillsN)
        rpcN.appendChild(eqN)
        self.node = rpcN

    def connect(self):
        for node in self.db.getElementsByTagName('rpc'):
            if node.getAttribute('rpcName') == self.name:
                self.node = node
        self.player = self.node.getAttribute('player')
        self.dmaster = self.node.getAttribute('dmaster')

    def setplayer(self,playerName):
        self.player = playerName

    def setgroup(self,groupName):
        self.group = groupName

    def finish(self):
        self.node.setAttribute('rpcName',self.name)
        self.node.setAttribute('player',self.player)
        self.node.setAttribute('dmaster',self.dmaster)

    def addSkill(self,skillName,skillValue,type='a'):
        skillNameN = self.db.createElement('skill')
        skillNameN.setAttribute('name',skillName)
        skillNameN.appendChild(self.db.createTextNode(skillValue))
        xpath.Evaluate('skills', self.node)[0].appendChild(skillNameN)

    def addAttribute(self,att,value='0'):
        attributeN = self.db.createElement('attribute')
        attributeN.setAttribute('name',att)
        attributeN.appendChild(self.db.createTextNode(value))
        xpath.Evaluate(self.attpath, self.node)[0].appendChild(attributeN)

    def setAttribute(self,att,value):
        xp = self.attpath+'/'+att
        xpath.Evaluate(xp,self.node)[0].childNodes[0].data = value

    def addWeapon(self,weaponName,weaponSkillValue,weaponDamage,comment=''):
        doc = self.db
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
        xpath.Evaluate(self.weaponpath, self.node)[0].appendChild(weaponN)

    def remove(tagName,attName,att):
        for node in self.node.getElementByTagName(tagName):
            if node.getAttribute(attName) == att:
                pass

    def addItem(self,itemName,comment=''):
        itemN = self.db.createElement('item')
        itemN.setAttribute('name',itemName)
        itemN.appendChild(self.db.createTextNode(comment))
        xpath.Evaluate(self.equipmentpath,self.node)[0].appendChild(itemN)

    def node(self):
        return self.node

    def clone(self,org):
        self.node = org.clone(1)

