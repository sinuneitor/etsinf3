#!/bin/bash
#PBS -l nodes=4,walltime=00:10:00
#PBS -q cpa
#PBS -d .

mpiexec ./newtonpro -c5
cmp newton.pgm newton5o.pgm
