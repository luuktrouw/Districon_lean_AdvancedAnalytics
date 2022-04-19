import dash
from dash import html, dcc
import Plotting_functions_Management
import Plotting_functions_Settings
import Plotting_functions_Inventory
import Plotting_functions_Leadtimes
from callbacks import get_callbacks
from Simulationfiles import Load_inputsettings, main_simulation

'''
This file is the main file to create the app
It does this by running the simulation using python, and creating a dashboard using Dash and Plotly
'''

# First it loads in the path name for the VSM image (to plot it later on
VSMimagefile_path = '../VSMvisualizationMatrasses.png'

# then it loads in the, MANUALLY SET FOR NOW, settings from the load settings file
settingdistibution_dict = Load_inputsettings.load_settings()

# with the settings it calls the function runsimulation from main_simulation.py to run the simulation and obtain the needed info
finished_orders_df, measures, totaltime = main_simulation.runsimulation(settingdistibution_dict)

# after running the simulation, it makes the basic page figures by calling the corresponding plotting functions
Mananger_fig_dict = Plotting_functions_Management.get_Management_figures(finished_orders_df)

Settings_fig_dict = Plotting_functions_Settings.get_Settings_figures(settingdistibution_dict)

Inventory_fig_dict = Plotting_functions_Inventory.get_Inventory_figures(measures, totaltime)

Leadtimes_fig_dict = Plotting_functions_Leadtimes.get_Leadtimes_figures(finished_orders_df, measures)

# it also sorts the finished order dataframe from the simulation, so this can be safed and only has to be done once
sortfinisheddf = finished_orders_df.sort_values('total queue time', ascending=False)

## Than it starts to make a dash app using Dash

# if some external stile css file exists, this can be uncommented
#external_stylesheets = [dbc.themes.BOOTSTRAP]

# it initializes the app with the Dash function
app = dash.Dash(__name__,
                #external_stylesheets=external_stylesheets
                )

# afterwards it makes the simplistic layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # the app structure is placed in a loading component, to make sure the loading sign is displayed if a new page is loaded
    dcc.Loading(
                children= [
                            # the first component is the page component, where the pages are loaded in using the callbacks
                            # this page is everything which is displayed in the dashboard (and the page can be changed of course)
                            html.Div([html.Div(id='page-content')]),

                            # further more there are some Store components, to store certain data
                            # by storing the data, we can use them in the callbacks, without having to run the simulation again
                            html.Div([dcc.Store(id='finishedorderdf', storage_type='session', data = finished_orders_df.to_json(orient="split")),]),
                            html.Div([dcc.Store(id='measures', storage_type='session', data = measures),]),
                            html.Div([dcc.Store(id='totaltime', storage_type='session', data=totaltime),]),
                            html.Div([dcc.Store(id='settingdistibution_dict', storage_type='session', data=settingdistibution_dict),]),
                            html.Div([dcc.Store(id='sortfinisheddf', storage_type='session', data=sortfinisheddf.to_json(orient="split")),]),
                            html.Div([dcc.Store(id= 'VSMfilepath', storage_type='session', data = VSMimagefile_path),]),
                            html.Div([dcc.Store(id='Mananger_fig_dict', storage_type='session', data=Mananger_fig_dict),]),
                            html.Div([dcc.Store(id='Settings_fig_dict', storage_type='session', data=Settings_fig_dict),]),
                            html.Div([dcc.Store(id='Inventory_fig_dict', storage_type='session', data=Inventory_fig_dict),]),
                            html.Div([dcc.Store(id='Leadtimes_fig_dict', storage_type='session', data=Leadtimes_fig_dict),]),
                          ],
                type = 'circle',
                fullscreen= True
                )
])

# it calls the get_callbacks function so that all the callbacks are now working
get_callbacks(app)

# let's run the app!
if __name__ == '__main__':
    app.run_server()