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


inner_radius = 10
layer_thickness = 10
outer_radius = inner_radius + layer_thickness
print('outer_radius',outer_radius)

sph1 = openmc.Sphere(R=inner_radius)
sph2 = openmc.Sphere(R=outer_radius)
sph3 = +sph1 & -sph2 #above sph1 and below sph2

cell = openmc.Cell(region=sph3)








































#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry with neutron flux."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt
import os

breeder_material = openmc.Material(1, "PbLi") #Pb84.2Li15.8 with 90% enrichment of Li6

enrichment_fraction = 0.9

breeder_material.add_element('Pb', 84.2,'ao')
breeder_material.add_nuclide('Li6', enrichment_fraction*15.8, 'ao')
breeder_material.add_nuclide('Li7', (1.0-enrichment_fraction)*15.8, 'ao')
# breeder_material.set_density('atom/b-cm',3.2720171e-2)
breeder_material.set_density('g/cm3',11.0)

mats = openmc.Materials([breeder_material])






sph1 = openmc.Sphere(R=100)
sph2 = openmc.Sphere(R=200, boundary_type = 'vacuum')

sph3 = +sph1 & -sph2 

breeder_blanket_cell = openmc.Cell(region=sph3)
breeder_blanket_cell.fill = breeder_material

inner_vacuum_cell = openmc.Cell(region=-sph1)
#inner_vacuum_cell.fill = 'vacuum'
#cell.region =cell.bounding_box

universe = openmc.Universe(cells=[inner_vacuum_cell,breeder_blanket_cell]) 

geom = openmc.Geometry(universe)





# OpenMC simulation parameters
batches = 1
inactive = 10
particles = 5000

# Instantiate a Settings object
sett = openmc.Settings()
sett.batches = batches
sett.inactive = inactive
sett.particles = particles
sett.run_mode = 'fixed source'

# Create an initial uniform spatial source distribution over fissionable zones
source = openmc.Source()
source.space = openmc.stats.Point((0,0,0))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
sett.source = source


tallies = openmc.Tallies()


# Create mesh which will be used for tally
mesh = openmc.Mesh()
mesh_height=200
mesh_width = mesh_height
mesh.dimension = [mesh_width, mesh_height]
mesh.lower_left = [-200, -200]
mesh.upper_right = [200, 200]

# Create mesh filter for tally
mesh_filter = openmc.MeshFilter(mesh)
# Create mesh tally to score flux and tritium production rate
mesh_tally = openmc.Tally(1,name='tallies_on_mesh')
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ['flux','(n,t)']
tallies.append(mesh_tally)



cell_filter = openmc.CellFilter(breeder_blanket_cell)
tbr_tally = openmc.Tally(2,name='TBR')
tbr_tally.filters = [cell_filter]
tbr_tally.scores = ['205']
tallies.append(tbr_tally)

try:
    os.system('rm statepoint.'+str(batches)+'.h5')
except:
    pass

# Run OpenMC! using the python objects instead of the xml files
model = openmc.model.Model(geom, mats, sett, tallies)
model.run()
#openmc.run()

sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')
#sp = openmc.StatePoint('statepoint.100.h5')

tbr_tally_result = sp.get_tally(name='TBR')
print(tbr_tally_result)
print(tbr_tally_result.sum)



flux_tally = sp.get_tally(scores=['flux'])
flux_slice = flux_tally.get_slice(scores=['flux'])
#flux_slice.std_dev.shape = (mesh_width, mesh_height)
flux_slice.mean.shape = (mesh_width, mesh_height)

fig = plt.subplot()
plt.show(fig.imshow(flux_slice.mean))

print()
absorption_tally = sp.get_tally(scores=['(n,t)'])
absorption_slice = absorption_tally.get_slice(scores=['(n,t)'])
#absorption_slice.std_dev.shape = (mesh_width, mesh_height)
absorption_slice.mean.shape = (mesh_width, mesh_height)
#absorption_slice.mean.shape = (100,100)

fig = plt.subplot()
print(fig.imshow(absorption_slice.mean))
plt.show(fig.imshow(absorption_slice.mean))

plt.show(universe.plot(width=(400,400),basis='xz'))
#plt.show(universe.plot(width=(400,400),basis='xy'))
#plt.show(universe.plot(width=(400,400),basis='yz'))
