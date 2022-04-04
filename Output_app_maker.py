import dash
import pandas as pd
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import json

import Functions
import Pagelayouts
from callbacks import get_callbacks
import main_simulation
import plottingfunctions
import Load_settings

#https://www.youtube.com/watch?v=hSPmj7mK6ng

settingdistibution_dict = Load_settings.load_settings()

finished_orders_df, measures, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions, totaltime = main_simulation.runsimulation(settingdistibution_dict)
print('huh')

sortfinisheddf = finished_orders_df.sort_values('total process time', ascending=False)

## MAKE APP


external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets
                )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='finishedorderdf', storage_type='session', data = finished_orders_df.to_json(orient="split")),
    dcc.Store(id='measures', storage_type='session', data = measures),
    dcc.Store(id='means', storage_type='session', data = means),
    dcc.Store(id='lower_5_quantiles', storage_type='session', data = lower_5_quantiles),
    dcc.Store(id='upper_95_quantiles', storage_type='session', data = upper_95_quantiles),
    dcc.Store(id='fig_total_thoughout_time', storage_type='session', data=fig_total_thoughout_time),
    dcc.Store(id='fig_queue_time_staal_buigen', storage_type='session', data=fig_queue_time_staal_buigen),
    dcc.Store(id='fig_queue_time_staal_koppelen', storage_type='session', data=fig_queue_time_staal_koppelen),
    dcc.Store(id='fig_queue_time_omhulsel_maken', storage_type='session', data=fig_queue_time_omhulsel_maken),
    dcc.Store(id='fig_total_queue_time', storage_type='session', data=fig_total_queue_time),
    dcc.Store(id='fig_gantt_disruptions', storage_type='session', data=fig_gantt_disruptions),
    dcc.Store(id='totaltime', storage_type='session', data=totaltime),
    dcc.Store(id='settingdistibution_dict', storage_type='session', data=settingdistibution_dict),
    dcc.Store(id='sortfinisheddf', storage_type='session', data=sortfinisheddf.to_json(orient="split")),

])

get_callbacks(app,settingdistibution_dict,  finished_orders_df, measures, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions, totaltime, sortfinisheddf)
print('heeeeeeeeyy')
if __name__ == '__main__':
    app.run_server()