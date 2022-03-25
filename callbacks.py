
from dash.dependencies import Input, Output

import dash
import pandas as pd
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from Pagelayouts import get_pagelayouts
import main_simulation
import plottingfunctions
import Load_settings

settingdistibution_dict = Load_settings.load_settings()

finished_orders_df, measures, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions, totaltime = main_simulation.runsimulation(settingdistibution_dict)
print('huh')

sortfinisheddf = finished_orders_df.sort_values('total process time', ascending=False)

def get_callbacks(app):
    @app.callback(Output(component_id= 'stock level graph', component_property= 'figure'),
                  [Input(component_id='select stock graph', component_property= 'value')])
    def update_stocklevelsgraph(option_slctd):
        #if text in finished_orders_df['orderID']:
        print(option_slctd)
        figure = plottingfunctions.plot_stocklevels_through_time(measures['stock levels'][option_slctd[0]][option_slctd[1]])
        return figure

    @app.callback(Output(component_id='process measure', component_property='figure'),
                  [Input(component_id='select measure', component_property='value')])
    def update_graph(option_slctd):
        if option_slctd == 1:
            figu = fig_total_thoughout_time
        elif option_slctd == 2:
            figu = fig_total_queue_time
        elif option_slctd == 3:
            figu = fig_queue_time_staal_buigen
        elif option_slctd == 4:
            figu = fig_queue_time_staal_koppelen
        elif option_slctd == 5:
            figu = fig_queue_time_omhulsel_maken

        return figu

    @app.callback(Output(component_id='Pie reason queue', component_property='figure'),
                  [Input(component_id='slider disruption measure percentage', component_property='value')])
    def update_single_order_graph(option_slctd):
        # if text in finished_orders_df['orderID']:
        figure = plottingfunctions.plot_fractions_wait_time_reasons(sortfinisheddf, option_slctd)
        return figure

    @app.callback(Output(component_id='schakel wait times', component_property='figure'),
                  [Input(component_id='select schakel waittimes', component_property='value')])
    def update_single_order_graph(option_slctd):
        # if text in finished_orders_df['orderID']:
        figure = plottingfunctions.plot_fractions_wait_time_reasons_perschakel(sortfinisheddf, 100, option_slctd)
        return figure

    # @app.callback(Output(component_id= 'stock level graph', component_property= 'figure'),
    #               [Input(component_id='select stock graph', component_property= 'value')])
    # def update_stocklevelsgraph(option_slctd):
    #     #if text in finished_orders_df['orderID']:
    #     print(option_slctd)
    #     figure = plottingfunctions.plot_stocklevels_through_time(measures['stock levels'][option_slctd[0]][option_slctd[1]])
    #     return figure

    @app.callback(Output(component_id='specific order disruptions', component_property='figure'),
                  [Input(component_id='input specific order', component_property='value')])
    def update_single_order_graph(option_slctd):
        # if text in finished_orders_df['orderID']:
        print(option_slctd)
        figure = plottingfunctions.plot_gantt_per_order(finished_orders_df, option_slctd)
        return figure

    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        page_manager, page_settings, page_inventory, page_leadtimes = get_pagelayouts(settingdistibution_dict)
        if pathname == '/Manager':
            return page_manager
        elif pathname == '/Settings':
            return page_settings
        elif pathname == '/Inventory':
            return page_inventory
        elif pathname == '/Lead_times':
            return page_leadtimes
        else:
            return page_manager