set terminal pngcairo enhanced font "arial, 10" fontscale 1.0 size 600,400
set output 'res.png'

set logscale x
set format x '%.0e'
set xrange [1e-21:1]
set xlabel "epsilon"

set logscale y 2
set yrange [0.2:25]
set ytics (0.5, 1, 2, 5, 10, 20)
set ylabel "% error"

set grid xtics ytics
set key off

plot 'result.out' using 1:($2*100) with lines lt 1, '' using 1:($2*100):($3*100) with yerrorbars lt 1
