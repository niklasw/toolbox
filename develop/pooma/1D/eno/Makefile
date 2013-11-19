include ${POOMA_BUILD_PATH}/linux/lib/Makefile.pooma-gcc

all: eno

eno.o: eno.cc
	$(POOMA_CXX) -c \
	$(POOMA_CXX_OPT_ARGS) \
	$(POOMA_CC_OPT_ARGS) \
	$(POOMA_INCLUDES) eno.cc

eno: eno.o
	$(POOMA_CXX) \
	$(POOMA_INCLUDES) \
	eno.o -o eno \
	$(POOMA_LIBS)

clean:
	rm eno eno.o
