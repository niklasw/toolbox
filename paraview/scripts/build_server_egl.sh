#!/bin/bash

[[ -n "$1" ]] || { echo "Must supply version number, e.g. $pvversion"; exit 1; }

pvversion=$1

# module add mpi

cmake ../ParaView-v$pvversion/ \
      -DBUILD_TESTING=OFF -DPARAVIEW_ENABLE_CATALYST=OFF \
      -DPARAVIEW_ENABLE_PYTHON=ON -DCMAKE_BUILD_TYPE=RELEASE \
      -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=OFF -DPARAVIEW_USE_MPI=ON \
      -DVTK_RENDERING_BACKEND=OpenGL2 -DVTK_OPENGL_HAS_EGL=ON \
      -DVTK_USE_X=OFF -DPARAVIEW_BUILD_QT_GUI=OFF \
      -DEGL_LIBRARY=/usr/lib64/libEGL.so.1 \
      -DEGL_opengl_LIBRARY=/usr/lib64/libOpenGL.so \
      -DEGL_INCLUDE_DIR=/usr/include \
      -DCMAKE_INSTALL_PREFIX=/remote/soft2/ParaView/$pvversion-EGL

# [[ $? == 0 ]] && make -j 32
# [[ $? == 0 ]] && make install

