
from dash.dependencies import Input, Output


import pandas as pd
from dash import State
from dash.dependencies import Input, Output
import Functions
import Pagelayouts
import Plotting_functions_Inventory
import Plotting_functions_Management
import main_simulation
import Plotting_functions_Extra

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
                    State('Mananger_fig_dict', 'data'),
                    State('Settings_fig_dict', 'data'),
                    State('Inventory_fig_dict', 'data'),
                    State('Leadtimes_fig_dict', 'data'),
                  ]
                  )
    def display_page(pathname, Mananger_fig_dict,Settings_fig_dict , Inventory_fig_dict, Leadtimes_fig_dict):
        #dff = pd.read_json(newfo_df, orient='split')
        #sortfinisheddf = pd.read_json(sortfinisheddf, orient='split')
        if pathname == '/Manager':
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
                   Output('means', 'data'),
                   Output('lower_5_quantiles', 'data'),
                   Output('upper_95_quantiles', 'data'),
                   Output('fig_total_thoughout_time', 'data'),
                   Output('fig_queue_time_staal_buigen', 'data'),
                   Output('fig_queue_time_staal_koppelen', 'data'),
                   Output('fig_queue_time_omhulsel_maken', 'data'),
                   Output('fig_total_queue_time', 'data'),
                   Output('fig_gantt_disruptions', 'data'),
                   Output('totaltime', 'data'),
                   Output('settingdistibution_dict', 'data'),
                   Output('sortfinisheddf', 'data')
                   ],
                  [Input('resimulate button', 'n_clicks')],
                [ State('settingssupply', 'data'), State('settingsbreakdowns', 'data'),State('settingsprocessschakels', 'data'),State('settingsorders', 'data'),])
    def RESIMULATE(n,datasupply, databreakdowns, dataschakels, dataorders ):
        print('n is nu', n)
        print('data suppple  = ', datasupply)
        #fig.show()
        if n ==0:
            return '/Settings', finished_orders_df, measures, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions, totaltime, settingdistibution_dict, sortfinisheddf

        else:
            settingdistibution_dict = Functions.read_supply_editabledata(dataorders, datasupply, dataschakels, databreakdowns)

            finished_orders_df, measures, totaltime = main_simulation.runsimulation(settingdistibution_dict)

            sortfinisheddf = finished_orders_df.sort_values('total process time', ascending=False)

            newfodf = finished_orders_df.to_json(orient="split")
            newmeasures = measures
            newmeans = means
            newlower_5_quantiles = lower_5_quantiles
            newupper_95_quantiles = upper_95_quantiles
            newfig_total_thoughout_time = fig_total_thoughout_time
            newfig_queue_time_staal_buigen = fig_queue_time_staal_buigen
            newfig_queue_time_staal_koppelen = fig_queue_time_staal_koppelen
            newfig_queue_time_omhulsel_maken = fig_queue_time_omhulsel_maken
            newfig_total_queue_time = fig_total_queue_time
            newfig_gantt_disruptions = fig_gantt_disruptions
            newtotaltime = totaltime
            newsettingdistibution_dict = settingdistibution_dict
            newsortfinisheddf = sortfinisheddf.to_json(orient="split")

            return '/Manager', newfodf, newmeasures, newmeans, newlower_5_quantiles, newupper_95_quantiles, newfig_total_thoughout_time, newfig_queue_time_staal_buigen, newfig_queue_time_staal_koppelen, newfig_queue_time_omhulsel_maken, newfig_total_queue_time, newfig_gantt_disruptions, newtotaltime, newsettingdistibution_dict, newsortfinisheddf





