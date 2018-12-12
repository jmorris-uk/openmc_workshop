#!/usr/bin/env python3

""" simulate_model.py: obtains a few netronics parameters for a basic tokamak geometry ."""
""" run with python3 simulate_model.py | tqdm >> /dev/null """
""" outputs results to a file called simulation_results*.json """

__author__      = "Jonathan Shimwell"


import re 
import openmc
import os
import json
import numpy as np
from numpy import random
from tqdm import tqdm
import sys
import os


# nuclear_data_path =  os.path.dirname(os.environ['OPENMC_CROSS_SECTIONS'])

def calculate_crystal_structure_density(material,atoms_per_unit_cell,volume_of_unit_cell_cm3):
      molar_mass = material.average_molar_mass*len(material.nuclides)
      atomic_mass_unit_in_g = 1.660539040e-24
      density_g_per_cm3 = molar_mass * atomic_mass_unit_in_g * atoms_per_unit_cell / volume_of_unit_cell_cm3
      #print('density =',density_g_per_cm3)
      return density_g_per_cm3

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

def make_breeder_materials(enrichment_fraction, breeder_material_name, temperature_in_C):

    #density data from http://aries.ucsd.edu/LIB/PROPS/PANOS/matintro.html

    natural_breeder_material = openmc.Material(2, "natural_breeder_material")
    breeder_material = openmc.Material(1, "breeder_material")

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

    if breeder_material_name == 'Pb84.2Li15.8':
        #Pb84.2Li15.8 is the eutectic ratio, this could be a varible

        density_of_natural_material_at_temperature = 99.90*(0.1-16.8e-6*temperature_in_C) #valid for in the range 240-350 C. source http://aries.ucsd.edu/LIB/PROPS/PANOS/lipb.html

    if breeder_material_name == 'F2Li2BeF2':
        #Li2BeF4 made from 2(FLi):BeF2 is the eutectic ratio, this could be a varible

        density_of_natural_material_at_temperature = 2.214 - 4.2e-4 * temperature_in_C # source http://aries.ucsd.edu/LIB/MEETINGS/0103-TRANSMUT/gohar/Gohar-present.pdf

    if breeder_material_name == 'Li':

        density_of_natural_material_at_temperature = 0.515 - 1.01e-4 * (temperature_in_C - 200) # valid between 200 - 1600 C source http://aries.ucsd.edu/LIB/PROPS/PANOS/li.html

    if breeder_material_name == 'Li4SiO4':

        density_of_natural_material_at_temperature = calculate_crystal_structure_density(natural_breeder_material,14,1.1543e-21)
        print('density_of_natural_material_at_temperature',density_of_natural_material_at_temperature)


    natural_breeder_material.set_density('g/cm3', density_of_natural_material_at_temperature)
    atom_densities_dict = natural_breeder_material.get_nuclide_atom_densities()
    atoms_per_barn_cm = sum([i[1] for i in atom_densities_dict.values()])
    print('atoms_per_barn_cm',atoms_per_barn_cm)
    breeder_material.set_density('atom/b-cm',atoms_per_barn_cm) 

    return breeder_material

def make_materials():  

    copper = openmc.Material(name='Copper')
    copper.set_density('g/cm3', 8.5)
    copper.add_element('Cu', 1.0)
    # mats.append(copper) 

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
    # mats.append(eurofer)    
    return eurofer, copper

