#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry ."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt

natural_lead = openmc.Material(1, "natural_lead")
natural_lead.add_element('Pb', 1,'ao')

mats = openmc.Materials([natural_lead])
mats.export_to_xml()



#example surfaces
sph1 = openmc.Sphere(R=10)
sph2 = openmc.Sphere(R=20)
sph3 = +sph1 & -sph2 #above sph1 and below sph2

#add surfaces here using https://openmc.readthedocs.io/en/stable/usersguide/geometry.html#surfaces-and-regions

#example cell
cell = openmc.Cell(region=sph3)
cell.fill = natural_lead

#add another cell here

universe = openmc.Universe(cells=[cell]) #this list will need to include the new cell

plt.show(universe.plot(width=(45,45),basis='xz',colors={cell: 'blue'}))
plt.show(universe.plot(width=(45,45),basis='xy',colors={cell: 'blue'}))
plt.show(universe.plot(width=(45,45),basis='yz',colors={cell: 'blue'}))

geom = openmc.Geometry(universe)





