# Gnuplot script file (for reference see:
# http://www.cs.uni.edu/Help/gnuplot/

set nomultiplot
set grid

#set output "ekman_layer.ps";set terminal postscript landscape color
set output "ekman_layer.ps";set terminal postscript landscape mono
#set terminal x11

set notime
set size 1,1
set origin 0.0,0.0
set multiplot
set size 0.5,0.5
set origin 0,0.5
set title "Ekman layer, u"
set ylabel "z (m)"
set xlabel "u (m/s)"
set xrange [-1:20]
set xrange [*:*]
set yrange [*:*]
set yrange [0:3000]
set key left top
plot "ekmandata.dat" using 5:1 title "Analytic" with lines, \
"ekmandata.dat" using 7:1 title "Num." with lines, \
"ekmandata.dat" using 9:1 title "WKB0" with lines, \
"ekmandata.dat" using 11:1 title "WKB1h" with lines, \
"ekmandata.dat" using 14:1 title "WKB1c" with lines


set size 0.5,0.5
set origin 0.5,0.5
set title "Ekman layer, v "
set ylabel "z (m)"
set xlabel "v (m/s)"
set xrange [-1:5]
set xrange [*:*]
#set yrange [*:*]
#set yrange [0:0010]
set key right
plot "ekmandata.dat" using 6:1 title "Analytic" with lines, \
"ekmandata.dat" using 8:1 title "Num." with lines, \
"ekmandata.dat" using 10:1 title "WKB0" with lines, \
"ekmandata.dat" using 12:1 title "WKB1h" with lines, \
"ekmandata.dat" using 13:1 title "WKB1c" with lines


set time
set size 0.5,0.5
set origin 0.0,0.0
set title "Ekman layer, K(z)"
set ylabel "z (m)"
set xlabel "K(z) (m^2/s)"
#set xrange [-1:20]
set xrange [-1:60]
set xrange [*:*]
#set yrange [*:*]
set xrange [-1:50]
#set yrange [0:0010]
set key right
plot "ekmandata.dat" using 2:1 title "K(z)" with lines, \
"ekmandata.dat" using 3:1 title "Analytic K" with lines
set notime

set size 0.5, 0.5
set origin 0.5, 0.0
set xrange [*:*]
set yrange [*:*]
set xlabel "u (m/s)"
set ylabel "v (m/s)"
set title "Ekman layer, hodographs"
set key outside
plot "ekmandata.dat" using 5:6 title "Analytic" with lines, \
"ekmandata.dat" using 7:8 title "Num." with lines, \
"ekmandata.dat" using 9:10 title "WKB0" with lines, \
"ekmandata.dat" using 11:12 title "WKB1h" with lines, \
"ekmandata.dat" using 14:13 title "WKB1c" with lines

set nogrid
set nomultiplot
