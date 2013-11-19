#!/usr/bin/awk -f
# Run as stlTranslate.awk xtran=2e-3 ytran=120.0 in.stl > out.stl
{
if($1~"vertex")
    printf("\tvertex %f %f %f\n",$2+xtran,$3+ytran,$4+ztran)
else
    printf("%s\n", $0)
}
