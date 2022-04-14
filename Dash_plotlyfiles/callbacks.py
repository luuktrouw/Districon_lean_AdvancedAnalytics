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


def get_callbacks(app):

    @app.callback(Output(component_id= 'stock level graph', component_property= 'figure'),
                  [Input(component_id='select stock graph', component_property= 'value')],
                  [State('measures', 'data')])
    def update_stocklevelsgraph(option_slctd, newmeasures):
        #if text in finished_orders_df['orderID']:
        print(option_slctd)
        figure = Plotting_functions_Inventory.plot_stocklevels_through_time(newmeasures['stock levels'][option_slctd[0]][option_slctd[1]])
        return figure

    @app.callback(Output(component_id='process measure', component_property='figure'),
                  [Input(component_id='select measure', component_property='value')],
                [ State('Leadtimes_fig_dict', 'data'),
                  ])
    def update_graph(option_slctd, Leadtimes_fig_dict):
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

    @app.callback(Output(component_id='VSMstatistics', component_property='figure'),
                  [Input(component_id='VSMfilteroutpercentage', component_property='value')],
                  [State('sortfinisheddf', 'data')])
    def update_VSM_graph(percentage,sortfinisheddf):
        sortfinisheddf = pd.read_json(sortfinisheddf, orient='split')
        sortfinisheddf = sortfinisheddf.sort_values(by='total queue time',ascending=False)
        newwwdf = sortfinisheddf.reset_index(drop = True)
        dropnumber = int(percentage/100 * len(sortfinisheddf))
        newdf = sortfinisheddf.iloc[dropnumber:, :]
        figure = Plotting_functions_Leadtimes.make_violin_VSM_statistics(newdf)
        return figure


    @app.callback(Output(component_id='Pie reason queue', component_property='figure'),
                  [Input(component_id='slider disruption measure percentage', component_property='value')],
                  [State('sortfinisheddf', 'data')])
    def update_single_order_graph(option_slctd, sortfinisheddf):
        sortfinisheddf = pd.read_json(sortfinisheddf, orient='split')
        # if text in finished_orders_df['orderID']:
        figure = Plotting_functions_Management.plot_fractions_wait_time_reasons(sortfinisheddf, option_slctd)
        return figure

    @app.callback(Output(component_id='schakel wait times', component_property='figure'),
                  [Input(component_id='select schakel waittimes', component_property='value')],
                  [State('Leadtimes_fig_dict', 'data')])
    def update_single_order_graph(option_slctd, Leadtimes_fig_dict):
        figure = Leadtimes_fig_dict['fraction wait times per schakel'][option_slctd]
        return figure

    @app.callback(Output(component_id='specific order disruptions', component_property='figure'),
                  [Input(component_id='input specific order', component_property='value')],
                  [State('finishedorderdf', 'data'),
                   State('sortfinisheddf', 'data')])
    def update_single_order_graph(option_slctd, finished_orders_df, sortfinisheddf):
        # if text in finished_orders_df['orderID']:
        sortfinisheddf = pd.read_json(sortfinisheddf, orient='split')
        option_slctd = sortfinisheddf.iloc[0]['orderID']
        print(option_slctd)
        figure = plottingfunctions.plot_gantt_per_order(finished_orders_df, option_slctd)
        return figure

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
        #dff = pd.read_json(newfo_df, orient='split')
        #sortfinisheddf = pd.read_json(sortfinisheddf, orient='split')
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

    #THE ALMIGHTY RESIMULATE CALL BACK
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
        print('n is nu', n)
        print('data suppple  = ', datasupply)
        #fig.show()
        if n ==0:
            raise PreventUpdate

        else:
            settingdistibution_dict = Functions.read_supply_editabledata(dataorders, datasupply, dataschakels, databreakdowns)

            finished_orders_df, measures, totaltime = main_simulation.runsimulation(settingdistibution_dict)

            Mananger_fig_dict = Plotting_functions_Management.get_Management_figures(finished_orders_df)

            Settings_fig_dict = Plotting_functions_Settings.get_Settings_figures(settingdistibution_dict)

            Inventory_fig_dict = Plotting_functions_Inventory.get_Inventory_figures(measures, totaltime)

            Leadtimes_fig_dict = Plotting_functions_Leadtimes.get_Leadtimes_figures(finished_orders_df, measures)

            sortfinisheddf = finished_orders_df.sort_values('total queue time', ascending=False)

            return '/Manager', finished_orders_df.to_json(orient="split"), measures, totaltime, settingdistibution_dict, \
                   sortfinisheddf.to_json(orient="split"), Mananger_fig_dict, Settings_fig_dict, Inventory_fig_dict, Leadtimes_fig_dict





