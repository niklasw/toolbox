include ${POOMA_BUILD_PATH}/linux/lib/Makefile.pooma-gcc

all: levelSet

levelSet.o: levelSet.cc
	$(POOMA_CXX) -c \
	$(POOMA_CXX_OPT_ARGS) \
	$(POOMA_CC_OPT_ARGS) \
	$(POOMA_INCLUDES) levelSet.cc

levelSet: levelSet.o
	$(POOMA_CXX) \
	$(POOMA_INCLUDES) \
	levelSet.o -o levelSet \
	$(POOMA_LIBS)

clean:
	rm levelSet levelSet.o
