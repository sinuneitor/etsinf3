#!/bin/bash
#PBS -l nodes=4,walltime=00:10:00
#PBS -q cpa
#PBS -d .

printf "%s | " $ARGS
mpiexec ./newton $ARGS

