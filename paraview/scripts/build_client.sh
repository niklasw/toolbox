#!/bin/bash

# module add mpi
#     -DVTK_USE_OFFSCREEN_EGL=ON \
#     -DVTK_OPENGL_HAS_EGL=ON \
#     -DEGL_INCLUDE_DIR=/usr/include \
#     -DEGL_LIBRARY=/usr/lib64/libEGL_mesa.so.0\
#     -DEGL_opengl_LIBRARY=/usr/lib64/libOpenGL.so \
#     -DQt5_DIR=/remote/soft2/Qt/5.10.1/lib/cmake/Qt5 \

cmake ../ParaView-git/ \
      -DBUILD_TESTING=OFF \
      -DPARAVIEW_USE_PYTHON=ON \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=OFF \
      -DPARAVIEW_USE_MPI=ON \
      -DVTKm_ENABLE_MPI=ON \
      -DVTK_RENDERING_BACKEND=OpenGL2 \
      -DVTK_USE_X=ON \
      -DPARAVIEW_USE_QT=ON \
      -DCMAKE_INSTALL_PREFIX=/home/software/ParaView/client-git \
      -DOpenGL_GL_PREFERENCE=GLVND \
      -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=ON 

[[ $? == 0 ]] && make -j 32
[[ $? == 0 ]] && make install

