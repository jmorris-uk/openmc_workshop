#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple geometry ."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt
import os

mats = openmc.Materials()

natural_lead = openmc.Material(1, "natural_lead")
natural_lead.add_element('Pb', 1,'ao')
mats.append(natural_lead)
mats.export_to_xml()


#example surfaces
surface_sph1 = openmc.Sphere(R=10) #hint, change the radius of this shpere to 500
surface_sph2 = openmc.Sphere(R=20) #hint, change the radius of this shpere to 500+100

volume_sph1 = +surface_sph1 & -surface_sph2 # above (+) surface_sph and below (-) surface_sph2

#add surfaces here using https://openmc.readthedocs.io/en/stable/usersguide/geometry.html#surfaces-and-regions

#example cell
cell = openmc.Cell(region=volume_sph1)
cell.fill = natural_lead

#add another cell here

universe = openmc.Universe(cells=[cell]) #hint, this list will need to include the new cell

geom = openmc.Geometry(universe)

geom.export_to_xml()

p = openmc.Plot()
p.basis='xz'
p.filename = 'plot'
p.width = (45, 45)
p.pixels = (400, 400) 
p.color_by = 'material'
p.colors = {natural_lead: 'blue'}
plots = openmc.Plots([p])
plots.export_to_xml()

openmc.plot_geometry()

os.system('convert plot.ppm plot.png')
#os.system('eog plot.png')
os.system('xdg-open plot.png')
