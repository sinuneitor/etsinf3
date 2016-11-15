#!/bin/bash
#PBS -l nodes=1:ppn=2,walltime=00:10:00
#PBS -W x="NACCESSPOLICY:SINGLEJOB"
#PBS -q cpa
#PBS -d .

mpiexec ./ping
