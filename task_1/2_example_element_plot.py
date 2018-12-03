#!/usr/bin/env python3

"""example_isotope_plot.py: plots cross sections for a couple of elements with natural abundance."""

__author__      = "Jonathan Shimwell"

import openmc
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout
from tqdm import tqdm

all_stable_elements = ['Ag', 'Al', 'Ar', 'As', 'Au', 'B', 'Ba', 'Be', 'Bi', 'Br', 'C', 'Ca', 'Cd', 'Ce', 'Cl', 'Co', 'Cr', 'Cs', 'Cu', 'Dy', 'Er', 'Eu', 'F', 'Fe', 'Ga', 'Gd', 'Ge', 'H', 'He', 'Hf', 'Hg', 'Ho', 'I', 'In', 'Ir', 'K', 'Kr', 'La', 'Li', 'Lu', 'Mg', 'Mn', 'Mo', 'N', 'Na', 'Nb', 'Nd', 'Ne', 'Ni', 'O', 'Os', 'P', 'Pa', 'Pb', 'Pd','Po', 'Pr', 'Pt', 'Rb', 'Re', 'Rh', 'Rn', 'Ru', 'S', 'Sb', 'Sc', 'Se', 'Si', 'Sm', 'Sn', 'Sr', 'Ta', 'Tb', 'Te', 'Th', 'Ti', 'Tl', 'Tm', 'U', 'V', 'W', 'Xe', 'Y', 'Yb', 'Zn', 'Zr']
Endf_MT_number = [16] # MT number 16 is (n,n2) reaction, MT 205 is (n,t)
traces=[]


for element_name in tqdm(all_stable_elements):
      try:
            element_object = openmc.Material()
            # this material defaults to a density of 1g/cm3
            element_object.add_element(element_name,1.0,percent_type='ao')
            energy, data = openmc.calculate_cexs(element_object, 'material', Endf_MT_number )
            cross_section = data[0]

            traces.append(Scatter(x=energy, 
                              y=cross_section, 
                              mode = 'lines', 
                              name=element_name+' MT '+str(Endf_MT_number[0]))
                        )
      except:
            print('element failed ',element_name)


layout = {'title':'Element cross sections'+ str(Endf_MT_number[0]),
          'xaxis':{'title':'Energy (eV)',
                   'range':(0,14.1e6)},
          'yaxis':{'title':'Cross section (barns)'},
          'hovermode':'closest'
         }

plot({'data':traces,
      'layout':layout},
      filename='2_example_element_plot.html')


