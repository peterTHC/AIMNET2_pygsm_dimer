#!/bin/bash

#SBATCH -t 24:00:00             #Time for the job to run
#SBATCH -J GSM                 #Name of the job appears on the queue
#SBATCH -o GSM.out             #Name of the output log file
#SBATCH -e GSM.err             #Log file for any errors
#SBATCH --job-name=GSM        
#SBATCH --time=24:00:00          # Set the wall clock limit to 1hr and 30min
#SBATCH --ntasks=1                      #Request tasks
#SBATCH --cpus-per-task=1     #Request CPUs per task
#SBATCH --mem-per-cpu=7000

module load Anaconda3/2021.05
source activate aimnet2
python ase_api_example.py 
