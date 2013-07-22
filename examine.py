#!/usr/bin/python

from optparse import OptionParser
from progressbar import ProgressBar, Percentage, Bar
import numpy as np
import pynbody as pyn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
try:
	from IPython import embed
except:
	from IPython.Shell import IPShellEmbed 
from sys import argv
from os.path import exists
import pynbody.analysis.angmom as angmom
import pynbody.plot.sph as p_sph
filename = ""

class pointplt():
	def __init__(self, sim):
		self.sim = sim
		self.point_size = 20
		self.color = 'k'
		self.range_x = (np.min(self.sim['x']), np.max(self.sim['x']))
		self.range_y = (np.min(self.sim['y']), np.max(self.sim['y']))
		self.plot()
	def cmap(self, qty, vmin=None, vmax=None):
		if vmin ==	None:
			vmin = np.min(self.sim[qty])
		if vmax ==	None:
			vmax = np.max(self.sim[qty])
		self.color = self.sim[qty]
		self.plot()
	def plot(self):
		plt.scatter(self.sim['x'], self.sim['y'], marker='.', c=self.color, s=self.point_size, edgecolors='none')
		plt.xlim(self.range_x)
		plt.ylim(self.range_y)
		plt.xlabel(self.sim['x'].units)
		plt.ylabel(self.sim['y'].units)


def points(sim):
	return pointplt(sim)

def twopoint_stars(sim):
	distances = []
	print "Simulation contains %d Stars" % len(sim.s)
	progress = ProgressBar(widgets=["Computing 2point correlation function:", Percentage(), Bar()])
	for i in progress(range(len(sim.s))):
		for j in range(len(sim.s)):
			if i != j:
				distances.append(np.linalg.norm(sim.s[i]['pos']-sim.s[j]['pos']))
	return np.array(distances)

#Spatial Derivative of the standard M4 Kernel
def dM4(x):
	if x <= 1:
		return 1.0/(4.0*np.pi)*(12.0*x+9.0*x**2)
	if x > 1 and x <= 2:
		return 1.0/(4.0*np.pi)*(3.0*(2-x)**2)
	else:
		return 0
	
#This function is not units-safe!
def massflux_cartesian(sim, axis, axis_value):
	x = np.abs(sim.g[axis] - axis_value)/sim.g['smooth']
	n = sim.g['smooth']/x*(sim.g[axis]-axis_value)
	return np.sum([n[i]*sim.g[i]['mass']*sim.g[i]['v'+axis]*dM4(x[i])/sim.g[i]['smooth']  for i in np.where(x < 2)[0]])

def scaleheight(sim, axis='z'):
	return np.inner(sim['mass'], np.abs(sim[axis]))/np.sum(sim['mass'])

def phase(sim):
	plt.loglog(sim.g['rho'], sim.g['temp'], 'r.', ms=1, mec='k')
	plt.xlabel('Density (%s)' % str(sim.g['rho'].units))
	plt.ylabel('Temperature (%s)' % str(sim.g['temp'].units))

def point_plot_3d(sim, qty='rho', size=2):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(sim['x'], sim['y'], sim['z'], c=sim[qty], s=size, marker=',', 
	edgecolor='none')

@pyn.snapshot.SimSnap.derived_quantity
def dt(sim):
   return np.array([float(i) for i in open(filename).readlines()[1:]])

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-c", "--code-units", action="store_true", dest="cunits",
	help="Keep sim in code units")
	(opts, args) = parser.parse_args()
	plt.ion()
	sim = pyn.load(args[0])
	if exists(args[0]+".dt"):
		filename = args[0]+".dt"
		sim['dt']
	if(not opts.cunits):
		#sim.physical_units()
		sim.g['rho'].convert_units('m_p cm**-3')
	try:
		embed()
	except:
		ipshell = IPShellEmbed() 
		ipshell()
