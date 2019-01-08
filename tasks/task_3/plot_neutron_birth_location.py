#!/usr/bin/env python3

"""example_isotope_plot.py: plots neutron birth locations and directions."""

__author__      = "Jonathan Shimwell"

import openmc
# import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout, Histogram , Bar
from plotly.figure_factory import create_quiver

import os
import numpy as np

#MATERIALS#


mats = openmc.Materials([])



#GEOMETRY#

sph1 = openmc.Sphere(R=100, boundary_type = 'vacuum')

simple_moderator_cell = openmc.Cell(region= -sph1 )

universe = openmc.Universe(cells=[simple_moderator_cell]) 

geom = openmc.Geometry(universe)



#SIMULATION SETTINGS#

# Instantiate a Settings object
sett = openmc.Settings()
batches = 2
sett.batches = batches
sett.inactive = 0
sett.particles = 300
sett.particle = "neutron"
sett.run_mode = 'fixed source'


# creates a 14MeV point source
source = openmc.Source()
source.space = openmc.stats.Point((0,0,0))
source.angle = openmc.stats.Isotropic()
#source.energy = openmc.stats.Discrete([14e6], [1])
#source.energy = openmc.stats.Watt(a=988000.0, b=2.249e-06) #fission energy distribution
source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0) #neutron energy = 14.08MeV, AMU for D + T = 5, temperature is 20KeV
sett.source = source


# Run OpenMC!
model = openmc.model.Model(geom, mats, sett)
model.run() 

sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

print('energy of neutrons =',sp.source['xyz']) # these neutrons are all created



# plot the neutron trajectory
fig = create_quiver(sp.source['xyz'][:,0], sp.source['xyz'][:,1],
                    sp.source['uvw'][:,0], sp.source['uvw'][:,1],
                    arrow_scale = 0.1)

plot(fig, filename='particle_directions.html')

