#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry with neutron flux."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt
import os
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout
import json
import numpy as np

def make_materials(enrichment_fraction,breeder_material_name,temperature_in_C):

    #density data from http://aries.ucsd.edu/LIB/PROPS/PANOS/matintro.html
    
    natural_breeder_material =     openmc.Material(2, "natural_breeder_material") 
    breeder_material =     openmc.Material(1, "breeder_material") 

    if breeder_material_name == 'PbLi':

        #Pb84.2Li15.8 is the eutectic ratio, this could be a varible
        Lead_atom_ratio = 84.2
        Lithium_atom_ratio = 15.8
        
        density_of_natural_material_at_temperature = 99.90*(0.1-16.8e-6*temperature_in_C) #valid for in the range 240-350 C. source http://aries.ucsd.edu/LIB/PROPS/PANOS/lipb.html

        natural_breeder_material.add_element('Pb', Lead_atom_ratio,'ao') 
        natural_breeder_material.add_element('Li', Lithium_atom_ratio, 'ao')
        natural_breeder_material.set_density('g/cm3',density_of_natural_material_at_temperature) 
        atom_densities_dict = natural_breeder_material.get_nuclide_atom_densities()
        atoms_per_barn_cm = sum([i[1] for i in atom_densities_dict.values()])

        breeder_material.add_element('Pb', Lead_atom_ratio,'ao') 
        breeder_material.add_nuclide('Li6', enrichment_fraction*Lithium_atom_ratio, 'ao')
        breeder_material.add_nuclide('Li7', (1.0-enrichment_fraction)*Lithium_atom_ratio, 'ao')
        breeder_material.set_density('atom/b-cm',atoms_per_barn_cm) 


    if breeder_material_name == 'Flibe':
        #Li2BeF4 made from 2(FLi):BeF2 is the eutectic ratio, this could be a varible
        FLi_atom_ratio = 2.0
        BeF_atom_ratio = 1.0

        density_of_natural_material_at_temperature = 2.214 - 4.2e-4 * temperature_in_C # source http://aries.ucsd.edu/LIB/MEETINGS/0103-TRANSMUT/gohar/Gohar-present.pdf

        natural_breeder_material.add_element('Li', 1.0*FLi_atom_ratio, 'ao')
        natural_breeder_material.add_element('F', 1.0*FLi_atom_ratio,'ao')
        natural_breeder_material.add_element('Be', 1.0*BeF_atom_ratio,'ao')
        natural_breeder_material.add_element('F', 2.0*BeF_atom_ratio,'ao')
        natural_breeder_material.set_density('g/cm3',density_of_natural_material_at_temperature)  
        atom_densities_dict = natural_breeder_material.get_nuclide_atom_densities()
        atoms_per_barn_cm = sum([i[1] for i in atom_densities_dict.values()])
 
        breeder_material.add_nuclide('Li6', enrichment_fraction*1.0*FLi_atom_ratio, 'ao')
        breeder_material.add_nuclide('Li7', (1.0-enrichment_fraction)*1.0*FLi_atom_ratio, 'ao')
        breeder_material.add_element('F', 1.0*FLi_atom_ratio,'ao')
        breeder_material.add_element('Be', 1.0*BeF_atom_ratio,'ao')
        breeder_material.add_element('F', 2.0*BeF_atom_ratio,'ao')
        breeder_material.set_density('atom/b-cm',atoms_per_barn_cm)  

    if breeder_material_name == 'Li':

        density_of_natural_material_at_temperature = 0.515 - 1.01e-4 * (temperature_in_C - 200) # valid between 200 - 1600 C source http://aries.ucsd.edu/LIB/PROPS/PANOS/li.html
        
        natural_breeder_material.add_element('Li', 1.0,'ao')
        natural_breeder_material.set_density('g/cm3',density_of_natural_material_at_temperature)
        atom_densities_dict = natural_breeder_material.get_nuclide_atom_densities()
        atoms_per_barn_cm = sum([i[1] for i in atom_densities_dict.values()])

        breeder_material.add_nuclide('Li6', enrichment_fraction*1.0, 'ao')
        breeder_material.add_nuclide('Li7', (1.0-enrichment_fraction)*1.0, 'ao')  
        breeder_material.set_density('atom/b-cm',atoms_per_barn_cm) 
        
    mats = openmc.Materials([breeder_material])
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
    tbr_tally = openmc.Tally(1,name='TBR')
    tbr_tally.filters = [cell_filter]
    tbr_tally.scores = ['205']
    tallies.append(tbr_tally)

    surface_filter = openmc.SurfaceFilter(breeder_blanket_outer_surface)
    leak_tally = openmc.Tally(2,name='Leakage')
    leak_tally.filters = [surface_filter]
    leak_tally.scores = ['current']
    tallies.append(leak_tally)

    #RUN OPENMC #
    model = openmc.model.Model(geom, mats, sett, tallies)
    model.run()
    sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

    tbr_tally = sp.get_tally(name='TBR')
    tbr_tally_result = tbr_tally.sum[0][0][0]/batches #for some reason the tally sum is a nested list 
    tbr_tally_std_dev = tbr_tally.std_dev[0][0][0]/batches #for some reason the tally std_dev is a nested list 

    leak_tally = sp.get_tally(name='Leakage')
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

enrichment_fraction=0.07589
#comparison TBR simulations https://link.springer.com/article/10.1023/B:JOFE.0000021555.70423.f1
results=[]
for enrichment_fraction in np.linspace(start=0,stop=1,num=40):
    results.append(make_materials_geometry_tallies(batches=2,
                                                   enrichment_fraction=enrichment_fraction,
                                                   inner_radius=500,
                                                   thickness=100,
                                                   breeder_material_name = 'Flibe', #Flibe or Li or PbLi
                                                   temperature_in_C=300
                                                   ))

print(results)
with open('simulation_results.json', 'w') as file_object:
    json.dump(results, file_object)

# PLOTS RESULTS #
trace1= Scatter(x=[entry['enrichment_fraction'] for entry in results], 
                y=[entry['tbr_tally'] for entry in results],
                mode = 'lines',
                name = 'tbr_tally',                
                error_y= {'array':[entry['tbr_tally_std_dev'] for entry in results]},
                )

trace2= Scatter(x=[entry['enrichment_fraction'] for entry in results], 
                y=[entry['leak_tally'] for entry in results],
                mode = 'lines',
                name = 'leak_tally',
                error_y= {'array':[entry['leak_tally_st_dev'] for entry in results]},
                )                

layout = {'title':'Tritium production and neutron leakage',
          'xaxis':{'title':'Li6 enrichment fraction'},
          'yaxis':{'title':'TBR'},
         }
plot({'data':[trace1,trace2],
      'layout':layout})

