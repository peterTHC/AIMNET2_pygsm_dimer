import ase
import ase.units
import torch
import numpy as np
import re
import os
from aimnet2calc import AIMNet2ASE
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from ase.optimize import BFGS
from ase import io
from ase.mep import DimerControl,  MinModeAtoms, MinModeTranslate

class Constraint_custom_forces:
    def __init__(self, a, direction):
        self.a = a
        self.dir = direction

    def adjust_positions(self, atoms, newpositions):
        pass

    def adjust_forces(self, atoms, forces):
        forces[self.a] = forces[self.a] + self.dir
        
def read_constraints_file(constraints_file):
    with open(constraints_file) as f:
        tmp = filter(None, (line.rstrip() for line in f))
        lines = []
        for line in tmp:
            lines.append(line)
    constraints = []
    for line in lines:
        force_x = float(line.split()[0])
        force_y = float(line.split()[1])
        force_z = float(line.split()[2])
        constraints.append([force_x, force_y, force_z])
    return np.array(constraints)


# Read initial and final states:
initial = io.read('./Reactant_old.xyz')

constraints_forces = read_constraints_file('constraints.txt')
atom_indices = [x for x in range(len(initial))]
constraints = Constraint_custom_forces(atom_indices, constraints_forces)

initial.set_constraint(constraints)
calc = AIMNet2ASE('aimnet2',charge=0)
initial.calc = calc
opt1 = BFGS(initial)
opt1.run(fmax=0.000027,steps=10000)

atoms = io.read('./TS_old_0.xyz')
calc = AIMNet2ASE('aimnet2',charge=0)
atoms.calc = calc

atoms.set_constraint(constraints)

with DimerControl(initial_eigenmode_method='displacement',
                  displacement_method='vector', max_num_rot = 10) as d_control:
    d_atoms = MinModeAtoms(atoms, d_control)
    displacement_vector = io.read('./TS_old_2.xyz').positions - io.read('./TS_old_0.xyz').positions
    d_atoms.displace(displacement_vector=displacement_vector)
    
    # Converge to a saddle point
    with MinModeTranslate(d_atoms, trajectory='dimer_method.traj') as dim_rlx:
        dim_rlx.run(fmax=0.0005, steps=5000)

final = io.read('./Product_old.xyz')
final.set_constraint(constraints)
calc = AIMNet2ASE('aimnet2',charge=0)
final.calc = calc
opt2 = BFGS(final)
opt2.run(fmax=0.000027,steps=10000)


io.write('Reactant_force.xyz',initial,format='xyz')
io.write('TS_force.xyz',atoms,format='xyz')
io.write('Product_force.xyz',final,format='xyz')

E_R = initial.get_potential_energy()
E_TS = atoms.get_potential_energy()
E_P = final.get_potential_energy()

print('Reactant Absolute Energy: ' + str(E_R*23.0609) + ' kcal/mol')
print('TS Absolute Energy: ' + str(E_TS*23.0609) + ' kcal/mol')
print('Product Absolute Energy: ' + str(E_P*23.0609) + ' kcal/mol')

print('Reactant Relative Energy: ' + str((E_R-E_R)*23.0609) + ' kcal/mol')
print('TS Relative Energy: ' + str((E_TS-E_R)*23.0609) + ' kcal/mol')
print('Product Relative Energy: ' + str((E_P-E_R)*23.0609) + ' kcal/mol')


