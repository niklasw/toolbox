#!/usr/bin/env python
#
# To create image arrays each consisting of images with identical names
# that are placed in separate subdirectories
# Directories are parsed for imagenames that exist in all directories.
#
# Depends on ImageMagick
# Author Niklas Wikstrom

from subprocess import Popen
import os,sys,re,string

def Info(s,i='Info'):
    s = '! %s: %s' % (i,s)
    n=len(s)
    #print '\t%s\n\t%s\n\t%s' % (n*'-',s,n*'-')
    print '\n\t%s' % (s)

def Error(s):
    Info(s,'Error')
    sys.exit(1)

prog = os.path.basename(sys.argv[0])
progPath = os.path.dirname(os.path.realpath(sys.argv[0]))

def getArgs():
    from optparse import OptionParser
    descString = """To create image arrays each consisting of images with
identical names that are placed in separate subdirectories Directories are
parsed for imagenames that exist in all directories.
Depends on ImageMagick /Author Niklas Wikstrom"""

    parser=OptionParser(description=descString)
    parser.usage = "%prog <options> <Directories with images>"
    parser.add_option('-r','--rows',dest='rows',default=0, help='Number of rows in image array')
    parser.add_option('-g','--geometry',dest='geometry',default='+2+2',help='ImageMagick geometry string')
    parser.add_option('-f','--format',dest='format',default='png',help='Image format/suffix (png)')
    parser.add_option('-F','--font',dest='font',default='helvetica',help='Font for text (helvetica)')
    parser.add_option('-p','--fontsize',dest='fontsize',default=40,help='Font size for text (40)')
    (opt,args)=parser.parse_args()

    dirs = []
    for arg in args:
        if os.path.isdir(arg):
            dirs.append(arg)

    def validateOption(option, test, msg='Invalid argument'):
        try:    option = test(option)
        except: argError('%s; got %s' % (msg,option))
        return option

    opt.rows = validateOption(opt.rows,int)
    opt.fontsize = validateOption(opt.fontsize,int)
    return opt,dirs

def findCommonImages(dirs,format):
    import re
    imgPat = re.compile('.*\.'+format,re.I)
    s = set( filter(imgPat.match, os.listdir(dirs[0])) )

    for dir in dirs[1:]:
        images = filter(imgPat.match, os.listdir(dir))
        s=s.intersection(images)
    return list (s)


options, dirs = getArgs()

commonImages = findCommonImages(dirs,options.format)

#nColumns = len(dirs)/options.rows+len(commonImages)%options.rows
import math
nColumns = int(math.ceil(float(len(dirs))/options.rows))
tile = '%ix%i'%(nColumns,options.rows)

geometryOpts = ['-tile',tile,'-geometry',options.geometry]

fontOpts     = ['-font',options.font,'-pointsize', str(options.fontsize)]

Info('Base arguments are %s' % string.join(geometryOpts+fontOpts))

montageImagePrefix = 'montage_'

print commonImages

for image in commonImages:
    title = re.sub('[_-]',' ',os.path.splitext(image)[0])
    titleOpts = ['-title',title]

    Info( '%s%s'%(montageImagePrefix,image),i='-->')

    labeledImages = []

    for dir in dirs:
        labeledImages += ['-label',dir,os.path.join(dir,image)]

    p = Popen(['montage']+titleOpts+fontOpts+geometryOpts+labeledImages+[montageImagePrefix+image])
    p.wait()
