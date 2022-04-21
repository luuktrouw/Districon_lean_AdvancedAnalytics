import dash_bootstrap_components as dbc
from dash import html, dcc

'''
This file contains the functions which make the layout of the pages. 
Each page has its own function which structures the page and gives the figures id's and possibly figures,
which are imported by this corresponding input dictionary which contains the figures
All pages are constructed with dash using html to structure the page and using dbc and dcc components
'''

# The navigation bar on top of all pages is designed below using the NavbarSimple functions from dash_bootstrap_components
Districonpicture = html.Img(
    src='./assets/Districon_RHDHV_RGB_White_w_Colour_Triangle.png',
    #className="logo-connekt",
    style = {'width': '16.66666666%', "background-color": "#024791", 'margin-right': '-12px'}
)
navbar1 = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("VSM Visualization", href="VSM")),
            dbc.NavItem(dbc.NavLink("Management summary", href="Manager")),
            dbc.NavItem(dbc.NavLink("Settings", href="Settings")),
            dbc.NavItem(dbc.NavLink("Inventory", href="Inventory")),
            dbc.NavItem(dbc.NavLink("Lead times", href="Lead_times")),
        ],
        id = 'navbarsimple',
        # brand = 'Districon',
        # brand_external_link=True,
        # brand_href='https://www.districon.com/',
        color=	'#024791',
        style = {'height': '100%', 'margin-right': '-12px'}
        )

navbar = dbc.Row(
    [Districonpicture, dbc.Col(navbar1, width = 10)]
)

# This function makes the layout of the management page and returns that page
def get_pagelayout_manager(Mananger_fig_dict):
    # the headline of the page is made below
    headline = html.H1("Management Summary", style={'text-align': 'center'})

    # The first row of this page consists of 4 cards, which are loaded into the first row in different columns, using the cards from Manager_fig_dict input
    row1_manager = dbc.Row(
        [
            dbc.Col(dbc.Card(Mananger_fig_dict['card deadlines made'], color="primary", outline=True)),
            dbc.Col(dbc.Card(Mananger_fig_dict['card prio deadlines made'], color="primary", outline=True)),
            dbc.Col(dbc.Card(Mananger_fig_dict['card throughout time'], color="primary", outline=True)),
            dbc.Col(dbc.Card(Mananger_fig_dict['card lateness'], color="primary", outline=True)),
        ]
    )
    # second row consists of two columns, one with two other cards and one with the pie chart of queueing reasons and a sliders to filter out an x% of worst orders
    row2_manager = dbc.Row(
        [
            dbc.Col(
                [
                dbc.Row(dbc.Card(Mananger_fig_dict['card queue time'], color="primary", outline=True, )),
                dbc.Row(dbc.Card(Mananger_fig_dict['card producing time'], color="primary", outline=True, style={"width": "18rem"},)),
                ]
            ),
            dbc.Col(
                [
                dcc.Slider(0,100, id = 'slider disruption measure percentage', value = 5),
                dcc.Loading(
                            children= [
                                        dcc.Graph(id = 'Pie reason queue', figure ={}),
                                      ],
                            type = 'circle',
                            ),
                ]
            ),
        ]
    )

    # The total page structure is made below using the previous components
    page_manager = html.Div([navbar,headline, row1_manager,  row2_manager, ])
    return page_manager

# This function makes the layout of the settings page and returns that page
def get_pagelayout_settings(Settings_fig_dict):
    # the headline of the page is made below
    headline = html.H1("Settings", style={'text-align': 'center'})

    # The resimulate button is placed on top of the page, inside the loading component to make sure the loading sign is displayed if the button is clicked
    resim_button = dcc.Loading(html.Div(
        dbc.Button("RESIMULATE", color="primary", id = 'resimulate button', n_clicks=0),
    )
    )

    #the second row consists of two editables in two columns
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
    #the third row consists of the remaining two editables in two columns
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
    # The total page structure is made below using the previous components
    page_settings = html.Div([navbar, headline,resim_button, row2_settings,row3_settings])
    return page_settings

