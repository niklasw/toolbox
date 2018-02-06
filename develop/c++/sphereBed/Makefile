APP=spheres
CC=g++

QT_HOME=/remote/soft/Qt/5.9.1/5.9.1/gcc_64/

INCLUDES = -I. -I$(QT_HOME)/include
CPPFLAGS = -fPIC -O2
LDFLAGS  =  -lGL -lpthread -L$(QT_HOME)/lib -lQt5Charts -lQt5Gui -lQt5Core -lQt5Widgets

SRC = sphere.cpp material.cpp bed.cpp main.cpp # qtPlot.cpp
OBJ = $(subst .cpp,.o,$(SRC))


%.o: %.cpp
	$(CC) -c $(INCLUDES)  main.cpp $(CPPFLAGS) $<

all: $(OBJ)
	$(CC) $(LDFLAGS) -o $(APP) $(OBJ)



clean:
	rm -f $(OBJ)

distclean: clean
	rm -f $(APP)
