
EXE = helloIf

CXX = g++

INC_DIRS =

LIBS = -lstdc++fs

SRC  = helloIf.cpp

OBJS = helloIf.o

FLAGS =  -std=c++17

$(EXE): $(OBJS)
	$(CXX) -o helloIf $(OBJS) $(FLAGS)

$(EXE).o: $(SRC)
	$(CXX) $(LIBS) -c $(SRC) -o helloIf.o $(FLAGS)

all: helloIf

clean:
	rm -f $(OBJS) $(EXE)
