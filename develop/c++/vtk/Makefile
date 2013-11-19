CXX=g++

CXX_OPT_ARGS=-Wno-deprecated

VTK_ROOT=/usr/lib

INCLUDES=-I$(VTK_ROOT)/Rendering \
         -I$(VTK_ROOT) \
         -I$(VTK_ROOT)/Graphics \
         -I$(VTK_ROOT)/Common \
         -I$(VTK_ROOT)/Filtering 
SOLIBS=-L$(VTK_ROOT)/bin -lvtkRendering -lvtkGraphics -lvtkCommon -lvtkFiltering
all: sphere

sphere.o: sphere.C
	$(CXX) -c \
	$(CXX_OPT_ARGS) \
	$(INCLUDES) sphere.C

sphere: sphere.o
	$(CXX) \
	$(INCLUDES) \
	$(SOLIBS) \
	sphere.o -o sphere \
	$(LIBS)

clean:
	rm sphere sphere.o
