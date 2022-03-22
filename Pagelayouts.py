from Output_app_maker import app
from dash.dependencies import Input, Output

import dash_core_components as dcc
import dash_html_components as html

import dash
import pandas as pd
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import Functions
import main_simulation
import plottingfunctions
import Load_settings

def makeinventory_rows()
    row1_inventory = dbc.Row(
        [
            dbc.Col(dcc.Graph(id = 'speelveld',figure =  fig_table_speelveld)),
            dbc.Col(dcc.Graph(id = 'speelveld',figure =  fig_table_speelveld)),
        ],
        className="mb-4",
    )
    row2_inventory = dbc.Row(
        [
            dcc.Dropdown(id='select stock graph', options=[{'label': 'raw material - stalen stangen', 'value': ['raw materials','stalen stangen']},
                                                           {'label': 'raw material - koppeldraad', 'value': ['raw materials','koppeldraad']},
                                                           {'label': 'raw material - soft stuffing', 'value': ['raw materials','soft stuffing']},
                                                           {'label': 'raw material - medium stuffing', 'value': ['raw materials','medium stuffing']},
                                                           {'label': 'raw material - hard stuffing', 'value': ['raw materials','hard stuffing']},
                                                           {'label': 'subassembly - gebogen stangen', 'value': ['subassemblies','gebogen stangen']},
                                                           {'label': 'subassembly - gekoppeld eenpersoons', 'value': ['subassemblies','gekoppeld eenpersoons']},
                                                           {'label': 'subassembly - gekoppeld twijfelaar', 'value': ['subassemblies','gekoppeld twijfelaar']},
                                                           {'label': 'subassembly - gekoppeld queensize', 'value': ['subassemblies','gekoppeld queensize']},
                                                           {'label': 'subassembly - gekoppeld kingsize', 'value': ['subassemblies','gekoppeld kingsize']}
                                                           ], multi=False,
                 value=['raw materials','stalen stangen'], style={'width': '100%'}),
        ],
        className="mb-4",
    )
    row3_inventory = dbc.Row(
        [
            dbc.Col(dcc.Graph(id = 'stock level graph', figure ={}),),
        ],
        className="mb-4",
    )
    return row1_inventory, row2_inventory, row3_inventory

@app.callback(Output(component_id= 'stock level graph', component_property= 'figure'),
              [Input(component_id='select stock graph', component_property= 'value')])
def update_stocklevelsgraph(option_slctd):
    #if text in finished_orders_df['orderID']:
    print(option_slctd)
    figure = plottingfunctions.plot_stocklevels_through_time(measures['stock levels'][option_slctd[0]][option_slctd[1]])
    return figure