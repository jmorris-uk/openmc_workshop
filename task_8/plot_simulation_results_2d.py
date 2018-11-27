#!/usr/bin/env python3

"""simulation_results_plot.py: plots few 2D views of TBR and leakage."""

__author__      = "Jonathan Shimwell"


from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout
import json
import pandas as pd

with open('simulation_results.json') as f:
    results = json.load(f)

# PLOTS RESULTS #

results_df = pd.DataFrame(results)

flibe = results_df[results_df['breeder_material_name']=='Flibe']
Li = results_df[results_df['breeder_material_name']=='Li']
PbLi = results_df[results_df['breeder_material_name']=='PbLi']

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






traces_ef=[]
traces_ef.append( Scatter(x=flibe['enrichment_fraction'], 
                       y=flibe['tbr_tally'] ,
                       mode = 'markers',
                       hoverinfo='text' ,
                       text=text_value_flibe,                       
                       name = 'FLiBe',                
                       error_y= {'array':flibe['tbr_tally_std_dev']},
                       )
              )

traces_ef.append( Scatter(x=Li['enrichment_fraction'], 
                       y=Li['tbr_tally'] ,
                       mode = 'markers',
                       hoverinfo='text' ,
                       text=text_value_li,                       
                       name = 'Li',                
                       error_y= {'array':Li['tbr_tally_std_dev']},
                       )
              )

traces_ef.append( Scatter(x=PbLi['enrichment_fraction'], 
                       y=PbLi['tbr_tally'] ,
                       mode = 'markers',
                       hoverinfo='text' ,
                       text=text_value_PbLi,                       
                       name = 'PbLi',                
                       error_y= {'array':PbLi['tbr_tally_std_dev']},
                       )
              ) 

layout_ef = {'title':'Tritium production and Li6 enrichment fraction',
            'hovermode':'closest',
          'xaxis':{'title':'Li6 enrichment fraction'},
          'yaxis':{'title':'TBR'},
         }
plot({'data':traces_ef,
      'layout':layout_ef},
      filename='TBR_vs_erichment_fraction.html'
      )







traces_ir=[]
traces_ir.append( Scatter(x=flibe['inner_radius'], 
                       y=flibe['tbr_tally'] ,
                       mode = 'markers',
                       hoverinfo='text' ,
                       text=text_value_flibe,                          
                       name = 'FLiBe',                
                       error_y= {'array':flibe['tbr_tally_std_dev']},
                       )
              )

traces_ir.append( Scatter(x=Li['inner_radius'], 
                       y=Li['tbr_tally'] ,
                       mode = 'markers',
                       hoverinfo='text' ,
                       text=text_value_li,                          
                       name = 'Li',                
                       error_y= {'array':Li['tbr_tally_std_dev']},
                       )
              )

traces_ir.append( Scatter(x=PbLi['inner_radius'], 
                       y=PbLi['tbr_tally'] ,
                       mode = 'markers',
                       hoverinfo='text' ,
                       text=text_value_PbLi,                          
                       name = 'PbLi',                
                       error_y= {'array':PbLi['tbr_tally_std_dev']},
                       )
              ) 

layout_ir = {'title':'Tritium production and inner radius',
            'hovermode':'closest',
          'xaxis':{'title':'inner_radius'},
          'yaxis':{'title':'TBR'},
         }
plot({'data':traces_ir,
      'layout':layout_ir},
      filename='TBR_vs_inner_radius.html')







traces_t=[]
traces_t.append( Scatter(x=flibe['thickness'], 
                       y=flibe['tbr_tally'] ,
                       mode = 'markers',
                       hoverinfo='text' ,
                       text=text_value_flibe,                          
                       name = 'FLiBe',                
                       error_y= {'array':flibe['tbr_tally_std_dev']},
                       )
              )

traces_t.append( Scatter(x=Li['thickness'], 
                       y=Li['tbr_tally'] ,
                       mode = 'markers',
                       hoverinfo='text' ,
                       text=text_value_li,                          
                       name = 'Li',                
                       error_y= {'array':Li['tbr_tally_std_dev']},
                       )
              )

traces_t.append( Scatter(x=PbLi['thickness'], 
                       y=PbLi['tbr_tally'] ,
                       mode = 'markers',
                       hoverinfo='text' ,
                       text=text_value_PbLi,                          
                       name = 'PbLi',                
                       error_y= {'array':PbLi['tbr_tally_std_dev']},
                       )
              ) 

layout_t = {'title':'Tritium production and thickness',
            'hovermode':'closest',
            'xaxis':{'title':'thickness'},
            'yaxis':{'title':'TBR'},
            }
plot({'data':traces_t,
      'layout':layout_t},
      filename='TBR_vs_thickness.html')
