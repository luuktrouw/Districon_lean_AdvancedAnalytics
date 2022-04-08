import dash
import pandas as pd
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import Plotting_functions_Management
import Plotting_functions_Settings
import Plotting_functions_Inventory
import Plotting_functions_Leadtimes
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import json

import Functions
import Pagelayouts
from callbacks import get_callbacks
import main_simulation
import Plotting_functions_Extra
import Load_inputsettings

settingdistibution_dict = Load_inputsettings.load_settings()

finished_orders_df, measures, totaltime = main_simulation.runsimulation(settingdistibution_dict)

Mananger_fig_dict = Plotting_functions_Management.get_Management_figures(finished_orders_df)

Settings_fig_dict = Plotting_functions_Settings.get_Settings_figures(settingdistibution_dict)

Inventory_fig_dict = Plotting_functions_Inventory.get_Inventory_figures(measures, totaltime)

Leadtimes_fig_dict = Plotting_functions_Leadtimes.get_Leadtimes_figures(finished_orders_df, measures)

sortfinisheddf = finished_orders_df.sort_values('total process time', ascending=False)

## MAKE APP

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets
                )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # change to 1 loading met als children al die Stores ipv elke apart)
    dcc.Loading(
                children= [
                            html.Div([html.Div(id='page-content')]),
                            html.Div([dcc.Store(id='finishedorderdf', storage_type='session', data = finished_orders_df.to_json(orient="split")),]),
                            html.Div([dcc.Store(id='measures', storage_type='session', data = measures),]),
                            html.Div([dcc.Store(id='totaltime', storage_type='session', data=totaltime),]),
                            html.Div([dcc.Store(id='settingdistibution_dict', storage_type='session', data=settingdistibution_dict),]),
                            html.Div([dcc.Store(id='sortfinisheddf', storage_type='session', data=sortfinisheddf.to_json(orient="split")),]),
                            html.Div([dcc.Store(id='Mananger_fig_dict', storage_type='session', data=Mananger_fig_dict),]),
                            html.Div([dcc.Store(id='Settings_fig_dict', storage_type='session', data=Settings_fig_dict),]),
                            html.Div([dcc.Store(id='Inventory_fig_dict', storage_type='session', data=Inventory_fig_dict),]),
                            html.Div([dcc.Store(id='Leadtimes_fig_dict', storage_type='session', data=Leadtimes_fig_dict),]),
                          ],
                type = 'circle',
                fullscreen= True
                )
])

get_callbacks(app)

if __name__ == '__main__':
    app.run_server()