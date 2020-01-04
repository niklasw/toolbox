#%Module 1.0
#
#  
#

module add openfoam/5.x
set softhome        "/home/software"
set name            "testSuite"
set version         ""
set prefix          "${softhome}/OpenFOAM/${name}"
set sitepkgs        "${prefix}/site-packages"

prepend-path        PYTHONPATH "${prefix}/site-packages"
set-alias           runParameterized "${sitepkgs}/parameterized/runParameterized.py"
