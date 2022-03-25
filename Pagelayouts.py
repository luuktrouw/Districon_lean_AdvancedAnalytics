
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

finished_orders_df, measures, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions, totaltime = main_simulation.runsimulation(settingdistibution_dict)
sortfinisheddf = finished_orders_df.sort_values('total process time', ascending=False)

navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Managerial summary", href="Manager")),
            dbc.NavItem(dbc.NavLink("Settings", href="Settings")),
            dbc.NavItem(dbc.NavLink("Inventory", href="Inventory")),
            dbc.NavItem(dbc.NavLink("Lead times", href="Lead_times")),
        ],
        id = 'navbarsimple',
        color="primary"
    )

def get_pagelayout_manager():
    headline = html.H1("Managerial Summary", style={'text-align': 'center'})

    percdeadlinemade = plottingfunctions.get_perc_deadlines_met(finished_orders_df)
    card_fracdeadlinesmade =[
        dbc.CardHeader("Deadlines made"),
        dbc.CardBody(
            [
                html.P(str(percdeadlinemade)+'%', className="card-title"),
            ]
        ),
    ]

    prios = finished_orders_df[finished_orders_df['high priority'] == True]
    if len(prios)>0:
        perc_prio_deadlinemade = str(plottingfunctions.get_perc_deadlines_met(prios)) + '%'
    else: perc_prio_deadlinemade = 'no simulated priority orders'
    card_fracprio_deadlinesmade =[
        dbc.CardHeader("Priority deadlines made"),
        dbc.CardBody(
            [
                html.P(str(perc_prio_deadlinemade), className="card-title"),
            ]
        ),
    ]

    card_average_throughputtime = plottingfunctions.get_cardtotalthroughput_time(means, lower_5_quantiles, upper_95_quantiles)

    card_average_lateness = plottingfunctions.get_cardlateness_time(means, lower_5_quantiles, upper_95_quantiles)

    card_average_waitingtime = plottingfunctions.get_cardtotalwaiting_time(means, lower_5_quantiles, upper_95_quantiles)

    card_average_timeproducing = plottingfunctions.get_cardtotalproducing_time(means, lower_5_quantiles, upper_95_quantiles)

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

    table_breakdowns = plottingfunctions.make_fig_speelveldbreakdowns(settingdistibution_dict)

    table_orders =  plottingfunctions.make_fig_speelveldorders(settingdistibution_dict)

    table_suppliers =  plottingfunctions.make_fig_speelveldsupply(settingdistibution_dict)

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
                        dcc.Graph(id='outofstockfractie', figure=plottingfunctions.make_barchart_disruptionfracs(measures, totaltime)),
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

    dropdown_schakel_waittimes = dcc.Dropdown(id = 'select schakel waittimes', options = [{'label': 'Total process', 'value': 'total process'},{'label': 'Staal buigen', 'value': 'staal buigen'},
                              {'label': 'Staal koppelen', 'value': 'staal koppelen'},{'label': 'Omhulsel maken', 'value': 'omhulsel maken'}], multi = False,
                            value = 'staal buigen',)

    row1_leadtimes = dbc.Row(
        [
            #dcc.Graph(id='VSMstatistics', figure=plottingfunctions.make_fig_VSM_statistics(means, lower_5_quantiles, upper_95_quantiles))
            dcc.Graph(id='VSMstatistics', figure=plottingfunctions.make_violin_VSM_statistics(finished_orders_df))
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
                    dbc.Row(dcc.Graph(id = 'specific order disruptions', figure = plottingfunctions.plot_gantt_per_order(finished_orders_df, sortfinisheddf.iloc[0]['orderID']))),
                ], style={'width': '40%'}
            ),
            dbc.Col(
                [
                    html.H5("All disruption intervals", style={'text-align': 'center'}),
                    dcc.Graph(id = 'Gantt_all_disruptions', figure = fig_gantt_disruptions),
                ], style={'width': '40%'}
            ),
        ]
    )

    page_leadtimes = html.Div([navbar, headline, row1_leadtimes, row2_leadtimes,row3_leadtimes, ])
    return page_leadtimes

def get_pagelayouts(settingdistibution_dict):

    page_manager = get_pagelayout_manager()

    page_settings = get_pagelayout_settings()

    page_inventory = get_pagelayout_inventory()

    page_leadtimes = get_pagelayout_leadtimes()

    return page_manager, page_settings, page_inventory, page_leadtimes


