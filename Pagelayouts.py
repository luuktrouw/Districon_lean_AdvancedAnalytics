
from dash.dependencies import Input, Output

import dash
import pandas as pd
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import main_simulation
import Plotting_functions_Extra
import Load_inputsettings

navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Management summary", href="Manager")),
            dbc.NavItem(dbc.NavLink("Settings", href="Settings")),
            dbc.NavItem(dbc.NavLink("Inventory", href="Inventory")),
            dbc.NavItem(dbc.NavLink("Lead times", href="Lead_times")),
        ],
        id = 'navbarsimple',
        color="primary"
    )

def get_pagelayout_manager(Mananger_fig_dict):
    headline = html.H1("Management Summary", style={'text-align': 'center'})

    row1_manager = dbc.Row(
        [
            dbc.Col(dbc.Card(Mananger_fig_dict['card deadlines made'], color="primary", outline=True)),
            dbc.Col(dbc.Card(Mananger_fig_dict['card prio deadlines made'], color="primary", outline=True)),
            dbc.Col(dbc.Card(Mananger_fig_dict['card throughout time'], color="primary", outline=True)),
            dbc.Col(dbc.Card(Mananger_fig_dict['card lateness'], color="primary", outline=True)),
        ]
    )

    row2_manager = dbc.Row(
        [
            dbc.Col(
                [
                dbc.Row(dbc.Card(Mananger_fig_dict['card queue time'], color="primary", outline=True)),
                dbc.Row(dbc.Card(Mananger_fig_dict['card producing time'], color="primary", outline=True)),
                ]
            ),
            dbc.Col(
                [
                dcc.Slider(0,100, id = 'slider disruption measure percentage', value = 5),
                dcc.Graph(id = 'Pie reason queue', figure ={}),
                ]
            ),
        ]
    )
    page_manager = html.Div([navbar,headline, row1_manager,  row2_manager, ])
    return page_manager

def get_pagelayout_settings(Settings_fig_dict):
    headline = html.H1("Settings", style={'text-align': 'center'})

    resim_button = dcc.Loading(html.Div(
        dbc.Button("RESIMULATE", color="primary", id = 'resimulate button', n_clicks=0),
    )
    )

    row2_settings = dbc.Row(
        [
            dbc.Col([
                    html.H5("speelveld process schakels", style={'text-align': 'center'}),
                    Settings_fig_dict['editable process schakels']
                    ], width={"size": 6, "offset": 0}),
            dbc.Col([
                    html.H5("speelveld breakdowns", style={'text-align': 'center'}),
                    Settings_fig_dict['editable breakdowns']
                    ],width={"size": 6, "offset": 0}),
        ]
    )

    row3_settings = dbc.Row(
        [
            dbc.Col([
                html.H5("speelveld orders", style={'text-align': 'center'}),
                Settings_fig_dict['editable orders']
                ],width={"size": 6, "offset":0}),
            dbc.Col([
                html.H5("speelveld suppliers", style={'text-align': 'center'}),
                Settings_fig_dict['editable supply']
                ],width={"size": 6, "offset": 0}),
        ]
    )

    page_settings = html.Div([navbar, headline,resim_button, row2_settings,row3_settings])
    return page_settings

def get_pagelayout_inventory(Inventory_fig_dict):
    headline = html.H1("Inventory results", style={'text-align': 'center'})

    dropdown_materials = dcc.Dropdown(id='select stock graph', options=[{'label': 'raw material - stalen stangen', 'value': ['raw materials','stalen stangen']},
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
                 value=['raw materials','stalen stangen'], style={'width': '100%'})

    row1_inventory = dbc.Row(
        [
            dbc.Col([
                        html.H5("fractie tijd out of order", style={'text-align': 'center'}),
                        dcc.Graph(id='outofstockfractie', figure=Inventory_fig_dict['frac out of order']),
                    ],  style={'width': '40%'}),
            dbc.Col([
                        html.H5("average stock levels V alle materials", style={'text-align': 'center'}),
                        dcc.Graph(id='average stock levels', figure={}),
                    ],  style={'width': '40%'}),
        ],
    )

    row2_inventory = dbc.Row(
        [
            dbc.Col(
                [
                    html.H5("Stock level verloop", style={'text-align': 'center'}),
                    dropdown_materials,
                    dcc.Graph(id='stock level graph', figure={}) ,
                ]
            ),
        ],
    )

    page_inventory = html.Div([navbar, headline, row1_inventory, row2_inventory, ])

    return page_inventory

def get_pagelayout_leadtimes(Leadtimes_fig_dict):
    headline = html.H1("Lead and wait time results", style={'text-align': 'center'})

    dropdown_schakel_leadtimes = dcc.Dropdown(id = 'select measure', options = [{'label': 'Total throughout time', 'value': 1},{'label': 'Total queueing time', 'value': 2},
                              {'label': 'Queueing time staal buigen', 'value': 3},{'label': 'Queueing time staal koppelen', 'value': 4},{'label': 'Queueing time omhulsel maken', 'value': 5}], multi = False,
                            value = 1,)

    dropdown_schakel_waittimes = dcc.Dropdown(id = 'select schakel waittimes', options = [{'label': 'Total process', 'value': 'total process'},{'label': 'Staal buigen', 'value': 'staal buigen'},
                              {'label': 'Staal koppelen', 'value': 'staal koppelen'},{'label': 'Omhulsel maken', 'value': 'omhulsel maken'}], multi = False,
                            value = 'staal buigen',)

    row1_leadtimes = dbc.Row(
        [
            dcc.Graph(id='VSMstatistics', figure=Leadtimes_fig_dict['VSM statistics times'])
        ]
    )

    row2_leadtimes = dbc.Row(
        [
            dbc.Col(
                [
                    html.H5("Throughput times of the orders", style={'text-align': 'center'}),
                    dbc.Row(dropdown_schakel_leadtimes),
                    dbc.Row(dcc.Graph(id = 'process measure', figure ={})),
                ],  style={'width': '40%'}
            ),
            dbc.Col(
                [
                    html.H5("Wait times per schakel", style={'text-align': 'center'}),
                    dbc.Row(dropdown_schakel_waittimes),
                    dbc.Row(dcc.Graph(id = 'schakel wait times', figure ={})),
                ],  style={'width': '40%'}
            ),
        ]
    )

    row3_leadtimes = dbc.Row(
        [
            dbc.Col(
                [
                    html.H5("Specifieke order verloop", style={'text-align': 'center'}),
                    dbc.Row(dcc.Input(id = 'input specific order', type = 'text', placeholder= 'type orderID')),
                    dbc.Row(dcc.Graph(id = 'specific order disruptions', figure = {})),
                    #plottingfunctions.plot_gantt_per_order(finished_orders_df, sortfinisheddf.iloc[0]['orderID'])
                ], style={'width': '40%'}
            ),
            dbc.Col(
                [
                    html.H5("All disruption intervals", style={'text-align': 'center'}),
                    dcc.Graph(id = 'Gantt_all_disruptions', figure = Leadtimes_fig_dict['all disruption intervals']),
                ], style={'width': '40%'}
            ),
        ]
    )

    page_leadtimes = html.Div([navbar, headline, row1_leadtimes, row2_leadtimes,row3_leadtimes, ])
    return page_leadtimes
