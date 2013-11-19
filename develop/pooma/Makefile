include ${POOMA_BUILD_PATH}/linux/lib/Makefile.pooma-gcc

all: first

first.o: first.cc
	$(POOMA_CXX) -c \
	$(POOMA_CXX_OPT_ARGS) \
	$(POOMA_CC_OPT_ARGS) \
	$(POOMA_INCLUDES) first.cc

first: first.o
	$(POOMA_CXX) \
	$(POOMA_INCLUDES) \
	first.o -o first \
	$(POOMA_LIBS)

clean:
	rm first first.o
