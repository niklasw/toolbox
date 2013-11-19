#!/usr/bin/python
#http://vobject.skyhouseconsulting.com/usage.html

import os,sys,vobject,string

from optparse import OptionParser

def fatal(astring, errno=1):
    print "\nFatal ERROR:\n\t%s\nABORTING" % astring
    sys.exit(errno)

def getArgs():
    descString = """
    Python thing using the module vobject to parse vCards.
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--vCardFile',dest='vcf',help='Iptut vCard file')
    parser.add_option('-o','--output',dest='out',help='Results in this file')
    (options,args) = parser.parse_args()

    vcfFile=options.vcf
    outFile=options.out
    if not vcfFile:
        fatal('Need input vcf file. Run with --help')

    vcfh=file(vcfFile,'r')
    outh=sys.stdout
    if outFile:
        outh=file(outFile,'w')

    return (vcfh,outh)


def mkEmptyVCard(fullName):
    newCard = vobject.vCard()
    newCard.add('n')
    newCard.n.value = vobject.vcard.Name( family=family, given=given )
    newCard.add('fn')
    newCard.fn = string.join([given,family])
    return newCard

def appendContent(card,content,f,type):
    tmp = []
    if not card.has_key(content):
        card.add(content)
    card.f.value = 



def main():
    vcfh,outh=getArgs()

    allCards=vobject.readComponents(vcfh.read())
    vcfh.close()

    nameDict={}
    noNameVCards=[]

    while 1:
        try:
            vcard=allCards.next()
        except:
            break
        if vcard.contents.has_key('n'):
            giv = vcard.n.value.given
            fam = vcard.n.value.family
            fullName = string.join([given,family])

            if not nameDict.has_key(fullName):
                nameDict[fullName] = mkEmptyVCard(fullName)
            
            if vcard.contents.has_key('tel'):
                for item in vcard.contents['tel']:
                    tel=item.value
                    type=item.params['TYPE'][0]
                    nameDict[fullName].
        else:
            noNameVCards.append(vcard)

    for name in nameDict.keys():
        print name, nameDict[name]
    print noNameVCards

main()









