include ${POOMA_BUILD_PATH}/linux/lib/Makefile.pooma-gcc

all: mesh

mesh.o: mesh.C
	$(POOMA_CXX) -c \
	$(POOMA_CXX_DBG_ARGS) \
	$(POOMA_C_DBG_ARGS) \
	$(POOMA_INCLUDES) mesh.C

mesh: mesh.o
	$(POOMA_CXX) \
	$(POOMA_INCLUDES) \
	mesh.o -o mesh \
	$(POOMA_LIBS)

clean:
	rm mesh mesh.o
