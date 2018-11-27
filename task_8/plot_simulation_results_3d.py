#!/usr/bin/env python3

"""simulation_results_plot.py: plots few 2D views of TBR and leakage."""

__author__      = "Jonathan Shimwell"


from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter3d, Layout, Scatter
import json
import pandas as pd
import numpy as np

with open('simulation_results.json') as f:
    results = json.load(f)

# PLOTS RESULTS #

results_df = pd.DataFrame(results)


flibe = results_df[results_df['breeder_material_name']=='F2Li2BeF2']
Li = results_df[results_df['breeder_material_name']=='Li']
PbLi = results_df[results_df['breeder_material_name']=='Pb84.2Li15.8']

text_value_flibe = []
for e,t,i,tbr in zip(flibe['enrichment_fraction'],flibe['thickness'],flibe['inner_radius'],flibe['tbr_tally']):
    text_value_flibe.append('TBR =' +str(tbr)+'<br>'+
                      'enrichment fraction ='+str(e) +'<br>'+
                      'thickness ='+str(t) +'<br>'+
                      'inner radius ='+str(i)                                            
                      )

text_value_li = []
for e,t,i,tbr in zip(Li['enrichment_fraction'],Li['thickness'],Li['inner_radius'],Li['tbr_tally']):
    text_value_li.append('TBR =' +str(tbr)+'<br>'+
                      'enrichment fraction ='+str(e) +'<br>'+
                      'thickness ='+str(t) +'<br>'+
                      'inner radius ='+str(i)                                            
                      )

text_value_PbLi = []
for e,t,i,tbr in zip(PbLi['enrichment_fraction'],PbLi['thickness'],PbLi['inner_radius'],PbLi['tbr_tally']):
    text_value_PbLi.append('TBR =' +str(tbr)+'<br>'+
                      'enrichment fraction ='+str(e) +'<br>'+
                      'thickness ='+str(t) +'<br>'+
                      'inner radius ='+str(i)                                            
                      )                      

# total_tbr_values_flibe = sum(flibe['tbr_tally'])
# color_scale_flibe = [float(i)/total_tbr_values_flibe for i in flibe['tbr_tally']]

# total_tbr_values_li = sum(Li['tbr_tally'])
# color_scale_li = [float(i)/total_tbr_values_li for i in Li['tbr_tally']]

# total_tbr_values_PbLi = sum(PbLi['tbr_tally'])
# color_scale_pbli = [float(i)/total_tbr_values_PbLi for i in PbLi['tbr_tally']]

print(len(list(flibe['tbr_tally'])))

traces=[]
traces.append( Scatter3d(x=list(flibe['enrichment_fraction']), 
                       y=list(flibe['thickness']),
                       z=list(flibe['inner_radius']),
                       mode = 'markers',
                       name = 'FLiBe',
                       hoverinfo='text' ,
                       text=text_value_flibe,
                       visible=False,
                       marker={'color':list(flibe['tbr_tally']),
                               'colorscale':'Viridis',
                               'size':2,
                               'colorbar':{'title':'TBR',
                                           'tickvals':np.linspace(start=min(list(flibe['tbr_tally'])),stop=max(list(flibe['tbr_tally'])),num=10)
                                            }
                               },
                       
                       )
              )

traces.append( Scatter3d(x=list(Li['enrichment_fraction']), 
                       y=list(Li['thickness']),
                       z=list(Li['inner_radius']),
                       mode = 'markers',
                       name = 'Li',
                       hoverinfo='text' ,
                       text=text_value_li,
                       visible=False,                       
                       marker={'color':list(Li['tbr_tally']),
                               'colorscale':'Viridis',
                               'size':2,
                               'colorbar':{'title':'TBR',
                                           'tickvals':np.linspace(start=min(list(Li['tbr_tally'])),stop=max(list(Li['tbr_tally'])),num=10)
                                            }
                               }
                       
                       )
              )

traces.append( Scatter3d(x=list(Li['enrichment_fraction']), 
                       y=list(PbLi['thickness']),
                       z=list(PbLi['inner_radius']),
                       mode = 'markers',
                       name = 'PbLi',
                       hoverinfo='text' ,
                       text=text_value_PbLi,
                       visible=False,                       
                       marker={'color':list(PbLi['tbr_tally']),
                               'colorscale':'Viridis',
                               'size':2,
                               'colorbar':{'title':'TBR',
                                           'tickvals':np.linspace(start=min(list(PbLi['tbr_tally'])),stop=max(list(PbLi['tbr_tally'])),num=10)
                                            }
                               }
                       
                       )
              )


layout = {'title':'Select a material',
          'hovermode':'closest',
          'scene':{'xaxis':{'title':'Li6 Enrichment Fraction'},
                   'yaxis':{'title':'Thickness'},
                   'zaxis':{'title':'Inner radius'}
          }
         }



updatemenus=list([
    dict(
        buttons=list([   
            dict(
                args=[{'visible': [False, False, False]},
                      {'title':''}
                      ],
                label='Select one',
                method='update'
            ),  
            dict(
                args=[{'visible': [True, False, False]},
                      {'title':'Tritium production and neutron leakage with FLiBe'}
                      ],
                label='Flibe',
                method='update'
            ),            
            dict(
                args=[{'visible': [False, True, False]},
                      {'title':'Tritium production and neutron leakage with Li'}
                      ],
                label='Li',
                method='update'
            ),
            dict(
                args=[{'visible': [False, False, True]},
                      {'title':'Tritium production and neutron leakage with PbLi'}
                      ],
                label='PbLi',
                method='update'
            )                              
        ]),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0.1,
        xanchor = 'left',
        y = 1.1,
        yanchor = 'top' 
    ),
])

annotations = list([
    dict(text='Breeder material:', x=0, y=1.085, yref='paper', align='left', showarrow=False)
])
layout['updatemenus'] = updatemenus
layout['annotations'] = annotations


plot({'data':traces,
      'layout':layout},
      filename='TBR_for_different_materials.html')