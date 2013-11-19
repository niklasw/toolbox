
class Coord(list):
    def __init__(self,coord=[0,0,0]):
        list.__init__(self,coord)
        self.x = float(coord[0])
        self.y = float(coord[1])
        self.z = float(coord[2])
    def __str__(self):
        return '(%f %f %f)' % (self.x,self.y,self.z)

class Node(Coord):
    def __init__(self, coords=[0,0,0], index=-1):
        Coord.__init__(self,coords)
        self.co = Coord(coords)
        self.index = index
    def __str__(self):
        return '(%f %f %f) // %i' % (self.x, self.y, self.z, self.index)

class NodeList(list):
    def __init__(self,l=[]):
        list.__init__(self,l)

    def __str__(self):
        for item in self:
            return str(item)+'\n'

    def sorted(self,dir,rev=False):
        import operator
        return NodeList(sorted(self,key=operator.attrgetter(dir),reverse=rev))

import sys
dir=sys.argv[1]


li = NodeList()
import random, operator
r = random.Random()
for i in range(8):
    no = Node([i*a for a in [r.random(),r.random(),r.random()]],i)
    li.append(no)

li2=li.sorted('x')
print li2.__class__
li2[0:4]=NodeList(li[0:4]).sorted(dir)
for n in li:
    print n
print '--------------'
for n in li2:
    print n