def make_materials_geometry_tallies(batches,nps,enrichment_fraction,inner_radius,thickness,breeder_material_name,temperature_in_C):
    #print('simulating ',batches,enrichment_fraction,inner_radius,thickness,breeder_material_name)

    #MATERIALS#
    breeder_material = make_breeder_materials(enrichment_fraction,breeder_material_name,temperature_in_C)
    eurofer, copper = make_materials()
    mats = openmc.Materials([breeder_material,eurofer, copper])
    mats.export_to_xml('materials.xml')


    #GEOMETRY#

    # central_sol_surface = openmc.ZCylinder(R=100)
    # central_shield_outer_surface = openmc.ZCylinder(R=110,boundary_type='vacuum')
    # vessel_inner = openmc.Sphere(R=500,boundary_type='vacuum')
    # first_wall_outer_surface = openmc.Sphere(R=510)
    # breeder_blanket_outer_surface = openmc.Sphere(R=610)

    # central_sol_region = -central_sol_surface & -breeder_blanket_outer_surface
    # central_sol_cell = openmc.Cell(region=central_sol_region) 
    # central_sol_cell.fill = copper

    # central_shield_region = +central_sol_surface & -central_shield_outer_surface & -breeder_blanket_outer_surface
    # central_shield_cell = openmc.Cell(region=central_shield_region) 
    # central_shield_cell.fill = eurofer

    # first_wall_region = -first_wall_outer_surface & +vessel_inner & +central_shield_outer_surface
    # first_wall_cell = openmc.Cell(region=first_wall_region) 
    # first_wall_cell.fill = eurofer

    # breeder_blanket_region = +first_wall_outer_surface & -breeder_blanket_outer_surface & +central_shield_outer_surface
    # breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region) 
    # breeder_blanket_cell.fill = breeder_material

    # universe = openmc.Universe(cells=[central_sol_cell,central_shield_cell,first_wall_cell, breeder_blanket_cell])


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
    geom.export_to_xml('geometry.xml')

    #SIMULATION SETTINGS#

    sett = openmc.Settings()
    sett.batches = batches
    sett.inactive = 1
    sett.particles = nps
    sett.run_mode = 'fixed source'

    source = openmc.Source()
    source.space = openmc.stats.Point((0,0,0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Discrete([14.08e6], [1])
    sett.source = source

    sett.export_to_xml('settings.xml')

    #TALLIES#

    tallies = openmc.Tallies()

    particle_filter = openmc.ParticleFilter([1]) #1 is neutron, 2 is photon
    cell_filter = openmc.CellFilter(breeder_blanket_cell)
    cell_filter_vessel = openmc.CellFilter(vessel_cell)
    surface_filter_front = openmc.SurfaceFilter(breeder_blanket_inner_surface)
    surface_filter_rear = openmc.SurfaceFilter(breeder_blanket_outer_surface)
    energy_bins = openmc.mgxs.GROUP_STRUCTURES['VITAMIN-J-175']   
    energy_filter = openmc.EnergyFilter(energy_bins)


    tally = openmc.Tally(1,name='TBR')
    tally.filters = [cell_filter,particle_filter]
    tally.scores = ['205']
    tallies.append(tally)

    tally = openmc.Tally(2,name='blanket_leakage')
    tally.filters = [surface_filter_rear,particle_filter]
    tally.scores = ['current']
    tallies.append(tally)

    tally = openmc.Tally(3,name='vessel_leakage')
    tally.filters = [surface_filter_rear,particle_filter]
    tally.scores = ['current']
    tallies.append(tally)    

    tally = openmc.Tally(4,name='rear_neutron_spectra')
    tally.filters = [surface_filter_rear,particle_filter,energy_filter]
    tally.scores = ['flux']
    tallies.append(tally)

    tally = openmc.Tally(5,name='front_neutron_spectra')
    tally.filters = [surface_filter_front,particle_filter,energy_filter]
    tally.scores = ['flux']
    tallies.append(tally)

    tally = openmc.Tally(6,name='breeder_blanket_spectra')
    tally.filters = [cell_filter,particle_filter,energy_filter]
    tally.scores = ['flux']
    tallies.append(tally)    

    tally = openmc.Tally(7,name='vacuum_vessel_spectra')
    tally.filters = [cell_filter_vessel,particle_filter,energy_filter]
    tally.scores = ['flux']
    tallies.append(tally)        

    tally = openmc.Tally(8,name='DPA')
    tally.filters = [cell_filter_vessel,particle_filter]
    tally.scores = ['444']
    tallies.append(tally)    

    # heat_tally = openmc.Tally(5,name='heat')
    # heat_tally.filters = [cell_filter]
    # heat_tally.scores = ['301'] #-4 for neutron heat, -6 for photon heat
    # tallies.append(heat_tally)    
    # this returns 0 as 301 is missing from xs file

    #RUN OPENMC #
    model = openmc.model.Model(geom, mats, sett, tallies)
    
    model.run()


    #RETRIEVING RESULTS

    sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')
    
    json_output= {'enrichment_fraction':enrichment_fraction,
                  'inner_radius':inner_radius,
                  'thickness':thickness,
                  'breeder_material_name':breeder_material_name,
                  'temperature_in_C':temperature_in_C}


    tally = sp.get_tally(name='TBR')
    tally_result = tally.sum[0][0][0]/batches #for some reason the tally sum is a nested list 
    tally_std_dev = tally.std_dev[0][0][0]/batches #for some reason the tally std_dev is a nested list 

    json_output['tbr']={'value':tally_result, 
                        'std_dev':tally_std_dev}


    tally = sp.get_tally(name='DPA')
    tally_result = tally.sum[0][0][0]/batches 
    tally_std_dev = tally.std_dev[0][0][0]/batches 

    json_output['dpa']={'value':tally_result, 
                        'std_dev':tally_std_dev}


    tally = sp.get_tally(name='blanket_leakage')
    tally_result = tally.sum[0][0][0]/batches 
    tally_std_dev = tally.std_dev[0][0][0]/batches  

    json_output['blanket_leakage']={'value':tally_result, 
                                    'std_dev':tally_std_dev}


    tally = sp.get_tally(name='vessel_leakage')
    tally_result = tally.sum[0][0][0]/batches 
    tally_std_dev = tally.std_dev[0][0][0]/batches  

    json_output['vessel_leakage']={'value':tally_result, 
                                   'std_dev':tally_std_dev}                                    


    spectra_tally = sp.get_tally(name='rear_neutron_spectra')
    spectra_tally_result = [entry[0][0] for entry in spectra_tally.mean] 
    spectra_tally_std_dev = [entry[0][0] for entry in spectra_tally.std_dev] 

    json_output['rear_neutron_spectra']={'value':spectra_tally_result,
                                         'std_dev':spectra_tally_std_dev,
                                         'energy_groups':list(energy_bins)}


    spectra_tally = sp.get_tally(name='front_neutron_spectra')
    spectra_tally_result = [entry[0][0] for entry in spectra_tally.mean] 
    spectra_tally_std_dev = [entry[0][0] for entry in spectra_tally.std_dev] 

    json_output['front_neutron_spectra']={'value':spectra_tally_result,
                                          'std_dev':spectra_tally_std_dev,
                                          'energy_groups':list(energy_bins)}                    


    spectra_tally = sp.get_tally(name='breeder_blanket_spectra')
    spectra_tally_result = [entry[0][0] for entry in spectra_tally.mean] 
    spectra_tally_std_dev = [entry[0][0] for entry in spectra_tally.std_dev] 

    json_output['breeder_blanket_spectra']={'value':spectra_tally_result,
                                            'std_dev':spectra_tally_std_dev,
                                            'energy_groups':list(energy_bins)}         


    spectra_tally = sp.get_tally(name='vacuum_vessel_spectra')
    spectra_tally_result = [entry[0][0] for entry in spectra_tally.mean] 
    spectra_tally_std_dev = [entry[0][0] for entry in spectra_tally.std_dev] 

    json_output['vacuum_vessel_spectra']={'value':spectra_tally_result,
                                          'std_dev':spectra_tally_std_dev,
                                          'energy_groups':list(energy_bins)}                                                                                                                                              

    
    return json_output







natural_enrichment_fraction=0.07589
#comparison TBR simulations values with https://link.springer.com/article/10.1023/B:JOFE.0000021555.70423.f1



results = []
num_sims = 500
output_filename= 'simulation_results'+str(num_sims)+'.json'
with open(output_filename, mode='w', encoding='utf-8') as f:
    json.dump(results, f)

for i in tqdm(range(0,num_sims)):
    breeder_material_name = random.choice(['Li4SiO4', 'F2Li2BeF2', 'Li', 'Pb84.2Li15.8'])
    enrichment_fraction = random.uniform(0, 1)
    inner_radius = random.uniform(1, 500)
    thickness = random.uniform(1, 500)
    result = make_materials_geometry_tallies(batches=2,
                                             nps=1500000,
                                             enrichment_fraction=enrichment_fraction,
                                             inner_radius=inner_radius,
                                             thickness=thickness,
                                             breeder_material_name = breeder_material_name, 
                                             temperature_in_C=500
                                             )
    results.append(result)

    with open(output_filename, mode='w', encoding='utf-8') as f:
        #results.append(result)
        json.dump(results, f)




