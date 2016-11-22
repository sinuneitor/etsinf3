#!/bin/bash
#PBS -l nodes=4,walltime=00:10:00
#PBS -q cpa
#PBS -d .
#PBS -o hello.out
#PBS -e hello.err

cat $PBS_NODEFILE
mpiexec ./hello
