"""Bulk Al(fcc) test"""
from __future__ import print_function
import numpy as np
from ase import Atoms
from ase import Atom
from ase.lattice.compounds import *
from ase.visualize import view
from gpaw import GPAW, PW
import os
import errno
from ase.optimize import QuasiNewton

localfolder = os.getcwd()

for ecut in range(700,701,50):
	print('Energy cutoff:', ecut, 'eV')
	for k in range(17, 18):
		print('k-points:', k)
		for a in np.linspace(3.8800, 3.9600, 5):
			dire = localfolder +'/%.0f/%.0f/' % (ecut,k)
			name = dire +'Pt-bulk-fcc-%.0f-%.0f-%.4f' % (ecut,k,a)
			filename = name +'.txt'
			b = a/2
			c = 'a-Pt-%.0f-%.0f-%.4f' % (ecut,k,a)
			bulk = Atoms('Pt', cell=[[0, b, b],[b, 0, b],[b, b, 0]],pbc=True)
			#bulk = L1_0(symbol=('Co','Pt'),latticeconstant=(a,c), pbc=True)
			if not os.path.exists(os.path.dirname(filename)):
				try:
					os.makedirs(os.path.dirname(filename))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise
			bulk *= [2,2,2]
			distancebefore = bulk.get_distance(1,2)
			bulk.pop(4)
			bulk.append(Atom('Co', [0.0, 1.96, 1.96]))
			bulk.pop(6)
			bulk.append(Atom('Co', [3.9199999999999999, 3.9199999999999999, 3.9199999999999999]))
			#bulk.set_initial_magnetic_moments([1,1,1,1])
			calc = GPAW(mode=PW(ecut),       # cutoff
            	kpts=(k, k, k),     # k-points
            	xc='PBE',
            	txt=filename)  # output file
			bulk.set_calculator(calc)
			relax = QuasiNewton(bulk, logfile= c + '.log')
			relax.run(fmax=0.0001)
			#energy = bulk.get_potential_energy()
			#atomons = bulk.get_magnetic_moments()
			distanceafter = bulk.get_distance(0,1)
			calc.write(name + '.gpw')
			#print('Lattice Constant:', a, 'eV''Energy:', energy, 'eV', ' Magnetic Momentes: ', atomons)
			print('Lattice Constant:', a, ' Distance Before: ', distancebefore,  ' Distance After: ', distanceafter)
		print(' ')
	