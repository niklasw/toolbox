from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
from wand.display import display

bg = Color('white')
fg = Color('black')
transp = Color('transparent')

plotImage = Image(filename='/tmp/image.png')
W = plotImage.width
Wext = 800
H = plotImage.height

with Image(width=W+Wext,height=H,background=bg) as output:
    with Image(width=Wext,height=H,background=bg) as img:
        fontsize = int(plotImage.height/30)
        headerSpacing = int(fontsize*2)
        lineSpacing = int(fontsize*1.5)
        boxTop = 97
        boxBottom = 1150
        boxLeft = 80
        lineY = boxTop+lineSpacing
        lineX = boxLeft+40

        canvas = Drawing()
        text = Drawing()
        canvas.stroke_color=fg
        canvas.stroke_width=1
        canvas.fill_color=transp
        canvas.rectangle(left=40,top=boxTop,right=Wext-40,bottom=boxBottom,radius=0)

        text.font_size=fontsize
        text.font='Courier-10-Pitch'
        text.text(lineX,lineY,'Train summary')
        lineY += headerSpacing
        text.text(lineX,lineY,'Length  500 m')
        lineY += lineSpacing
        text.text(lineX,lineY,'Area    500 m')
        lineY += lineSpacing
        text.text(lineX,lineY,'Slope   2.5%')
        lineY += lineSpacing
        text.text(lineX,lineY,'Trafic  double track')
        canvas(img)
        text(img)

        output.composite(image=plotImage,left=0,top=0)
        output.composite(image=img,left=W,top=0)
        output.save(filename='/tmp/composite.png')
