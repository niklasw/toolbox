#!/usr/bin/python

import string,re,sys,os

def usage():
    print '''A tex file is needed as input, with hard coded (h.c.) bibliography;
each item separated by the latex new line "\\\\". 

One need to make each h.c. reference unique by e.g prepending letter in A-E:
    sed -i  '/newcommand/!s/\[\([0-9]*\)\]/\[C\1\]/g' file.tex
'''
    sys.exit(0)

try:
    src=sys.argv[1]
    if not os.path.isfile(src):
        sys.exit(1)
except:
    usage()

quotes='["\'`]'
space='\s*'
index='\[([ABCDEF]?[0-9]+)\]'
start='^.*'
end='.*$'
authors='\s+([A-Z].*);'
year='\s*([1-9][0-9]+)\s*,'

title=space+quotes+'(.*)'+quotes+space+','
journal='(.*)\s*'

refStr=start+index+authors+year+title+'(.*)'+end#+journal+end

print 'Using this regexp to parse hardcoded items\n\t{0}'.format(refStr)

refPat=re.compile(refStr,re.MULTILINE|re.I|re.DOTALL)

document=open(src).read()

refStrList=document.split('\\\\')

foundRefs = {}

for line in refStrList:
    line=re.sub('\n',' ',line)
    match = refPat.match(line)

    if match:
        fields = match.groups()
        fields = ( re.sub('[\'"`]','',a) for a in fields)
        fields = [ re.sub('\n',' ', a) for a in fields]

        i = fields[0]
        foundRefs[i] = fields

bibFileContent = ''
for item,fields in foundRefs.iteritems():
    i,a,y,t,r=fields
    bibFileContent+= '''
@misc{{auto{0},
    author="{{{1}}}",
    year={{{3}}},
    title="{{{2}}}",
    note="{4}"
}}'''.format(i,a,t,y,r)

    document = re.sub('\[\s*{0}\s*\]'.format(i),'\\cite{{auto{0}}}'.format(i),document)

bibFile = src+'.bib'
texFile = src+'.cited'

print '''
Output to be written to
{0}
{1}'''.format(texFile,bibFile)

bh = open(bibFile,'w')
dh = open(texFile,'w')

dh.write(document)
bh.write(bibFileContent)

print '''
Now remember to remove the hard coded reference list
form the produced .cited file. Change the suffix and
read it carefully.

This hack probably failed horribly.
                                             /nikwik
'''
