#!/bin/bash

[[ -n "$1" ]] || { echo "Must supply version number, e.g. $pvversion"; exit 1; }

pvversion=$1

module add mpi

      #-DEGL_INCLUDE_DIR=/usr/include \
      #-DEGL_LIBRARY=/usr/lib64/libEGL_mesa.so.0\
      #-DEGL_opengl_LIBRARY=/usr/lib64/libOpenGL.so \
      #-DVTK_USE_OFFSCREEN_EGL=ON \
      #-DVTK_EGL_DEVICE_INDEX=??
cmake ../ParaView-$pvversion/ \
      -DOPENGL_INCLUDE_DIR=/usr/include \
      -DOSMESA_INCLUDE_DIR=/usr/include/GL \
      -DOSMESA_LIBRARY=/usr/lib64/libOSMesa.so \
      -DBUILD_TESTING=OFF \
      -DPARAVIEW_USE_PYTHON=ON \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DPARAVIEW_USE_MPI=ON \
      -DVTKm_ENABLE_MPI=ON \
      -DVTK_MPI_NUMPROCS=16 \
      -DVTK_RENDERING_BACKEND=OpenGL2 \
      -DVTK_OPENGL_HAS_EGL=OFF \
      -DVTK_OPENGL_HAS_OSMESA=ON \
      -DVTK_USE_X=OFF \
      -DPARAVIEW_USE_QT=OFF \
      -DOPENGL_gl_LIBRARY=/usr/lib64/libGL.so \
      -DOPENGL_glu_LIBRARY=/usr/lib64/libGLU.so \
      -DCMAKE_INSTALL_PREFIX=/home/software/ParaView/server-git \
      -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=OFF

[[ $? == 0 ]] && make -j 32
[[ $? == 0 ]] && make install

