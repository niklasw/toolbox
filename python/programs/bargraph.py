#!/usr/bin/env python

from pylab import *

def main():  
    labels=['A','B','C','D']
    g=lambda x:x/0.00108483
    values=map(g,[0.000308818, 0.0003349328, 0.000283932, 0.00019002])
    bar_graph(labels,values, graph_title='Drag per unit length [N/m]')


def bar_graph(labels,values, graph_title='', output_name='bargraph.png'):
    figure(figsize=(6, 4)) # image dimensions  
    title(graph_title, size='xx-large')
   
    # add bars
    for i, y in enumerate(values):
        bar(i + 0.40 , y, color='orange',width=0.5)
   
    # axis setup
    xticks(arange(0.65, len(labels)), [ str(name) for name in labels],size='xx-large')
    tick_range = arange(0, 4e-1, (1e-1))
    yticks(tick_range, size='xx-large')
    formatter = FixedFormatter([str(x) for x in tick_range])
    gca().yaxis.set_major_formatter(formatter)
    gca().yaxis.grid(which='major')
   
    savefig(output_name)


if __name__ == "__main__":
    main()



