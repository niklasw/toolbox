#!/bin/bash

[[ -n "$1" ]] || { echo "Must supply version number, e.g. $pvversion"; exit 1; }

pvversion=$1

# module add mpi

cmake ../ParaView-v$pvversion/ \
      -DBUILD_TESTING=OFF -DPARAVIEW_ENABLE_CATALYST=OFF \
      -DPARAVIEW_ENABLE_PYTHON=ON -DCMAKE_BUILD_TYPE=RELEASE \
      -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=OFF -DPARAVIEW_USE_MPI=ON \
      -DVTK_RENDERING_BACKEND=OpenGL2 -DVTK_USE_OFFSCREEN_EGL=OFF \
      -DVTK_USE_X=ON -DPARAVIEW_BUILD_QT_GUI=ON \
      -DCMAKE_INSTALL_PREFIX=/remote/soft2/ParaView/$pvversion \
      -DOpenGL_GL_PREFERENCE=GLVND \
      -DQt5_DIR=/remote/soft2/Qt/5.10.1/lib/cmake/Qt5 \
      -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=ON 

# [[ $? == 0 ]] && make -j 32
# [[ $? == 0 ]] && make install

