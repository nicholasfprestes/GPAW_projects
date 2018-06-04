"""Bulk Al(fcc) test"""
from __future__ import print_function
import numpy as np
from ase import Atoms
from ase import Atom
from ase.build import *
from gpaw import GPAW, PW
import os
import errno
from ase.optimize import QuasiNewton

localfolder = os.getcwd()

for ecut in range(200,500,50):
	print('Energy cutoff:', ecut, 'eV')
	for k in range(6, 12):
		
		#Setting up different k points for different regions

		kz = k					
		kxy = k // 2				
		print('k-xy: ', kxy, ' kz: ', kz)	

		#Setting up file names

		dire = localfolder +'/%.0f/%.0f/' % (ecut,k)		#Getting file locations
		name = dire +'Pt-bulk-fcc-%.0f-%.0f' % (ecut,k)		#Setting up file names
		filename = name +'.txt'					#Setting up file names
		
		
		#Verifying the existance of folders for file creation and creating them if the path doest exist

		if not os.path.exists(os.path.dirname(filename)):
			try:
				os.makedirs(os.path.dirname(filename))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		
		#Creating structure
			
		pt111=fcc111('Pt', size=(2,2,4))
		pt111.pbc=True
		pt111.cell=[[5.5437171645025325, 0.0, 0.0], [2.7718585822512662, 4.800999895855028, 0.0], [0.0, 0.0, 9.06]]
		co0001=hcp0001('Co', size=(2,2,4))
		del co0001[[atom.index for atom in co0001 if co0001[atom.index].tag==1]]	#Without excluding this layer Pt atoms would be on top of Co atoms 
		co0001.pbc=True
		co0001.cell=[[5.02, 0.0, 0.0], [2.51, 4.347447526997882, 0.0], [0.0, 0.0, 6.10425]]
		intercopt=stack(co0001,pt111,maxstrain=1)
		
		#Setting up Calculator
		
		calc = GPAW(mode=PW(ecut), kpts=(kxy, kxy, kz), xc='PBE',txt=filename)  
		intercopt.set_calculator(calc)
		energy = intercopt.get_potential_energy()
		print('Energy before: ', energy)
		relax = QuasiNewton(intercopt, logfile= name + '.log')
		relax.run(fmax=0.01)
		energy = intercopt.get_potential_energy()
		print('Energy after: ', energy)
		#atomons = bulk.get_magnetic_moments()
		#distanceafter = bulk.get_distance(0,1)
		calc.write(name + '.gpw')
		#print('Lattice Constant:', a, 'eV''Energy:', energy, 'eV', ' Magnetic Momentes: ', atomons)
		#print('Lattice Constant:', a, ' Distance Before: ', distancebefore,  ' Distance After: ', distanceafter)
		print('End')
	
