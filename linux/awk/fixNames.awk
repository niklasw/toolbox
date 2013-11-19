BEGIN {OFS=" "}
$1~"^solid" {printf("%s ","solid"); for(i=2;i<NF;i++){printf("%s_",$i);}; print $NF};
$1~"^endsolid" {printf("%s ","endsolid"); for(i=2;i<NF;i++){printf("%s_",$i);}; print $NF};
$1!~"^solid" && $1!~"endsolid" {print $0};
