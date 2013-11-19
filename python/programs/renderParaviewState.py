#!/usr/bin/env pvpython

import os,sys
try:
    from paraview import servermanager
except:
    print 'Paraview API not found'
    sys.exit(1)

def getArgs():
    from optparse import OptionParser
    descString = """
    Python thing relying on the paraview API to generate image from state file
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--state',dest='pvsm',default=None,help='Input state file')
    parser.add_option('-o','--image',dest='image',default=None,help='Output image file. PNG only!')
    parser.add_option('-S','--server',dest='server',default=None,help='NOT WORKING. pvserver host. server must be running!')

    (opt,arg)=parser.parse_args()

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)


    if not opt.pvsm:
        argError('Missing state file argument')

    if not opt.image:
        argError('Missing image file argument')

    stateFile = opt.pvsm
    imageName, imageExt = os.path.splitext(opt.image)
    imageFile = imageName+'.png'

    argDict = {'stateFile':stateFile,
               'imageFile':imageFile,
               'pvserver':opt.server}
    return argDict

def main():

    args = getArgs()
    pvsm = args['stateFile']
    image = args['imageFile']
    server = args['pvserver']

    imageBase,imageExt=os.path.splitext(image)

    if server:
        servermanager.Connect(server,11111)
    else:
        servermanager.Connect()

    servermanager.LoadState(pvsm)

    views = servermanager.GetRenderViews()

    for i,view in enumerate(views):
        view.Background = [1,1,1]
        viewImage = 'view'+str(i)+'_'+imageBase+imageExt
        view.WriteImage(viewImage,'vtkPNGWriter',1)

if __name__=='__main__':
    main()

