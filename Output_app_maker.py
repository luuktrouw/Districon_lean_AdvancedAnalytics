import dash
import pandas as pd
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import Functions
import Pagelayouts
from callbacks import get_callbacks
import main_simulation
import plottingfunctions
import Load_settings

#https://www.youtube.com/watch?v=hSPmj7mK6ng

#settingdistibution_dict = Load_settings.load_settings()

#### deze functie gebruikt handmatig ingevoerde getallen voor bill of materials
#settingdistibution_dict = Functions.calculateSafetyStocks(settingdistibution_dict)

##------------------------------------
### LOAD FIGURES


#finished_orders_df, measures, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions, totaltime = main_simulation.runsimulation(settingdistibution_dict)

#sortfinisheddf = finished_orders_df.sort_values('total process time', ascending=False)
#fig_some_order = plottingfunctions.plot_gantt_per_order(finished_orders_df, sortfinisheddf.iloc[0]['orderID'])

#fig_pie_chart_reasons_queue = plottingfunctions.plot_fractions_wait_time_reasons(finished_orders_df, 20)
#
# fig_order_deadlines_met = plottingfunctions.plot_fraction_deadlines_met(finished_orders_df)
#
# testt = finished_orders_df[finished_orders_df['high priority'] == True]
# if len(testt)>0:
#     figorderdeadlinesmet_priority = plottingfunctions.plot_fraction_deadlines_met(finished_orders_df[finished_orders_df['high priority'] == True])


#fig_stocklevels = plottingfunctions.plot_stocklevels_through_time(measures['stock levels']['raw materials']['stalen stangen'])

#fig_VSM_statistics = plottingfunctions.make_fig_VSM_statistics(means, lower_5_quantiles, upper_95_quantiles)

## ----------------------------------------------
## MAKE APP

#app = dash.Dash(__name__)

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets
                )

# app.layout = html.Div([
#             dbc.Row( dbc.Col(html.H1("Simulation results with the given settings", style={'text-align':'center'}),
#                      ),
#              ),
#
#             html.H1("Simulation results with the given settings", style={'text-align':'center'}),
#             # dcc.Dropdown(id='select speelvelddeel', options=[{'label': 'Total throughout time', 'value': 1}, {'label': 'Total queueing time', 'value': 2},
#             #                 {'label': 'Queueing time staal buigen', 'value': 3}, {'label': 'Queueing time staal koppelen', 'value': 4}, {'label': 'Queueing time omhulsel maken', 'value': 5}], multi=False,
#             #      value=1, style={'width': '100%'}),
#             dcc.Graph(id = 'speelveld',figure =  fig_table_speelveld),
#             dcc.Graph(id = 'orders met',figure =  fig_order_deadlines_met),
#             dcc.Graph(id='priority orders met', figure=figorderdeadlinesmet_priority),
#             dcc.Graph(id = 'VSMstatistics',figure =  fig_VSM_statistics),
#             dcc.Dropdown(id = 'select measure', options = [{'label': 'Total throughout time', 'value': 1},{'label': 'Total queueing time', 'value': 2},
#                           {'label': 'Queueing time staal buigen', 'value': 3},{'label': 'Queueing time staal koppelen', 'value': 4},{'label': 'Queueing time omhulsel maken', 'value': 5}], multi = False,
#                         value = 1, style = {'width':'100%'}),
#             html.Div(id = 'output_container', children = []),
#             html.Br(),
#             #dcc.Graph(id = 'queue time staal koppelen', figure = fig_queue_time_staal_koppelen),
#             dcc.Graph(id = 'process measure', figure ={}),
#             dcc.Graph(id = 'Gantt_all_disruptions', figure = fig_gantt_disruptions),
#             dcc.Slider(0,100, id = 'slider disruption measure percentage', value = 5),
#             dcc.Graph(id = 'Pie reason queue', figure ={}),
#             dcc.Dropdown(id='select stock graph', options=[{'label': 'raw material - stalen stangen', 'value': ['raw materials','stalen stangen']},
#                                                            {'label': 'raw material - koppeldraad', 'value': ['raw materials','koppeldraad']},
#                                                            {'label': 'raw material - soft stuffing', 'value': ['raw materials','soft stuffing']},
#                                                            {'label': 'raw material - medium stuffing', 'value': ['raw materials','medium stuffing']},
#                                                            {'label': 'raw material - hard stuffing', 'value': ['raw materials','hard stuffing']},
#                                                            {'label': 'subassembly - gebogen stangen', 'value': ['subassemblies','gebogen stangen']},
#                                                            {'label': 'subassembly - gekoppeld eenpersoons', 'value': ['subassemblies','gekoppeld eenpersoons']},
#                                                            {'label': 'subassembly - gekoppeld twijfelaar', 'value': ['subassemblies','gekoppeld twijfelaar']},
#                                                            {'label': 'subassembly - gekoppeld queensize', 'value': ['subassemblies','gekoppeld queensize']},
#                                                            {'label': 'subassembly - gekoppeld kingsize', 'value': ['subassemblies','gekoppeld kingsize']}
#                                                            ], multi=False,
#                  value=['raw materials','stalen stangen'], style={'width': '100%'}),
#             dcc.Graph(id = 'stock level graph', figure ={}),
#             dcc.Input(id = 'input specific order', type = 'text', placeholder= 'type orderID'),
#             dcc.Graph(id = 'specific order disruptions', figure = fig_some_order),
#
#
#
# ])



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

get_callbacks(app)

if __name__ == '__main__':
    app.run_server()