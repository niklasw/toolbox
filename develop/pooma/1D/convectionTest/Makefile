include ${POOMA_BUILD_PATH}/linux/lib/Makefile.pooma-gcc

all: convect

convect.o: convect.cc
	$(POOMA_CXX) -c \
	$(POOMA_CXX_OPT_ARGS) \
	$(POOMA_CC_OPT_ARGS) \
	$(POOMA_INCLUDES) convect.cc

convect: convect.o
	$(POOMA_CXX) \
	$(POOMA_INCLUDES) \
	convect.o -o convect \
	$(POOMA_LIBS)

clean:
	rm convect convect.o
