changecom(//)changequote([,])                                                   
define(calc, [esyscmd(perl -e 'print ($1)')])                                   
define(icalc, [esyscmd(perl -e 'printf("%d",$1)')])                             

define(LL, 0.5)
define(ff, 0.0078125)
define(ll, 0.0625)
define(calcStretch, [esyscmd(stretchCalculator.py -L $1 -f $2 -l $3 --shortOutput)])

calcStretch(LL,ff,ll)
