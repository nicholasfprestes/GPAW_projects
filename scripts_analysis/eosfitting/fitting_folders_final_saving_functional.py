from __future__ import print_function
import numpy as np
from ase import Atoms
from ase.visualize import view
from gpaw import GPAW, PW
import os
#import errno
import pylab as plt
from ase.eos import EquationOfState
from ase.io import read

volumes = []
energies = []
localfolder = os.getcwd()
ecut = 200
ecutcounter = 0
ecutfolderlist = os.listdir(os.getcwd())
while ecutcounter < len(ecutfolderlist)-3:
	kcounter = 0
	kfolderlist = os.listdir(os.getcwd() + '/' + ecutfolderlist[ecutcounter])
	with open('zfit/' + ecutfolderlist[ecutcounter] + '.txt', 'a') as the_file:
		the_file.write('Energy Cutoff: ' + ecutfolderlist[ecutcounter] + '\n')
		the_file.write('CoffE	k	v0	e0	B\n')
	while kcounter < len(kfolderlist):
		a=0
		print(ecutcounter,kcounter)
		folder = os.listdir(os.getcwd()+ '/' + ecutfolderlist[ecutcounter] + '/' + kfolderlist[kcounter])
		while a < len(folder):
			a = a+2
			f = a-1
			configs = []
			configs = read(os.getcwd()+ '/' + ecutfolderlist[ecutcounter] + '/' + kfolderlist[kcounter] + '/' + folder[f])
			volume = configs.get_volume()
			energy = configs.get_potential_energy()
			volumes.append(volume)
			energies.append(energy)
			print(ecutfolderlist[ecutcounter]+ kfolderlist[kcounter] + folder[f])
		
		try:
			eos = EquationOfState(volumes, energies)
			v0, e0, B = eos.fit()
			print(ecutfolderlist[ecutcounter],kfolderlist[kcounter], v0, e0, B)
			v0str = str(v0)
			e0str = str(e0)
			Bstr = str(B)				
		except Exception:
			v0str = 'fail'
			e0str = 'fail'
			Bstr = 'fail'
			pass
		
		with open('zfit/' + ecutfolderlist[ecutcounter] + '.txt', 'a') as the_file:
				the_file.write(ecutfolderlist[ecutcounter] + '	' + kfolderlist[kcounter] + '	' +  v0str + '	'  + e0str + '	' +  Bstr + '\n')	
		

			

		
		kcounter = kcounter + 1
	ecutcounter = ecutcounter + 1
	ecut = ecut + 50
