#!/usr/bin/env python3
import os
from os.path import join as pjoin
from flask import Flask,url_for,render_template
import glob


app = Flask(__name__)

def mkImgPage(imgPaths):
    page = render_template('main.html', \
                    image     = imgPaths[1], \
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

@app.route('/backward/',methods=['GET','POST'])
def bwdPage():
    global imageNames
    imageNames = rotate(imageNames,1)
    return showPage()

@app.route('/forward/',methods=['GET','POST'])
def fwdPage():
    global imageNames
    imageNames = rotate(imageNames,-1)
    return showPage()

# Testing plot with pyplot
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

@app.route('/myplot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    from random import randint
    fig = Figure(figsize=(10,4))
    fig.patch.set_alpha(0.0)
    axis = fig.add_subplot(1, 1, 1)
    axis.patch.set_alpha(0.0)
    axis.grid(True, color='#444444')
    axis.set_title('Random plot to test direct rendering', color='orange')
    xs = range(1000)
    ys = [randint(1, 50) for x in xs]
    axis.plot(xs, ys, color='orange')
    return fig


# Test socketio
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

if __name__ == '__main__':
    imageNames = getImageList(pjoin('static','images'))

    #app.run(host="127.0.0.1", port=5000, debug=True)
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)

