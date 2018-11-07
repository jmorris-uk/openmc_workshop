#!/usr/bin/env python3

"""example_isotope_plot.py: plots cross sections for a couple of isotopes."""

__author__      = "Jonathan Shimwell"

import openmc
from plotly import __version__
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout




Be_element = openmc.Material()
Be_element.add_element('Be',1.0,percent_type='ao')

Pb_element = openmc.Material()
Pb_element.add_element('Pb',1.0,percent_type='ao')

Endf_MT_number = [16]

Energy_Pb_MT16, data = openmc.calculate_cexs(Pb_element, 'material', Endf_MT_number )
cross_section_Pb_MT16 = data[0]

Energy_Be_MT16, data = openmc.calculate_cexs(Be_element, 'material', Endf_MT_number )
cross_section_Be_MT16 = data[0]

trace1= Scatter(x=Energy_Be_MT16, 
                y=cross_section_Be_MT16, 
                mode = 'lines', 
                name='Be(n,2n)')

trace2= Scatter(x=Energy_Pb_MT16, 
                y=cross_section_Pb_MT16, 
                mode = 'lines', 
                name='Pb(n,2n)')

layout = {'title':'Element cross sections',
          'xaxis':{'title':'Energy (eV)',
                   'range':(0,14.1e6)},
          'yaxis':{'title':'Cross section (barns)'},
         }

plot({'data':[trace1,trace2],
      'layout':layout})


#example_element.set_density('g/cm3', 11.34)

