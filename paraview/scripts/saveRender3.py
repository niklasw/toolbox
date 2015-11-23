#### import the simple module from the paraview
from paraview.simple import *
import os

def createFileName(rootPath):
    base = 'quickSaveImage'
    if not os.path.isdir(rootPath):
        os.makedirs(rootPath)
    for i in range(100):
        fname = os.path.join(rootPath,'{0}_{1:04d}.png'.format(base,i))
        if os.path.isfile(fname):
            continue
        else:
            return fname

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1512, 796]

# current camera placement for renderView1
### renderView1.InteractionMode = '2D'
### renderView1.CameraPosition = [0.5, 0.5, 3.3]
### renderView1.CameraFocalPoint = [0.5, 0.5, 0.5]
### renderView1.CameraParallelScale = 0.65244769565367

# save screenshot
fileName = createFileName('/home/niklas/tmp/pvQuickImages')
SaveScreenshot(fileName, magnification=2, quality=100, view=renderView1)

#### saving camera placements for all active views

# current camera placement for renderView1
### renderView1.InteractionMode = '2D'
### renderView1.CameraPosition = [0.5, 0.5, 3.3]
### renderView1.CameraFocalPoint = [0.5, 0.5, 0.5]
### renderView1.CameraParallelScale = 0.65244769565367

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
