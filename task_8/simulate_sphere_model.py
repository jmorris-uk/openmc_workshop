#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry with neutron flux."""

__author__      = "Jonathan Shimwell"

import openmc
import os
import json
import numpy as np
from numpy import random

#import chemical_formula #from pyEQL github but does not support floats in equation
    # element_numbers = chemical_formula.get_element_numbers(breeder_material_name)
    # elements =chemical_formula.get_elements(breeder_material_name)


import re 



def read_chem_eq(chemical_equation):
        return [a for a in re.split(r'([A-Z][a-z]*)', chemical_equation) if a]


def get_elements(chemical_equation):
        chemical_equation_chopped_up = read_chem_eq(chemical_equation)
        list_elements = []

        for counter in range(0, len(chemical_equation_chopped_up)):
            if chemical_equation_chopped_up[counter].isalpha():
                element_symbol = chemical_equation_chopped_up[counter]
                list_elements.append(element_symbol)
        return list_elements

def get_element_numbers(chemical_equation):
        chemical_equation_chopped_up = read_chem_eq(chemical_equation)
        list_of_fractions = []

        for counter in range(0, len(chemical_equation_chopped_up)):
            if chemical_equation_chopped_up[counter].isalpha():
                if counter == len(chemical_equation_chopped_up)-1:
                    list_of_fractions.append(1.0)
                elif not (chemical_equation_chopped_up[counter + 1]).isalpha():
                    list_of_fractions.append(float(chemical_equation_chopped_up[counter + 1]))
                else:
                    list_of_fractions.append(1.0)
        return list_of_fractions


def make_materials(enrichment_fraction, breeder_material_name, temperature_in_C):

    #density data from http://aries.ucsd.edu/LIB/PROPS/PANOS/matintro.html

    natural_breeder_material = openmc.Material(2, "natural_breeder_material")
    breeder_material = openmc.Material(1, "breeder_material")

    element_numbers = get_element_numbers(breeder_material_name)
    elements = get_elements(breeder_material_name)

    for e, en in zip(elements, element_numbers):
        natural_breeder_material.add_element(e, en,'ao')
    print('natural_breeder_material',natural_breeder_material)

    if breeder_material_name == 'Pb84.2Li15.8':
        #Pb84.2Li15.8 is the eutectic ratio, this could be a varible

        density_of_natural_material_at_temperature = 99.90*(0.1-16.8e-6*temperature_in_C) #valid for in the range 240-350 C. source http://aries.ucsd.edu/LIB/PROPS/PANOS/lipb.html

    if breeder_material_name == 'F2Li2BeF2':
        #Li2BeF4 made from 2(FLi):BeF2 is the eutectic ratio, this could be a varible

        density_of_natural_material_at_temperature = 2.214 - 4.2e-4 * temperature_in_C # source http://aries.ucsd.edu/LIB/MEETINGS/0103-TRANSMUT/gohar/Gohar-present.pdf

    if breeder_material_name == 'Li':

        density_of_natural_material_at_temperature = 0.515 - 1.01e-4 * (temperature_in_C - 200) # valid between 200 - 1600 C source http://aries.ucsd.edu/LIB/PROPS/PANOS/li.html

    natural_breeder_material.set_density('g/cm3', density_of_natural_material_at_temperature)
    atom_densities_dict = natural_breeder_material.get_nuclide_atom_densities()
    atoms_per_barn_cm = sum([i[1] for i in atom_densities_dict.values()])

    for e, en in zip(elements, element_numbers):
        if e == 'Li':
            breeder_material.add_nuclide('Li6', en * enrichment_fraction, 'ao')
            breeder_material.add_nuclide('Li7', en * (1.0-enrichment_fraction), 'ao')  

        else:
            natural_breeder_material.add_element(e, en,'ao')

    breeder_material.set_density('atom/b-cm',atoms_per_barn_cm) 

    mats = openmc.Materials([breeder_material])
    print(breeder_material)
    return mats

