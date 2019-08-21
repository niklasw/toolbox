CXX=g++

CXX_OPT_ARGS=-Wno-deprecated

VTK_LIB_ROOT=/usr/lib64/vtk
VTK_INCLUDE=/usr/include/vtk

INCLUDES=-I$(VTK_INCLUDE)/Rendering \
         -I$(VTK_INCLUDE) \
         -I$(VTK_INCLUDE)/Graphics \
         -I$(VTK_INCLUDE)/Common \
         -I$(VTK_INCLUDE)/Filtering 
SOLIBS=-L$(VTK_LIB_ROOT) -lvtkRenderingCore
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
