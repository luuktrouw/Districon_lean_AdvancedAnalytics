
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
import plottingfunctions
import Load_settings

settingdistibution_dict = Load_settings.load_settings()

finished_orders_df, measures, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions = main_simulation.runsimulation(settingdistibution_dict)
sortfinisheddf = finished_orders_df.sort_values('total process time', ascending=False)
fig_table_speelveld = plottingfunctions.make_fig_speelveld(settingdistibution_dict)

navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Manager troep", href="Manager")),
            dbc.NavItem(dbc.NavLink("Settings", href="Settings")),
            dbc.NavItem(dbc.NavLink("Inventory", href="Inventory")),
            dbc.NavItem(dbc.NavLink("Lead times", href="Lead_times")),
        ],
        id = 'navbarsimple'
    )

def get_pagelayout_manager():
    headline = html.H1("Managerial information", style={'text-align': 'center'})

    card_fracdeadlinesmade =[
        dbc.CardHeader("percentage deadlines made"),
        dbc.CardBody(
            [
                html.H5("percentage", className="card-title"),
            ]
        ),
    ]

    card_fracprio_deadlinesmade =[
        dbc.CardHeader("percentage priority deadlines made"),
        dbc.CardBody(
            [
                html.H5("percentage", className="card-title"),
            ]
        ),
    ]

    card_average_throughputtime = [
        dbc.CardHeader("average throughput time"),
        dbc.CardBody(
            [
                html.H5("time", className="card-title"),
                html.P(
                    ".05 quantile - .95 quantile",
                    className="card-text",
                ),
            ]
        ),
    ]

    card_average_lateness = [
        dbc.CardHeader("Average lateness"),
        dbc.CardBody(
            [
                html.H5("time", className="card-title"),
                html.P(
                    ".05 quantile - .95 quantile",
                    className="card-text",
                ),
            ]
        ),
    ]

    card_average_waitingtime = [
        dbc.CardHeader("Average waiting time"),
        dbc.CardBody(
            [
                html.H5('time', className="card-title"),
                html.P(
                    ".05 quantile - .95 quantile",
                    className="card-text",
                ),
            ]
        ),
    ]

    card_average_timeproducing = [
        dbc.CardHeader("Average producing time"),
        dbc.CardBody(
            [
                html.H5("time", className="card-title"),
                html.P(
                    ".05 quantile - .95 quantile",
                    className="card-text",
                ),
            ]
        ),
    ]

    row1_manager = dbc.Row(
        [
            dbc.Col(dbc.Card(card_fracdeadlinesmade, color="primary", outline=True)),
            dbc.Col(dbc.Card(card_fracprio_deadlinesmade, color="primary", outline=True)),
            dbc.Col(dbc.Card(card_average_throughputtime, color="primary", outline=True)),
            dbc.Col(dbc.Card(card_average_lateness, color="primary", outline=True)),
        ]
    )

    row2_manager = dbc.Row(
        [
            dbc.Col(
                [
                dbc.Row(dbc.Card(card_average_waitingtime, color="primary", outline=True)),
                dbc.Row(dbc.Card(card_average_timeproducing, color="primary", outline=True)),
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


def get_pagelayout_settings():
    headline = html.H1("Settings", style={'text-align': 'center'})

    table_processschakels = plottingfunctions.make_fig_speelveldprocessschakels(settingdistibution_dict)

    table_breakdowns = plottingfunctions.make_fig_speelveldprocessschakels(settingdistibution_dict)

    table_orders =  plottingfunctions.make_fig_speelveldprocessschakels(settingdistibution_dict)

    table_suppliers =  plottingfunctions.make_fig_speelveldprocessschakels(settingdistibution_dict)

    row1_settings = dbc.Row(
        [
            dbc.Col([
                    html.H5("speelveld process schakels", style={'text-align': 'center'}),
                    dcc.Graph(id='speelveld process schakels', figure=table_processschakels)
                    ]),
            dbc.Col([
                    html.H5("speelveld breakdowns", style={'text-align': 'center'}),
                    dcc.Graph(id='speelveld breakdowns', figure=table_breakdowns)
                    ]  ),
        ]
    )

    row2_settings = dbc.Row(
        [
            dbc.Col([
                html.H5("speelveld orders", style={'text-align': 'center'}),
                dcc.Graph(id='speelveld orders', figure=table_orders)
            ]),
            dbc.Col([
                html.H5("speelveld suppliers", style={'text-align': 'center'}),
                dcc.Graph(id='speelveld suppliers', figure=table_suppliers)
            ]),
        ]
    )

    page_settings = html.Div([navbar, headline, row1_settings,  row2_settings, ])
    return page_settings

def get_pagelayout_inventory():
    headline = html.H1("Lead and wait time results", style={'text-align': 'center'})

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
                        dcc.Graph(id='outofstockfractie', figure={}),
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


def get_pagelayout_leadtimes():
    headline = html.H1("Lead and wait time results", style={'text-align': 'center'})

    dropdown_schakel_leadtimes = dcc.Dropdown(id = 'select measure', options = [{'label': 'Total throughout time', 'value': 1},{'label': 'Total queueing time', 'value': 2},
                              {'label': 'Queueing time staal buigen', 'value': 3},{'label': 'Queueing time staal koppelen', 'value': 4},{'label': 'Queueing time omhulsel maken', 'value': 5}], multi = False,
                            value = 1,)

    dropdown_schakel_waittimes = dcc.Dropdown(id = 'select schakel waittimes', options = [{'label': 'Total process', 'value': 1},{'label': 'Staal buigen', 'value': 2},
                              {'label': 'Staal koppelen', 'value': 3},{'label': 'Omhulsel maken', 'value': 4}], multi = False,
                            value = 1,)

    row1_leadtimes = dbc.Row(
        [
            dcc.Graph(id='VSMstatistics', figure=plottingfunctions.make_fig_VSM_statistics(means, lower_5_quantiles, upper_95_quantiles))
        ]
    )

    row2_leadtimes = dbc.Row(
        [
            dbc.Col(
                [
                    html.H5("Throughput times of the orders", style={'text-align': 'center'}),
                    dbc.Row(dropdown_schakel_leadtimes),
                    dbc.Row(dcc.Graph(id = 'process measure', figure ={})),
                ]
            ),
            dbc.Col(
                [
                    html.H5("Wait times per schakel", style={'text-align': 'center'}),
                    dbc.Row(dropdown_schakel_waittimes),
                    dbc.Row(dcc.Graph(id = 'schakel wait times', figure ={})),
                ]
            ),
        ]
    )

    row3_leadtimes = dbc.Row(
        [
            dbc.Col(
                [
                    html.H5("Specifieke order verloop", style={'text-align': 'center'}),
                    dbc.Row(dcc.Input(id = 'input specific order', type = 'text', placeholder= 'type orderID')),
                    dbc.Row(dcc.Graph(id = 'specific order disruptions', figure = plottingfunctions.plot_gantt_per_order(finished_orders_df, sortfinisheddf.iloc[0]['orderID']))),
                ]
            ),
            dbc.Col(
                [
                    html.H5("All disruption intervals", style={'text-align': 'center'}),
                    dcc.Graph(id = 'Gantt_all_disruptions', figure = fig_gantt_disruptions),
                ]
            ),
        ]
    )

    page_leadtimes = html.Div([navbar, headline, row1_leadtimes, row2_leadtimes,row3_leadtimes, ])
    return page_leadtimes

def get_pagelayouts(settingdistibution_dict):


    # row1_manager =

    row1_inventory = dbc.Row(
        [
            dbc.Col(dcc.Graph(id = 'speelveld',figure =  plottingfunctions.make_fig_speelveld(settingdistibution_dict))),
            dbc.Col(dcc.Graph(id = 'speelveld',figure =  plottingfunctions.make_fig_speelveld(settingdistibution_dict))),
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

    page_manager = get_pagelayout_manager()


    page_settings = get_pagelayout_settings()


    page_inventory = get_pagelayout_inventory()


    page_leadtimes = get_pagelayout_leadtimes()

    return page_manager, page_settings, page_inventory, page_leadtimes


