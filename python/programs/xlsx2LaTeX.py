#!/usr/bin/env python

import os,sys,re,string

def Info(s,i='Info'):
    s = '! %s: %s' % (i,s)
    n=len(s)
    print '\n\t%s' % (s)

def Error(s):
    Info(s,'Error')
    print ''
    sys.exit(1)


def getArgs():
    from optparse import OptionParser
    descString = '''Extract ranges of columns and rows from an
xlsx file and write in LaTeX table format.
Columns are limited to A-ZZ, Rows are limited to 0-1000.
Example Options: -f myFile.xlsx -R 1,4:10 -C "A,D:G,AZ --pretty"
    '''

    parser=OptionParser(description=descString)
    parser.add_option('-f','--file',dest='xlsx',default=None,help='.xlsx input')
    parser.add_option('-o','--output',dest='tex',default=None,help='.tex output')
    parser.add_option('-C','--columns',dest='columns',default='',help='Column range to use, as "A,C:G,AC:AG"')
    parser.add_option('-R','--rows',dest='rows',default='',help='Row range to use, as "1,2:8"')
    parser.add_option('-S','--sheet',dest='sheet',default='Sheet1',help='Name of sheet in xlsx file.')
    parser.add_option('-p','--precision',dest='precision',default=2,help='Numeric precision for ALL! floats.')
    parser.add_option('-P','--pretty',dest='pretty',action='store_true',default=False,help='Try to print pretty table')
    (opt,arg)=parser.parse_args()

    alphabet = map(chr, range(65, 91))
    doubleAlphabet = list(alphabet)
    for c in alphabet:
        doubleAlphabet += [ c+a for a in alphabet ]

    charMap = dict( zip(doubleAlphabet, range(len(doubleAlphabet))) )
    intMap  = dict( zip(map(str, range(1,1001)),range(0,1000)) )

    def argError(s):
        parser.print_help()
        Error(s)

    def charRangeToIntList(charRange, mapHash):
        columns = set()
        ranges = charRange.split(',')
        for r in ranges:
            if r in doubleAlphabet:
                columns.add(mapHash[r])
            else:
                if ':' in r:
                    begin,end = r.split(':')
                    columns = columns.union(sorted(mapHash.values())[mapHash[begin]:mapHash[end]+1])
                else:
                    columns.add(mapHash[r])
        return list(sorted(columns))

    if not opt.xlsx or not os.path.isfile(opt.xlsx):
        argError('Missing .xlsx input file')

    if not opt.tex:
        opt.tex = os.path.splitext(opt.xlsx)[0]+'.tex'

    if opt.columns:
        try:
            opt.columns = charRangeToIntList(opt.columns.upper(),charMap)
        except:
            argError('Could not parse column range %s' % opt.columns)
    if opt.rows:
        try:
            opt.rows = charRangeToIntList(opt.rows,intMap)
        except ValueError as e:
            print e
            argError('Could not parse row range %s' % opt.rows)

    try:
        opt.precision = int(opt.precision)
    except:
        argError('--precision must be integer')

    return opt

def tableStart(nCols,alignment='c'):
    str = string.join([
    '\\begin{table}',
    '\\caption{My table}\n'
    '\\begin{tabular*}{\\textwidth}{%s} \\toprule\n'% ('l'+(nCols-1)*alignment)],
    '\n')
    return str

def tableEnd():
    str='\\bottomrule\n\\end{tabular*}\n\\label{tab:}\n\\end{table}\n'
    return str

def xlsxToArray(fileName,sheetName='Sheet1',columns=None,rows=None):
    try:
        from openpyxl.reader.excel import load_workbook
    except:
        Error( "This program rely on the python module openpyxl for excel parsing" )
    wb = load_workbook(filename=fileName,read_only=True,data_only=True)
    if not sheetName in wb.get_sheet_names():
        Error( 'Could not open sheet named %s' % sheetName)
        sys.exit(1)
    sheet = wb.get_sheet_by_name(name=sheetName)


    sheetArray = []
    nCols = len(columns)

    for row in rows:
        sheetRow = list(sheet.rows)[row]
        rowList = [ a.value for i,a in enumerate(sheetRow) if i in columns ]
        sheetArray.append(rowList)
    return sheetArray

def arrayToLatexTable(sheetArray,precision=2,colSep = '&'):
    newLines = []
    nCols = len(sheetArray[0])

    def roundFloat(f,prec):
        if isinstance(f,float):
            if prec < 0:
                f = round(f,prec)
                prec = 0
            fmt = '%0.'+str(prec)+'f'
        elif isinstance(f,int):
            fmt = '%i'
        else:
            fmt = '%s'
        return fmt%f

    rnd = lambda f : roundFloat(f,precision)

    for rowList in sheetArray:
        rowString = string.join(map(rnd,rowList),separator) + '  \\\\'
        newLines.append(rowString)

    return nCols,newLines

if __name__=="__main__":
    options = getArgs()

    outFile = open(options.tex,'w')

    separator = ' & '
    if options.pretty:
        # Since pretty printing using unix program 'column', we need
        # and extra character to split columns with.
        separator = '|& '

    sheetArray  = xlsxToArray(options.xlsx,columns=options.columns,rows=options.rows,sheetName=options.sheet)
    nCols,lines = arrayToLatexTable(sheetArray, precision=options.precision, colSep=separator)

    outFile.write( tableStart(nCols) )

    for line in lines:
        outFile.write('%s\n'%(line))

    outFile.write( tableEnd() )

    outFile.close()

    if options.pretty:
        # Call unix program 'column' to reorganize the table
        # Simply read the created output file, columnize it an
        # rewrite it. Ugly? Yes.
        from subprocess import Popen, PIPE

        p = Popen(['column','-t','-s','|',options.tex],stdout=PIPE,stderr=PIPE)
        out,err = p.communicate()
        outFile = open(options.tex,'w')
        outFile.write(out)
        outFile.close()

    Info( 'Wrote LaTeX table to %s\n' % (options.tex))

