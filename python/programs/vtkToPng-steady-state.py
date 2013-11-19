import xml.dom.minidom
import xml.dom.ext
import glob
import sys

from paraview.simple import *

def process_state(statefile,stateroot, casefile, caseroot):

    document = xml.dom.minidom.parse(statefile)

    #Update filename
    for i in document.getElementsByTagName('Property'):
        if i.getAttribute('name')=="FileNameInfo":
            for k in i.getElementsByTagName('Element'):
                k.setAttribute('value', glob.glob(casefile+'/VTK/*.vtk')[0])
                print k.getAttribute('value')

        elif i.getAttribute('name')=="FileNames":
            for k in i.getElementsByTagName('Element'):
                k.setAttribute('value', glob.glob(casefile+'/VTK/*.vtk')[0])
                print k.getAttribute('value')


    file_object = open('tmp/tmp.pvsm', "w")
    xml.dom.ext.PrettyPrint(document, file_object)
    file_object.close()

def generate_png(statefile,stateroot,casefile,caseroot,postroot):

    print statefile
    print casefile

    process_state(statefile,stateroot,casefile,caseroot)

    servermanager.Connect()
    servermanager.LoadState('tmp/tmp.pvsm')
    view=GetRenderView()
    view.Background=[0,0,0]
    view.ViewSize=[2998,1822]
    global a
    prefix=statefile[::-1].split('/')[0][::-1].split(".")[0]
    view.StillRender()
    imgfile = postroot+prefix+"-%04d.png" % a
    print imgfile
    view.WriteImage(imgfile, "vtkPNGWriter", 1)
    a+=1

    servermanager.Disconnect()

def matrix(state,stateroot,cases,caseroot,postroot):
    global a
    a=1
    for case in cases:
        generate_png(state,stateroot, case,caseroot,postroot)

def main(argv):
    caseroot=argv[0]
    state=argv[1]
    stateroot='.'
    postroot='.'
    #postroot='./'
    a = 1
    cases=glob.glob(caseroot+'[1-9]*')
    cases.sort(lambda a,b: cmp(int(a[::-1].split('/')[0][::-1]),  int(b[::-1].split('/')[0][::-1])))
    print cases
    for i in cases:
        print i
    #states=glob.glob(stateroot+'*.pvsm')
    #states.sort()
    print state
    matrix(state,stateroot, cases, caseroot,postroot)

if __name__ == "__main__":
    print sys.argv
    main(sys.argv[1:])