def make_materials_geometry_tallies(batches,enrichment_fraction,inner_radius,thickness,breeder_material_name,temperature_in_C):
    print('simulating ',batches,enrichment_fraction,inner_radius,thickness,breeder_material_name)

    #MATERIALS#

    mats = make_materials(enrichment_fraction,breeder_material_name,temperature_in_C)
    for mat in mats:
        print(mat)
        if mat.name == 'breeder_material':
            print('found breeder materials')
            breeder_material = mat

    #GEOMETRY#

    breeder_blanket_inner_surface = openmc.Sphere(R=inner_radius)
    breeder_blanket_outer_surface = openmc.Sphere(R=inner_radius+thickness,boundary_type='vacuum')

    breeder_blanket_region = -breeder_blanket_outer_surface & +breeder_blanket_inner_surface
    breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region) 
    breeder_blanket_cell.fill = breeder_material
    breeder_blanket_cell.name = 'breeder_blanket'

    inner_vessel_region = -breeder_blanket_inner_surface 
    inner_vessel_cell = openmc.Cell(region=inner_vessel_region) 
    breeder_blanket_cell.name = 'inner_vessel'

    universe = openmc.Universe(cells=[inner_vessel_cell, breeder_blanket_cell])
    geom = openmc.Geometry(universe)

    #SIMULATION SETTINGS#

    sett = openmc.Settings()
    # batches = 3
    sett.batches = batches
    sett.inactive = 50
    sett.particles = 5000
    sett.run_mode = 'fixed source'

    source = openmc.Source()
    source.space = openmc.stats.Point((0,0,0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Discrete([14e6], [1])
    sett.source = source

    #TALLIES#

    tallies = openmc.Tallies()

    cell_filter = openmc.CellFilter(breeder_blanket_cell)
    particle_filter = openmc.ParticleFilter([1]) #1 is neutron, 2 is photon
    tbr_tally = openmc.Tally(1,name='TBR')
    tbr_tally.filters = [cell_filter,particle_filter]
    tbr_tally.scores = ['205']

    tallies.append(tbr_tally)

    surface_filter = openmc.SurfaceFilter(breeder_blanket_outer_surface)
    leak_tally = openmc.Tally(2,name='leakage')
    particle_filter = openmc.ParticleFilter([1])
    leak_tally.filters = [surface_filter,particle_filter]
    leak_tally.scores = ['current']
    tallies.append(leak_tally)

    cell_filter = openmc.CellFilter(breeder_blanket_cell)
    heat_tally = openmc.Tally(3,name='heat')
    heat_tally.filters = [cell_filter]
    heat_tally.scores = ['301'] #-4 for neutron heat, -6 for photon heat
    tallies.append(heat_tally)    

    # energy_filter = openmc.EnergyFilter([0.0, 4.0, 1.0e6]) # such an energy filter can be used to get the neutron spectra

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

    heat_tally = sp.get_tally(name='heat')
    heat_tally_result = heat_tally.sum[0][0][0]/batches #for some reason the tally sum is a nested list 
    heat_tally_std_dev = heat_tally.std_dev[0][0][0]/batches #for some reason the tally std_dev is a nested list    

    print('heat_tally_result',heat_tally_result)

    return {'enrichment_fraction':enrichment_fraction,
            'tbr_tally':tbr_tally_result, 
            'tbr_tally_std_dev':tbr_tally_std_dev,
            'leak_tally':leak_tally_result,
            'leak_tally_st_dev':leak_tally_std_dev,
            'heat_tally':heat_tally_result,
            'heat_tally_std_dev':heat_tally_std_dev,
            'inner_radius':inner_radius,
            'thickness':thickness,
            'breeder_material_name':breeder_material_name,
            'temperature_in_C':temperature_in_C
           }







natural_enrichment_fraction=0.07589
#comparison TBR simulations https://link.springer.com/article/10.1023/B:JOFE.0000021555.70423.f1

with open('simulation_results.json', 'w') as file_object:
    file_object.write('[')
for breeder_material_name in ['F2Li2BeF2', 'Li', 'Pb84.2Li15.']:
    for x in range(0,10):
        enrichment_fraction = random.uniform(0, 1)
        inner_radius = random.uniform(1, 1000)
        thickness = random.uniform(1, 500)

        # for enrichment_fraction in np.linspace(start=0,stop=1,num=10):
        #     for inner_radius in np.linspace(start=100,stop=10000,num=10):
        #         for thickness in np.linspace(start=50,stop=500,num=10):
        results = (make_materials_geometry_tallies(batches=4,
                                                enrichment_fraction=enrichment_fraction,
                                                inner_radius=inner_radius,
                                                thickness=thickness,
                                                breeder_material_name = breeder_material_name, # 'Flibe', #Flibe or Li or PbLi
                                                temperature_in_C=300
                                                ))

        print(results)
        with open('simulation_results.json', 'a') as file_object:
            json.dump(results, file_object, indent=2)
            file_object.write(',')


with open('simulation_results.json', 'a') as file_object:
    file_object.write(']')



