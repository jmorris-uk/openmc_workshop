#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry ."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt

breeder_material = openmc.Material(1, "PbLi") #Pb84.2Li15.8 with 90% enrichment of Li6

enrichment_fraction = 0.9

breeder_material.add_element('Pb', 84.2,'ao')
breeder_material.add_nuclide('Li6', enrichment_fraction*15.8, 'ao')
breeder_material.add_nuclide('Li7', (1-enrichment_fraction)*15.8, 'ao')
breeder_material.set_density('atom/b-cm',3.2720171e-2)

mats = openmc.Materials([breeder_material])
mats.export_to_xml()





sph1 = openmc.Sphere(R=10)
sph2 = openmc.Sphere(R=20)
sph1.boundary_type = 'vacuum'
sph2.boundary_type = 'vacuum'
sph3 = +sph1 & -sph2 

cell = openmc.Cell(region=sph3)
cell.fill = breeder_material
#cell.region =cell.bounding_box

universe = openmc.Universe(cells=[cell]) 

geom = openmc.Geometry(universe)

geom.export_to_xml()





# OpenMC simulation parameters
batches = 100
inactive = 10
particles = 5000

# Instantiate a Settings object
settings_file = openmc.Settings()
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = neutrons

# Create an initial uniform spatial source distribution over fissionable zones

source = openmc.Source()
source.space = openmc.stats.Point((0,0,0))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
settings_file.source = source

# Export to "settings.xml"
settings_file.export_to_xml()



tallies_file = openmc.Tallies()


# Create mesh which will be used for tally
mesh = openmc.Mesh()
mesh.dimension = [100, 100]
mesh.lower_left = [-0.63, -0.63]
mesh.upper_right = [0.63, 0.63]

# Create mesh filter for tally
mesh_filter = openmc.MeshFilter(mesh)

# Create mesh tally to score flux and fission rate
tally = openmc.Tally(name='flux')
tally.filters = [mesh_filter]
tally.scores = ['flux', 'fission']
tallies_file.append(tally)



# Export to "tallies.xml"
tallies_file.export_to_xml()



# Run OpenMC!
openmc.run()


