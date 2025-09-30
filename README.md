This code is used for running pyGSM using a starting conformer (conf.xyz) and an indicated reaction direction (isomer.txt).
To make the pyGSM compatible with AIMNet2, and external force, the pyGSM folder in this repository needs to be installed.

To install this version of pyGSM you need to do

 cd pyGSM
 
 pip install .


The calculation workflow is to run a single-ended growing string method starting from the product of a Diels-Alder reaction with given direction for 50 steps.
The reactant complex is then taken from the result and further used for double-ended growing string method.
The final string output will be in molden format (opt_converged_000.xyz) and the output file is writen in gsm2.out


In the no_force_ex folder

conf.xyz: the product conformer xyz file

isomer.txt: the bonds that need to be broken

submit.sh: an example submission script. The conda environment name will be where everything is installed at

convert_conf.py: a python file used to convert single growing string method result to an input file containing both reactant and product for the second run of double-ended growing string method

test.py: pyGSM running file


In the force_ex/gsm folder

constraints.txt: the file used to indicate the external force direction in the shape of (N, 3)


In the force_ex/dimer folder

dimer_force.py: python file to run dimer method with external force direction implied by constraints.txt file
 
