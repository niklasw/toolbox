#%Module 1.0
#
#  OpenMPI module for use with 'environment-modules' package:
#

conflict openfoam
module add mpi/openmpi-x86_64 gcc/8.3
set softhome    "/home/software"
set name        "OpenFOAM"
set version     "5.x"
set prefix      "${softhome}/${name}/${name}-${version}"
set site        "EQUA"

set siteprefix  "$env(HOME)/${name}/${site}"

setenv          FOAM_INST_DIR     "${softhome}/${name}"
setenv          FOAM_BASH        "${prefix}/etc/bashrc"
setenv          WM_PROJECT_SITE "${siteprefix}" 
setenv          FOAM_SITE_SRC   "${siteprefix}/${version}/src"
setenv          FOAM_SITE_APP   "${siteprefix}/${version}/applications"
setenv          FOAM_SITE_TEMPLATES   "${siteprefix}/${version}/templates"
#setenv         GTAGSROOT      "${prefix}/src"

