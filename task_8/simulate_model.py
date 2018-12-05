#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry with neutron flux."""
""" run with python3 simulate_sphere_model.py | tqdm >> /dev/null """

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

def make_materials_geometry_tallies(batches,enrichment_fraction,inner_radius,thickness,breeder_material_name,temperature_in_C):
    #print('simulating ',batches,enrichment_fraction,inner_radius,thickness,breeder_material_name)

    #MATERIALS#
    breeder_material = make_breeder_materials(enrichment_fraction,breeder_material_name,temperature_in_C)
    eurofer, copper = make_materials()
    mats = openmc.Materials([breeder_material,eurofer, copper])


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
    # breeder_blanket_cell.fill = eurofer

    # universe = openmc.Universe(cells=[central_sol_cell,central_shield_cell,first_wall_cell, breeder_blanket_cell])


    breeder_blanket_inner_surface = openmc.Sphere(R=inner_radius)
    breeder_blanket_outer_surface = openmc.Sphere(R=inner_radius+thickness,boundary_type='vacuum')

    breeder_blanket_region = -breeder_blanket_outer_surface & +breeder_blanket_inner_surface
    breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region) 
    breeder_blanket_cell.fill = breeder_material
    breeder_blanket_cell.name = 'breeder_blanket'

    inner_vessel_region = -breeder_blanket_inner_surface 
    inner_vessel_cell = openmc.Cell(region=inner_vessel_region) 
    inner_vessel_cell.name = 'inner_vessel'

    universe = openmc.Universe(cells=[inner_vessel_cell, breeder_blanket_cell])


    geom = openmc.Geometry(universe)

    #SIMULATION SETTINGS#

    sett = openmc.Settings()
    # batches = 3
    sett.batches = batches
    sett.inactive = 1
    sett.particles = 5000
    sett.run_mode = 'fixed source'

    source = openmc.Source()
    source.space = openmc.stats.Point((0,0,0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Discrete([14.08e6], [1])
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

    surface_filter = openmc.SurfaceFilter(breeder_blanket_outer_surface)
    spectra_tally = openmc.Tally(3,name='rear_neutron_spectra')
    particle_filter = openmc.ParticleFilter([1])
    #group strucutre 315 from https://github.com/fispact/pypact/blob/master/pypact/input/groupstructures.py
    energy_bins = [1e-05,0.00011,0.003,0.0055,0.01,0.015,0.02,0.03,0.032,0.03238,0.043,0.059,0.077,0.095,0.1,0.115,0.134,0.16,0.189,0.22,0.248,0.2825,0.3145,0.352,0.391,0.414,0.433,0.485,0.5316,0.54,0.625,0.6826,0.705,0.79,0.86,0.8764,0.93,0.986,1.01,1.035,1.07,1.08,1.09,1.11,1.125,1.17,1.235,1.305,1.37,1.44,1.445,1.51,1.59,1.67,1.755,1.84,1.855,1.93,2.02,2.13,2.36,2.372,2.768,3.059,3.381,3.928,4.129,4.47,4.67,5.043,5.623,6.16,6.476,7.079,7.524,7.943,8.315,8.913,9.19,10.0,10.68,11.22,12.59,13.71,15.23,16.74,17.6,19.03,20.45,22.6,24.98,27.92,29.2,30.51,33.89,37.27,39.81,45.52,47.85,50.12,55.59,61.44,63.1,67.9,70.79,78.89,85.28,91.66,101.3,112.2,130.1,136.7,158.5,167.0,177.8,204.0,214.5,243.0,275.4,304.3,353.6,398.1,454.0,514.5,583.0,631.0,677.3,707.9,748.5,848.2,961.1,1010.0,1117.0,1234.0,1364.0,1507.0,1585.0,1796.0,2035.0,2113.0,2249.0,2371.0,2485.0,2613.0,2661.0,2747.0,2818.0,3035.0,3162.0,3355.0,3548.0,3707.0,3981.0,4307.0,4643.0,5004.0,5531.0,6267.0,7102.0,7466.0,8251.0,9119.0,10080.0,11140.0,11710.0,12730.0,13830.0,15030.0,15850.0,16620.0,17780.0,19310.0,19950.0,20540.0,21130.0,21870.0,22390.0,23040.0,23580.0,24180.0,24410.0,24790.0,25120.0,25850.0,26060.0,26610.0,27000.0,27380.0,28180.0,28500.0,29010.0,29850.0,30730.0,31620.0,31830.0,34310.0,36980.0,40870.0,43590.0,46310.0,49390.0,52480.0,55170.0,56560.0,61730.0,67380.0,72000.0,74990.0,79500.0,82300.0,82500.0,86520.0,98040.0,111100.0,116800.0,122800.0,129100.0,135700.0,142600.0,150000.0,157600.0,165700.0,174200.0,183200.0,192500.0,202400.0,212800.0,223700.0,235200.0,247200.0,273200.0,287300.0,294500.0,297200.0,298500.0,302000.0,333700.0,368800.0,387700.0,407600.0,450500.0,523400.0,550200.0,578400.0,608100.0,639300.0,672100.0,706500.0,742700.0,780800.0,820900.0,862900.0,907200.0,961600.0,1003000.0,1108000.0,1165000.0,1225000.0,1287000.0,1353000.0,1423000.0,1496000.0,1572000.0,1653000.0,1738000.0,1827000.0,1921000.0,2019000.0,2122000.0,2231000.0,2307000.0,2346000.0,2365000.0,2385000.0,2466000.0,2592000.0,2725000.0,2865000.0,3012000.0,3166000.0,3329000.0,3679000.0,4066000.0,4493000.0,4724000.0,4966000.0,5220000.0,5488000.0,5769000.0,6065000.0,6376000.0,6592000.0,6703000.0,7047000.0,7408000.0,7788000.0,8187000.0,8607000.0,9048000.0,9512000.0,10000000.0,10510000.0,11050000.0,11620000.0,12210000.0,12840000.0,13500000.0,13840000.0,14190000.0,14550000.0,14920000.0,15680000.0,16490000.0,16910000.0,17330000.0,19640000.0]
    energy_filter = openmc.EnergyFilter(energy_bins)
    spectra_tally.filters = [surface_filter,particle_filter,energy_filter]
    spectra_tally.scores = ['flux']
    tallies.append(spectra_tally)

    surface_filter = openmc.SurfaceFilter(breeder_blanket_inner_surface)
    spectra_tally = openmc.Tally(4,name='front_neutron_spectra')
    particle_filter = openmc.ParticleFilter([1])
    #group strucutre 315 from https://github.com/fispact/pypact/blob/master/pypact/input/groupstructures.py
    energy_bins = energy_bins # openmc.mgxs.GROUP_STRUCTURES['CASMO-70']   
    #315 [1e-05,0.00011,0.003,0.0055,0.01,0.015,0.02,0.03,0.032,0.03238,0.043,0.059,0.077,0.095,0.1,0.115,0.134,0.16,0.189,0.22,0.248,0.2825,0.3145,0.352,0.391,0.414,0.433,0.485,0.5316,0.54,0.625,0.6826,0.705,0.79,0.86,0.8764,0.93,0.986,1.01,1.035,1.07,1.08,1.09,1.11,1.125,1.17,1.235,1.305,1.37,1.44,1.445,1.51,1.59,1.67,1.755,1.84,1.855,1.93,2.02,2.13,2.36,2.372,2.768,3.059,3.381,3.928,4.129,4.47,4.67,5.043,5.623,6.16,6.476,7.079,7.524,7.943,8.315,8.913,9.19,10.0,10.68,11.22,12.59,13.71,15.23,16.74,17.6,19.03,20.45,22.6,24.98,27.92,29.2,30.51,33.89,37.27,39.81,45.52,47.85,50.12,55.59,61.44,63.1,67.9,70.79,78.89,85.28,91.66,101.3,112.2,130.1,136.7,158.5,167.0,177.8,204.0,214.5,243.0,275.4,304.3,353.6,398.1,454.0,514.5,583.0,631.0,677.3,707.9,748.5,848.2,961.1,1010.0,1117.0,1234.0,1364.0,1507.0,1585.0,1796.0,2035.0,2113.0,2249.0,2371.0,2485.0,2613.0,2661.0,2747.0,2818.0,3035.0,3162.0,3355.0,3548.0,3707.0,3981.0,4307.0,4643.0,5004.0,5531.0,6267.0,7102.0,7466.0,8251.0,9119.0,10080.0,11140.0,11710.0,12730.0,13830.0,15030.0,15850.0,16620.0,17780.0,19310.0,19950.0,20540.0,21130.0,21870.0,22390.0,23040.0,23580.0,24180.0,24410.0,24790.0,25120.0,25850.0,26060.0,26610.0,27000.0,27380.0,28180.0,28500.0,29010.0,29850.0,30730.0,31620.0,31830.0,34310.0,36980.0,40870.0,43590.0,46310.0,49390.0,52480.0,55170.0,56560.0,61730.0,67380.0,72000.0,74990.0,79500.0,82300.0,82500.0,86520.0,98040.0,111100.0,116800.0,122800.0,129100.0,135700.0,142600.0,150000.0,157600.0,165700.0,174200.0,183200.0,192500.0,202400.0,212800.0,223700.0,235200.0,247200.0,273200.0,287300.0,294500.0,297200.0,298500.0,302000.0,333700.0,368800.0,387700.0,407600.0,450500.0,523400.0,550200.0,578400.0,608100.0,639300.0,672100.0,706500.0,742700.0,780800.0,820900.0,862900.0,907200.0,961600.0,1003000.0,1108000.0,1165000.0,1225000.0,1287000.0,1353000.0,1423000.0,1496000.0,1572000.0,1653000.0,1738000.0,1827000.0,1921000.0,2019000.0,2122000.0,2231000.0,2307000.0,2346000.0,2365000.0,2385000.0,2466000.0,2592000.0,2725000.0,2865000.0,3012000.0,3166000.0,3329000.0,3679000.0,4066000.0,4493000.0,4724000.0,4966000.0,5220000.0,5488000.0,5769000.0,6065000.0,6376000.0,6592000.0,6703000.0,7047000.0,7408000.0,7788000.0,8187000.0,8607000.0,9048000.0,9512000.0,10000000.0,10510000.0,11050000.0,11620000.0,12210000.0,12840000.0,13500000.0,13840000.0,14190000.0,14550000.0,14920000.0,15680000.0,16490000.0,16910000.0,17330000.0,19640000.0]
    energy_filter = openmc.EnergyFilter(energy_bins)
    spectra_tally.filters = [surface_filter,particle_filter,energy_filter]
    spectra_tally.scores = ['flux']
    tallies.append(spectra_tally)

    cell_filter = openmc.CellFilter(breeder_blanket_cell)
    heat_tally = openmc.Tally(5,name='heat')
    heat_tally.filters = [cell_filter]
    heat_tally.scores = ['301'] #-4 for neutron heat, -6 for photon heat
    tallies.append(heat_tally)    
    # this returns 0 as 301 is missing from xs file

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

    rear_neutron_spectra_tally = sp.get_tally(name='rear_neutron_spectra')
    rear_neutron_spectra_tally_result = heat_tally.sum[0][0][0]/batches #for some reason the tally sum is a nested list 
    rear_neutron_spectra_tally_std_dev = heat_tally.std_dev[0][0][0]/batches #for some reason the tally std_dev is a nested list 

    front_neutron_spectra_tally = sp.get_tally(name='front_neutron_spectra')
    front_neutron_spectra_tally_result = heat_tally.sum[0][0][0]/batches #for some reason the tally sum is a nested list 
    front_neutron_spectra_tally_std_dev = heat_tally.std_dev[0][0][0]/batches #for some reason the tally std_dev is a nested list        

    print('heat_tally_result',heat_tally_result)

    return {'enrichment_fraction':enrichment_fraction,
            'tbr_tally':tbr_tally_result, 
            'tbr_tally_std_dev':tbr_tally_std_dev,
            'leak_tally':leak_tally_result,
            'leak_tally_std_dev':leak_tally_std_dev,
            'upper_energy_bin_neutron_spectra':energy_bins,
            'front_surface_neutron_spectra':front_neutron_spectra_tally_result,
            'rear_surface_neutron_spectra':rear_neutron_spectra_tally_result,
            'heat_tally':heat_tally_result,
            'heat_tally_std_dev':heat_tally_std_dev,
            'inner_radius':inner_radius,
            'thickness':thickness,
            'breeder_material_name':breeder_material_name,
            'temperature_in_C':temperature_in_C
           }







natural_enrichment_fraction=0.07589
#comparison TBR simulations https://link.springer.com/article/10.1023/B:JOFE.0000021555.70423.f1



results = []
num_sims = 2
for i in tqdm(range(0,num_sims)):
    breeder_material_name = random.choice(['Li4SiO4', 'F2Li2BeF2', 'Li', 'Pb84.2Li15.8'])
    enrichment_fraction = random.uniform(0, 1)
    inner_radius = random.uniform(1, 500)
    thickness = random.uniform(1, 500)
    result = make_materials_geometry_tallies(batches=10,
                                             enrichment_fraction=enrichment_fraction,
                                             inner_radius=inner_radius,
                                             thickness=thickness,
                                             breeder_material_name = breeder_material_name, 
                                             temperature_in_C=500
                                             )
    results.append(result)




with open('simulation_results'+str(num_sims)+'.json', 'w') as file_object:
    json.dump(results, file_object, indent=2)
       



