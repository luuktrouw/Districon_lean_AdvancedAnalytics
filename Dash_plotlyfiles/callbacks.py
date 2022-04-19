import pandas as pd
from dash import State
from dash.dependencies import Input, Output
import Functions
import Pagelayouts
import Plotting_functions_Inventory
import Plotting_functions_Management
import Plotting_functions_Leadtimes
import Plotting_functions_Settings
from Simulationfiles import main_simulation
from dash.exceptions import PreventUpdate

'''
This file contains all the callback functions of the app (dashboard)
The are loaded in by calling the get_callbacks function, after which they respond to changes
Each callback has a certain input id component, if the component with this id (i.e. a dorpdown) changes, the callback is triggered
The callback used the input and certain state variables to calculate an Output. 
The function returns a value for the component with the output id, which result in now values of the app
There are multiple callbacks, each for one for a certain adjustable figure or variable
A callback consists of two things: an @app.callback line and a function directly below it, which are automatically linked
The @app.callback part describes the input, output and needed states, and the function calculated the outputs
The component_id's which are inputs or outputs are the component id's as specified in the creation of the figures
'''

def get_callbacks(app):

    # The callback below updates the stock level time series. It's input is the corresponding dropdown of materials
    @app.callback(Output(component_id= 'stock level graph', component_property= 'figure'),
                  [Input(component_id='select stock graph', component_property= 'value')],
                  [State('measures', 'data')])
    def update_timeseries_stocklevelsgraph(option_slctd, newmeasures):
        print(option_slctd)
        # it calls the function which plots the time series using the measures state variable and returns this figure
        figure = Plotting_functions_Inventory.plot_stocklevels_through_time(newmeasures['stock levels'][option_slctd[0]][option_slctd[1]])
        return figure

    # The callback below updates the fraction of time in each work state for a certain process. It's input is the corresponding of process steps
    @app.callback(Output(component_id= 'work state fractions process step', component_property= 'figure'),
                  [Input(component_id='select work state fraction process step', component_property= 'value')],
                  [State('measures', 'data')])
    def update_workstate_fraction_perstep(option_slctd, newmeasures):
        # it calls the function which plots the work state fractions using the measures state variable and returns this figure
        figure = Plotting_functions_Inventory.plotworkstates_fractions(newmeasures['workstate times'][option_slctd])
        return figure


    # The callback below updates the throughput time histogram of the process steps, it's input is the corresponding dropwdown of process steps
    @app.callback(Output(component_id='process measure', component_property='figure'),
                  [Input(component_id='select measure', component_property='value')],
                [ State('Leadtimes_fig_dict', 'data'),
                  ])
    def update_througput_times_histogram(option_slctd, Leadtimes_fig_dict):
        # given the input, it calls the corresponding figure from the leadtimes figure dictionary state variable
        if option_slctd == 1:
            figu = Leadtimes_fig_dict['throughput times per schakel']['total throughput time']
        elif option_slctd == 2:
            figu = Leadtimes_fig_dict['throughput times per schakel']['total queueing time']
        elif option_slctd == 3:
            figu = Leadtimes_fig_dict['throughput times per schakel']['Queueing time staal buigen']
        elif option_slctd == 4:
            figu = Leadtimes_fig_dict['throughput times per schakel']['Queueing time staal koppelen']
        elif option_slctd == 5:
            figu = Leadtimes_fig_dict['throughput times per schakel']['Queueing time omhulsel maken']

        return figu

    # The callback below updates the total lead times violin plot which contains all process steps. It's input is the percentage which needs to be filtered out
    @app.callback(Output(component_id='VSMstatistics', component_property='figure'),
                  [Input(component_id='VSMfilteroutpercentage', component_property='value')],
                  [State('sortfinisheddf', 'data')])
    def update_VSM_violin_times_graph(percentage,sortfinisheddf):
        # The function first reads in the sorted finished order dataframe from the state variable
        # afterwards it makes sure to sort them on queueing time, instead of process time
        # (process time is only until the order can be delivered, so might not include the delay in the first step if it take the sub assembly from the last step) Total queuing time does have this time so gives more info
        sortfinisheddf = pd.read_json(sortfinisheddf, orient='split')
        # afterwards it takes out the filtered percentage and calls the make violin function to return the figure
        sortfinisheddf = sortfinisheddf.sort_values(by='total queue time',ascending=False)
        sortfinisheddf = sortfinisheddf.reset_index(drop = True)
        dropnumber = int(percentage/100 * len(sortfinisheddf))
        newdf = sortfinisheddf.iloc[dropnumber:, :]
        figure = Plotting_functions_Leadtimes.make_violin_VSM_statistics(newdf)
        return figure

    # The callback below updates the pie chart with the disruption fractions of the total process. It's input is the percentage slider which needs to be filtered out
    @app.callback(Output(component_id='Pie reason queue', component_property='figure'),
                  [Input(component_id='slider disruption measure percentage', component_property='value')],
                  [State('sortfinisheddf', 'data')])
    def update_total_pie_chart_disruptions(option_slctd, sortfinisheddf):
        # it first loads in the sorted finished order dataframe from the state variable.
        # afterwards it calls the corresponding plotting function with this dataframe and the selected percantage
        sortfinisheddf = pd.read_json(sortfinisheddf, orient='split')
        figure = Plotting_functions_Management.plot_fractions_wait_time_reasons(sortfinisheddf, option_slctd)
        return figure

    # The callback below updates the pie chart with the disruption fractions for each process step. It's input is the dropdown containing process steps
    @app.callback(Output(component_id='schakel wait times', component_property='figure'),
                  [Input(component_id='select schakel waittimes', component_property='value')],
                  [State('Leadtimes_fig_dict', 'data')])
    def update_pie_chart_disruption_process_step(option_slctd, Leadtimes_fig_dict):
        # it receives the stored figure from the given state variable lead times figures dictionary with the selected option and returns that figure
        figure = Leadtimes_fig_dict['fraction wait times per schakel'][option_slctd]
        return figure

    # The callback below updates the gantt chart which gives the events of the time span of one specific order. It's input is the order name
    @app.callback(Output(component_id='specific order disruptions', component_property='figure'),
                  [Input(component_id='input specific order', component_property='value')],
                  [State('finishedorderdf', 'data'),
                   State('sortfinisheddf', 'data')])
    def update_single_order_graph(option_slctd, finished_orders_df, sortfinisheddf):
        # it first loads in the sorted finished order dataframe from the state variable.
        sortfinisheddf = pd.read_json(sortfinisheddf, orient='split')

        ##################################################################################################
        # the line below automatically selects the slowest order, this should be deleted if the function needs to be working
        option_slctd = sortfinisheddf.iloc[0]['orderID']
        print(option_slctd)
        ##################################################################################################

        # afterwards it calls the corresponding plotting function and returns the figure
        figure = Plotting_functions_Leadtimes.plot_gantt_per_order(sortfinisheddf, option_slctd)
        return figure

    # the callback below updates the current page of the complete app if the link is changed, input is clicking the NavBar, or typing a different link
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')],
                  [
                    State('VSMfilepath', 'data'),
                    State('Mananger_fig_dict', 'data'),
                    State('Settings_fig_dict', 'data'),
                    State('Inventory_fig_dict', 'data'),
                    State('Leadtimes_fig_dict', 'data'),
                  ]
                  )
    def display_page(pathname,VSMfilepath, Mananger_fig_dict,Settings_fig_dict , Inventory_fig_dict, Leadtimes_fig_dict):
        # The link pathname determines the if statement it goes in.
        # with the pathname, a page of the pagelayout is called and is returned
        if pathname == '/VSM':
            return Pagelayouts.get_pagelayout_manager(Mananger_fig_dict)
        elif pathname == '/Manager':
            return Pagelayouts.get_pagelayout_manager(Mananger_fig_dict)
        elif pathname == '/Settings':
            return Pagelayouts.get_pagelayout_settings(Settings_fig_dict)
        elif pathname == '/Inventory':
            return Pagelayouts.get_pagelayout_inventory(Inventory_fig_dict)
        elif pathname == '/Lead_times':
            return Pagelayouts.get_pagelayout_leadtimes(Leadtimes_fig_dict)
        else:
            return Pagelayouts.get_pagelayout_manager(Mananger_fig_dict)

    #The callback below resimulates the entire process and updates all state variables. it's input is the resimulate button
    # afterwards, all new state variables are returned, so that we can use the updated variables in the future
    # the page is reset to the management page
    @app.callback([Output('url', 'pathname'), Output('finishedorderdf', 'data'),
                   Output('measures', 'data'),
                   Output('totaltime', 'data'),
                   Output('settingdistibution_dict', 'data'),
                   Output('sortfinisheddf', 'data'),
                   Output('Mananger_fig_dict', 'data'),
                   Output('Settings_fig_dict', 'data'),
                   Output('Inventory_fig_dict', 'data'),
                   Output('Leadtimes_fig_dict', 'data'),
                   ],
                  [Input('resimulate button', 'n_clicks')],
                [ State('settingssupply', 'data'), State('settingsbreakdowns', 'data'),State('settingsprocessschakels', 'data'),State('settingsorders', 'data'),])
    def RESIMULATE(n,datasupply, databreakdowns, dataschakels, dataorders ):
        # if the button is not clicked (n=0), nothing is updated
        if n ==0:
            raise PreventUpdate
        # otherwise, the process is resimulated
        else:
            #the settings for the simulation are read in from the editable tables
            settingdistibution_dict = Functions.read_supply_editabledata(dataorders, datasupply, dataschakels, databreakdowns)
            # the simulation is rerun with the new settings
            finished_orders_df, measures, totaltime = main_simulation.runsimulation(settingdistibution_dict)
            # and all page figures are re-determined by called each function again
            Mananger_fig_dict = Plotting_functions_Management.get_Management_figures(finished_orders_df)

            Settings_fig_dict = Plotting_functions_Settings.get_Settings_figures(settingdistibution_dict)

            Inventory_fig_dict = Plotting_functions_Inventory.get_Inventory_figures(measures, totaltime)

            Leadtimes_fig_dict = Plotting_functions_Leadtimes.get_Leadtimes_figures(finished_orders_df, measures)

            sortfinisheddf = finished_orders_df.sort_values('total queue time', ascending=False)
            # afterwards, all new state variables are returned, so that we can use the updated variables in the future
            # the page is reset to the management page
            return '/Manager', finished_orders_df.to_json(orient="split"), measures, totaltime, settingdistibution_dict, \
                   sortfinisheddf.to_json(orient="split"), Mananger_fig_dict, Settings_fig_dict, Inventory_fig_dict, Leadtimes_fig_dict





