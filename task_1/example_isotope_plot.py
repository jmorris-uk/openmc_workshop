#!/usr/bin/env python3

"""example_isotope_plot.py: plots cross sections for a couple of isotopes."""

__author__      = "Jonathan Shimwell"

import openmc
from plotly import __version__
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout




Pb208_isotope = openmc.Material()
Pb208_isotope.add_nuclide('Pb208',1.0,percent_type='ao')

Pb207_isotope = openmc.Material()
Pb207_isotope.add_nuclide('Pb207',1.0,percent_type='ao')

Endf_MT_number = [16]

Energy_Pb207_MT16, data = openmc.calculate_cexs(Pb207_isotope, 'material', Endf_MT_number )
cross_section_Pb207_MT16 = data[0]

Energy_Pb208_MT16, data = openmc.calculate_cexs(Pb208_isotope, 'material', Endf_MT_number )
cross_section_Pb208_MT16 = data[0]

trace1= Scatter(x=Energy_Pb208_MT16, 
                y=cross_section_Pb208_MT16, 
                mode = 'lines', 
                name='Pb208(n,2n)')

trace2= Scatter(x=Energy_Pb207_MT16, 
                y=cross_section_Pb207_MT16, 
                mode = 'lines', 
                name='Pb208(n,2n)')

layout = {'title':'Isotope cross sections',
          'xaxis':{'title':'Energy (eV)',
                   'range':(0,14.1e6)},
          'yaxis':{'title':'Cross section (barns)'},
         }

plot({'data':[trace1,trace2],
      'layout':layout})

