#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry ."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt
import os

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

geom = openmc.Geometry(universe)

geom.export_to_xml()

vox_plot = openmc.Plot()
vox_plot.type = 'voxel'
vox_plot.width = (20., 20., 20.)
vox_plot.pixels = (200, 200, 200)
vox_plot.filename = 'plot_3d'
vox_plot.color_by = 'material'
vox_plot.colors = {natural_lead: 'blue'}
plots = openmc.Plots([vox_plot])
plots.export_to_xml()

openmc.plot_geometry()

os.system('openmc-voxel-to-vtk plot_3d.h5 -o plot_3d.vti')
os.system('paraview plot_3d.vti') # or visit might work better