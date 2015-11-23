#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
# find source
source = GetActiveSource()

rView = GetRenderView()

Hide(source, rView)

for i in range(10,2,-1):
    extractBlock = ExtractBlock(Input=source)
    try:
        extractBlock.BlockIndices = [i]
        extractBlockDisplay = Show(extractBlock, rView)
    except:
        continue

SetActiveSource(source)

