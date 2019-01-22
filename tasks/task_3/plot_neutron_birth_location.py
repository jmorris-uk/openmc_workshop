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

sph1 = openmc.Sphere(R=1000, boundary_type = 'vacuum')

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


# creates a source object
source = openmc.Source()

#sets the source poition, direction and energy
source.space = openmc.stats.Point((0,0,0))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0) #neutron energy = 14.08MeV, AMU for D + T = 5, temperature is 20KeV

#sets the source position, direction and energy to be read from a file
source.file = 'source.h5'

sett.source = source


# Run OpenMC!
model = openmc.model.Model(geom, mats, sett)
model.run() 

sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

print('energy of neutrons =',sp.source['xyz']) # these neutrons are all created



# plot the neutron birth locations and trajectory
traces =[{
    'type': 'cone',
    'cauto' : False,
    'x':sp.source['xyz'][:,0],'y':sp.source['xyz'][:,1],'z':sp.source['xyz'][:,2],
    'u':sp.source['uvw'][:,0],'v':sp.source['uvw'][:,1],'w':sp.source['uvw'][:,2],
    'cmin':0,'cmax':1,
    "anchor": "tail",
    "colorscale": 'Viridis',
    "hoverinfo": "u+v+w+norm",
    "sizemode":"absolute",
    "sizeref":3,
    "showscale":False,
    }]

layout = {'title':'Neutron initial directions coloured by direction',
        'hovermode':'closest'}

plot({'data':traces,
    'layout':layout},
    filename='3d_plot_cones.html')

