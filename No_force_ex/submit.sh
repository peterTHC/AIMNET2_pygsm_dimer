#!/bin/bash
##NECESSARY JOB SPECIFICATIONS
#SBATCH --job-name=gsm
#SBATCH --output=gsm.%j
#SBATCH --time=24:00:00            
#SBATCH --ntasks=1                      #Request tasks
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4    #Request CPUs per task
#SBATCH --mem-per-cpu=7000

module load Anaconda3/2021.05
source activate aimnet2
#python test.py -xyzfile conf.xyz -isomers isomer.txt -mode SE_GSM -package ase -num_nodes 20 -mp_cores 4 > gsm.out -max_gsm_iters 50
#convert_conf.py
python test.py -xyzfile conf_continue.xyz -mode DE_GSM -package ase -mp_cores 4 -restart_file opt_converged_000.xyz > gsm2.out
