#!/usr/bin/env python3


import openmc
import openmc.model
import os
import matplotlib.pyplot as plt


#MATERIALS#

mats = openmc.Materials()

copper = openmc.Material(name='Copper')
copper.set_density('g/cm3', 8.5)
copper.add_element('Cu', 1.0)
mats.append(copper)

eurofer = openmc.Material(name='EUROFER97')
eurofer.set_density('g/cm3', 7.75)
eurofer.add_element('Fe', 89.067, percent_type='wo')
eurofer.add_element('C', 0.11, percent_type='wo')
eurofer.add_element('Mn', 0.4, percent_type='wo')
eurofer.add_element('Cr', 9.0, percent_type='wo')
eurofer.add_element('Ta', 0.12, percent_type='wo')
eurofer.add_element('W', 1.1, percent_type='wo')
eurofer.add_element('N', 0.003, percent_type='wo')
eurofer.add_element('V', 0.2, percent_type='wo')
mats.append(eurofer)

#GEOMETRY#

central_sol_surface = openmc.ZCylinder(R=100)
central_shield_outer_surface = openmc.ZCylinder(R=110,boundary_type='vacuum')
vessel_inner = openmc.Sphere(R=500,boundary_type='vacuum')
first_wall_outer_surface = openmc.Sphere(R=510)
breeder_blanket_outer_surface = openmc.Sphere(R=610)

central_sol_region = -central_sol_surface & -breeder_blanket_outer_surface
central_sol_cell = openmc.Cell(region=central_sol_region) 
central_sol_cell.fill = copper

central_shield_region = +central_sol_surface & -central_shield_outer_surface & -breeder_blanket_outer_surface
central_shield_cell = openmc.Cell(region=central_shield_region) 
central_shield_cell.fill = eurofer

first_wall_region = -first_wall_outer_surface & +vessel_inner & +central_shield_outer_surface
first_wall_cell = openmc.Cell(region=first_wall_region) 
first_wall_cell.fill = eurofer

breeder_blanket_region = +first_wall_outer_surface & -breeder_blanket_outer_surface & +central_shield_outer_surface
breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region) 
breeder_blanket_cell.fill = eurofer

#this is a void and hence has no material fill
inner_vessel_region = +central_shield_outer_surface & -vessel_inner
inner_vessel_cell = openmc.Cell(region=inner_vessel_region) 
inner_vessel_cell.name = 'inner_vessel'

universe = openmc.Universe(cells=[central_sol_cell, central_shield_cell ,first_wall_cell , breeder_blanket_cell])

# VISULISATION

plt.show(universe.plot(width=(1500,1500),basis='xz'))
plt.show(universe.plot(width=(1500,1500),basis='xy'))
plt.show(universe.plot(width=(1500,1500),basis='yz'))
