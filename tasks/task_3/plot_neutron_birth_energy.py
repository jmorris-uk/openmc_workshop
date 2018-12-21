#!/usr/bin/env python3

"""example_isotope_plot.py: plots 3D model with neutron tracks."""

__author__      = "Jonathan Shimwell"

import openmc
# import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout, Histogram , Bar
from plotly.figure_factory import create_quiver

import os
import numpy as np

#MATERIALS#

moderating_material = openmc.Material(1, "water") # water contains hydrogen which is a good neutron moderator
moderating_material.add_element('H', 2,'ao')
moderating_material.add_element('O', 1,'ao')
moderating_material.set_density('g/cm3',1.0)

mats = openmc.Materials([moderating_material])



#GEOMETRY#

sph1 = openmc.Sphere(R=100, boundary_type = 'vacuum')

simple_moderator_cell = openmc.Cell(region= -sph1 )
simple_moderator_cell.fill = moderating_material

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
source.energy = openmc.stats.Discrete([14e6], [1])
source.energy = openmc.stats.Watt(a=988000.0, b=2.249e-06)
source.energy = openmc.stats.Muir()
sett.source = source


# Run OpenMC!
model = openmc.model.Model(geom, mats, sett)
model.run() 

sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

print('energy of neutrons =',sp.source['E']) # these neutrons are all created

energy_bins = np.logspace(3,7) #energy range could b changed
energy_bins = np.logspace(3,7) #energy range could b changed

# Calculate pdf for source energies
probability, bin_edges = np.histogram(sp.source['E'], energy_bins, density=True)


# Plot source energy PDF
traces=[]
traces.append(Scatter(x=energy_bins[:-1], 
                       y=probability*np.diff(energy_bins),
                       line={'shape':'hv'},
                       hoverinfo='text' ,                       
                       name = 'neutron direction',                
                      )
              ) 

layout_ef = {'title':'neutron energy',
             'hovermode':'closest',
             'xaxis':{'title':'Energy (eV)'},
             'yaxis':{'title':'Probability'},
            }

plot({'data':traces,
      'layout':layout_ef},
      filename='particle_energy_histogram.html'
      )