# This function makes the layout of the iventory page and returns that page
def get_pagelayout_inventory(Inventory_fig_dict):
    # the headline of the page is made below
    headline = html.H1("Inventory results", style={'text-align': 'center'})

    # For the disruption fractions of process steps, a dropdown is made to be able to select the step of desire
    dropdown_workstate_fractions = dcc.Dropdown(id = 'select work state fraction process step', options = [{'label': 'Staal buigen', 'value': 0},
                              {'label': 'Staal koppelen', 'value': 1},{'label': 'Omhulsel maken', 'value': 2}], multi = False,
                            value = 0,)

    # The first row contains two figures in two columns, the fractions of disruptions in the first and fraction of capacity the process steps used
    row1_inventory = dbc.Row(
        [
            dbc.Col([
                        html.H5("fractie tijd out of order", style={'text-align': 'center'}),
                        dcc.Graph(id='outofstockfractie', figure=Inventory_fig_dict['frac out of order']),
                    ],  style={'width': '40%'}),
            dbc.Col([
                        html.H5("Amount of capacity utilized fractions", style={'text-align': 'center'}),
                        dropdown_workstate_fractions,
                        dcc.Graph(id='work state fractions process step', figure={}),
                    ],  style={'width': '40%'}),
        ],
    )

    # For the time series of stock levels, a dropdown is made to be able to select the material of desire
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

    # the second row consists of one column, containing the dropdown and the time series graph below
    row2_inventory = dbc.Row(
        [
            dbc.Col(
                [
                    html.H5("Time Series Stock Level", style={'text-align': 'center'}),
                    dropdown_materials,
                    dcc.Graph(id='stock level graph', figure={}) ,
                ]
            ),
        ],
    )
    # The total page structure is made below using the previous components
    page_inventory = html.Div([navbar, headline, row1_inventory, row2_inventory, ])

    return page_inventory

# This function makes the layout of the lead times page and returns that page
def get_pagelayout_leadtimes(Leadtimes_fig_dict):
    # the headline of the page is made below
    headline = html.H1("Lead and wait time results", style={'text-align': 'center'})

    # For the throughput times of process steps, a dropdown is made to be able to select the step of desire
    dropdown_schakel_leadtimes = dcc.Dropdown(id = 'select measure', options = [{'label': 'Total throughout time', 'value': 1},{'label': 'Total queueing time', 'value': 2},
                              {'label': 'Queueing time staal buigen', 'value': 3},{'label': 'Queueing time staal koppelen', 'value': 4},{'label': 'Queueing time omhulsel maken', 'value': 5}], multi = False,
                            value = 1,)

    # For the disruption fractions of process steps, a dropdown is made to be able to select the step of desire
    dropdown_schakel_waittimes = dcc.Dropdown(id = 'select schakel waittimes', options = [{'label': 'Total process', 'value': 'total process'},{'label': 'Staal buigen', 'value': 'staal buigen'},
                              {'label': 'Staal koppelen', 'value': 'staal koppelen'},{'label': 'Omhulsel maken', 'value': 'omhulsel maken'}], multi = False,
                            value = 'staal buigen',)

    # The first row consists of the lead times violin plot of all process steps, below the plot is a slider
    # which indicates the percentage of worst lead times filtered out
    row1_leadtimes = dbc.Row(
        [
            dbc.Row(dcc.Graph(id='VSMstatistics', figure=Leadtimes_fig_dict['VSM statistics times'])),
            dbc.Row(dcc.Slider(0, 100, id='VSMfilteroutpercentage', value=5)),
        ]
    )

    # The second row consists of two columns, each with a dropdown and a graph
    # The first column is the lead times of process steps
    # The second column is the wait time fractions at each process step
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

    # The third row consists of two columns,
    # the first is the gantt plot of one order with all its events
    # The second one is the gantt plot of all disruptions in the simulation horizon
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
    # The total page structure is made below using the previous components
    page_leadtimes = html.Div([navbar, headline, row1_leadtimes, row2_leadtimes,row3_leadtimes, ])
    return page_leadtimes

# This function makes the layout of the value stream map page and returns that page
def get_pagelayout_VSMpicture(VSMfilepath):
    # the headline of the page is made below
    headline = html.H1("Value Stream Map Visualization", style={'text-align': 'center'})

    VSMpicture = html.Div([
        html.Img(
        src='./assets/VSMvisualizationMatrasses.png',
        #className="logo-connekt",
        style = {'width': '70%',}
        )],
        style = {'textAlign': 'center'})


    page_VSM = html.Div([navbar, headline,VSMpicture])
    return page_VSM

