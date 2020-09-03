import os
from os.path import join as pjoin
from flask import Flask,url_for
from jinja2 import Template
from template import template
import glob

app = Flask(__name__)

def mkImgPage(imgPaths):
    t = Template(template)
    page = t.render(image     = imgPaths[1], \
                    nextImage = imgPaths[2], \
                    prevImage = imgPaths[0])
    return page

def getImageList(imgPath):
    return [os.path.basename(i) for i in glob.glob(pjoin('static','images','*.jpg'))]

def rotate(L, n):
    return L[n:] + L[:n]

@app.route('/')
def showPage():
    global imageNames

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    imgPaths = [pjoin('images',imageNames[i]) for i in (0,1,2)]

    return mkImgPage([ url_for('static',filename=imgPaths[0]),
                       url_for('static',filename=imgPaths[1]),
                       url_for('static',filename=imgPaths[2])])

@app.route('/backward/',methods=['POST'])
def bwdPage():
    global imageNames
    imageNames = rotate(imageNames,1)
    return showPage()

@app.route('/forward/',methods=['POST'])
def fwdPage():
    global imageNames
    imageNames = rotate(imageNames,-1)
    return showPage()


if __name__ == '__main__':
    imageNames = getImageList(pjoin('static','images'))

    app.run(host="192.168.10.10", port=5000, debug=True)

