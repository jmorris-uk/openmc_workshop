#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry with neutron flux."""

__author__      = "Jonathan Shimwell"

import openmc
import os
import json
import numpy as np
from numpy import random
import re 
from tqdm import tqdm

from material_maker_functions import *


def make_breeder_material(enrichment_fraction, breeder_material_name, temperature_in_C):

    #density data from http://aries.ucsd.edu/LIB/PROPS/PANOS/matintro.html

    natural_breeder_material = openmc.Material(2, "natural_breeder_material")
    breeder_material = openmc.Material(1, breeder_material_name) # this is for enrichmed Li6 

    element_numbers = get_element_numbers(breeder_material_name)
    elements = get_elements(breeder_material_name)

    for e, en in zip(elements, element_numbers):
        natural_breeder_material.add_element(e, en,'ao')

    for e, en in zip(elements, element_numbers):
        if e == 'Li':
            breeder_material.add_nuclide('Li6', en * enrichment_fraction, 'ao')
            breeder_material.add_nuclide('Li7', en * (1.0-enrichment_fraction), 'ao')  
        else:
            breeder_material.add_element(e, en,'ao')    

    density_of_natural_material_at_temperature = find_density_of_natural_material_at_temperature(breeder_material_name,temperature_in_C,natural_breeder_material)

    natural_breeder_material.set_density('g/cm3', density_of_natural_material_at_temperature)
    atom_densities_dict = natural_breeder_material.get_nuclide_atom_densities()
    atoms_per_barn_cm = sum([i[1] for i in atom_densities_dict.values()])

    breeder_material.set_density('atom/b-cm',atoms_per_barn_cm) 

    return breeder_material



def make_materials_geometry_tallies(batches,enrichment_fraction,inner_radius,thickness,breeder_material_name,temperature_in_C):
    print('simulating ',batches,enrichment_fraction,inner_radius,thickness,breeder_material_name)

    #MATERIALS#

    breeder_material = make_breeder_material(enrichment_fraction,breeder_material_name,temperature_in_C)
    eurofer = make_eurofer()
    mats = openmc.Materials([breeder_material, eurofer])


    #GEOMETRY#

    breeder_blanket_inner_surface = openmc.Sphere(R=inner_radius)
    breeder_blanket_outer_surface = openmc.Sphere(R=inner_radius+thickness)

    vessel_inner_surface = openmc.Sphere(R=inner_radius+thickness+10)
    vessel_outer_surface = openmc.Sphere(R=inner_radius+thickness+20,boundary_type='vacuum')

    breeder_blanket_region = -breeder_blanket_outer_surface & +breeder_blanket_inner_surface
    breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region) 
    breeder_blanket_cell.fill = breeder_material
    breeder_blanket_cell.name = 'breeder_blanket'

    inner_void_region = -breeder_blanket_inner_surface 
    inner_void_cell = openmc.Cell(region=inner_void_region) 
    inner_void_cell.name = 'inner_void'

    vessel_region = +vessel_inner_surface & -vessel_outer_surface
    vessel_cell = openmc.Cell(region=vessel_region) 
    vessel_cell.name = 'vessel'
    vessel_cell.fill = eurofer

    blanket_vessel_gap_region = -vessel_inner_surface & + breeder_blanket_outer_surface
    blanket_vessel_gap_cell = openmc.Cell(region=blanket_vessel_gap_region) 
    blanket_vessel_gap_cell.name = 'blanket_vessel_gap'    

    universe = openmc.Universe(cells=[inner_void_cell, 
                                      breeder_blanket_cell,
                                      blanket_vessel_gap_cell,
                                      vessel_cell])

    geom = openmc.Geometry(universe)

    #SIMULATION SETTINGS#

    sett = openmc.Settings()
    # batches = 3 # this is parsed as an argument
    sett.batches = batches
    sett.inactive = 10
    sett.particles = 500
    sett.run_mode = 'fixed source'

    source = openmc.Source()
    source.space = openmc.stats.Point((0,0,0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0) #neutron energy = 14.08MeV, AMU for D + T = 5, temperature is 20KeV
    sett.source = source

    #TALLIES#

    tallies = openmc.Tallies()

    # define filters
    cell_filter = openmc.CellFilter(breeder_blanket_cell)
    particle_filter = openmc.ParticleFilter([1]) #1 is neutron, 2 is photon
    surface_filter = openmc.SurfaceFilter(breeder_blanket_outer_surface)
    
    tally = openmc.Tally(1,name='TBR')
    tally.filters = [cell_filter,particle_filter]
    tally.scores = ['205']
    tallies.append(tally)

    tally = openmc.Tally(2,name='leakage')
    tally.filters = [surface_filter,particle_filter]
    tally.scores = ['current']
    tallies.append(tally)
 

    #RUN OPENMC #
    model = openmc.model.Model(geom, mats, sett, tallies)
    model.run()
    sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

    tbr_tally = sp.get_tally(name='TBR')
    tbr_tally_result = tbr_tally.sum[0][0][0]/batches #for some reason the tally sum is a nested list 
    tbr_tally_std_dev = tbr_tally.std_dev[0][0][0]/batches #for some reason the tally std_dev is a nested list 

    leak_tally = sp.get_tally(name='leakage')
    leak_tally_result = leak_tally.sum[0][0][0]/batches #for some reason the tally sum is a nested list 
    leak_tally_std_dev = leak_tally.std_dev[0][0][0]/batches #for some reason the tally std_dev is a nested list    

    return {'enrichment_fraction':enrichment_fraction,
            'tbr_tally':tbr_tally_result, 
            'tbr_tally_std_dev':tbr_tally_std_dev,
            'leak_tally':leak_tally_result,
            'leak_tally_st_dev':leak_tally_std_dev,
            'inner_radius':inner_radius,
            'thickness':thickness,
            'breeder_material_name':breeder_material_name,
            'temperature_in_C':temperature_in_C
           }





results = []
num_simulations=5

for i in tqdm(range(0,num_simulations)):
        breeder_material_name = random.choice(['Li4SiO4', 'F2Li2BeF2', 'Li', 'Pb84.2Li15.8'])
        enrichment_fraction = random.uniform(0, 1)
        inner_radius = random.uniform(1, 1000)
        thickness = random.uniform(1, 500)

        result = make_materials_geometry_tallies(batches=4,
                                                enrichment_fraction=enrichment_fraction,
                                                inner_radius=inner_radius,
                                                thickness=thickness,
                                                breeder_material_name = breeder_material_name, 
                                                temperature_in_C=500
                                                )
        results.append(result)



with open('simulation_results_sphere.json', 'w') as file_object:
    json.dump(results, file_object, indent=2)
       



