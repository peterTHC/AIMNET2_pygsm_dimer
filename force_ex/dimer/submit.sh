#!/bin/bash
##NECESSARY JOB SPECIFICATIONS
#SBATCH --job-name=dimer
#SBATCH --output=dimer.%j
#SBATCH --time=24:00:00            
#SBATCH --ntasks=1                      #Request tasks
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4    #Request CPUs per task
#SBATCH --mem-per-cpu=7000

module load Anaconda3/2021.05
source activate aimnet2
python dimer_force.py > dimer.out
