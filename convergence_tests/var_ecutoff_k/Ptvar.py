"""Bulk Al(fcc) test"""
from __future__ import print_function
import numpy as np
from ase import Atoms
from ase.visualize import view
from gpaw import GPAW, PW
import os
import errno

localfolder = os.getcwd()

for ecut in range(500,950,50):
	print('Energy cutoff:', ecut, 'eV')
	for k in range(13, 20):
		print('k-points:', k)
		for a in np.linspace(3.8500, 4.0500, 10):
			dire = localfolder +'/%.0f/%.0f/' % (ecut,k)
			name = dire +'Pt-bulk-fcc-%.0f-%.0f-%.4f' % (ecut,k,a)
			filename = name +'.txt'
			b = a / 2
			bulk = Atoms('Pt', cell=[[0, b, b],[b, 0, b],[b, b, 0]],pbc=True)
			if not os.path.exists(os.path.dirname(filename)):
				try:
					os.makedirs(os.path.dirname(filename))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise
			calc = GPAW(mode=PW(ecut),       # cutoff
            	kpts=(k, k, k),     # k-points
            	xc='PBE',
            	txt=filename)  # output file
			bulk.set_calculator(calc)
			energy = bulk.get_potential_energy()
			calc.write(name + '.gpw')
			print('Lattice Constant:', a, 'eV''Energy:', energy, 'eV')
		print(' ')
	