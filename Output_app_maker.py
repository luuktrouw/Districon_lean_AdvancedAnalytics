import dash
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import main_simulation
import plottingfunctions

#https://www.youtube.com/watch?v=hSPmj7mK6ng

############## SETTINGS

#capacity of the schakels
capacity_staalbuigen = 10
capacity_staalkoppelen = 10
capacity_omhulselmaken = 10

# distribution binnenkomen van orders
Mean_ordertime = 800
Mean_ordersize = 2
stdev_ordertime = 1
stdev_ordersize = 1

# deadline orders
Mean_order_deadline = 750
stdev_order_deadline = 30

# high priority chance
high_priority_chance = 0.001

# supply (manual stock level determined)
supply_order_interval_time = 24000
Mean_supplytime_stalen_stangen = 480
stdev_supplytime_stalen_stangen = 20
#eorderpoint_stalenstangen = 20
reorder_upto_point_stalenstangen = 1700

Mean_supplytime_koppeldraad = 480
stdev_supplytime_koppeldraad = 20
reorder_upto_point_koppeldraad = 750

Mean_supplytime_stuffing = 480
stdev_supplytime_stuffing = 20
reorder_upto_point_softstuffing = 100
reorder_upto_point_mediumstuffing = 100
reorder_upto_point_hardstuffing = 100

stdev_order_quantity_percentage_of_quantity = 0.01
# distributions processes
Mean_process0time = 720
Mean_process1time = 650
Mean_process2time = 700
stdev_process0time = 20
stdev_process1time = 40
stdev_process2time = 20

# schakel breakdowns
Mean_schakel_staalbuigen_breakdown = 24000
Mean_schakel_staalkoppelen_breakdown = 24000
Mean_schakel_omhulselmaken_breakdown = 24000
Mean_fix_staalbuigen_breakdown = 480
Mean_fix_staalkoppelen_breakdown = 480
Mean_fix_omhulselmaken_breakdown = 480

# Manual safety stocks sub assemblies
SS_gebogen_stangen = 0
SS_gekoppeld_eenpersoons = 0
SS_gekoppeld_twijfelaar =  0
SS_gekoppeld_queensize =  0
SS_gekoppeld_kingsize = 0

# calculated guess safety stocks all stock levels
#SS_gebogen_stangen, SS_gekoppeld_eenpersoons, SS_gekoppeld_twijfelaar, SS_gekoppeld_queensize, SS_gekoppeld_kingsize = 10

settingdistibution_dict = {'order time mean': Mean_ordertime, 'order time stdev': stdev_ordertime,
                           'order size mean': Mean_ordersize, 'order size stdev': stdev_ordersize,
                           'supply interval order': supply_order_interval_time,
                           'mean supply time stalen stangen': Mean_supplytime_stalen_stangen, 'stdev supply time stalen stangen': stdev_supplytime_stalen_stangen,
                           'reorder upto stalen stangen': reorder_upto_point_stalenstangen,
                           'mean supply time koppeldraad': Mean_supplytime_koppeldraad, 'stdev supply time koppeldraad': stdev_supplytime_koppeldraad,
                           'reorder upto koppeldraad': reorder_upto_point_koppeldraad,
                           'mean supply time stuffing': Mean_supplytime_stuffing, 'stdev supply time stuffing': stdev_supplytime_stuffing,
                           'reorder upto soft stuffing': reorder_upto_point_softstuffing, 'reorder upto medium stuffing': reorder_upto_point_mediumstuffing,
                           'reorder upto hard stuffing': reorder_upto_point_hardstuffing,
                           'mean staal buigen time': Mean_process0time, 'mean staal koppelen time': Mean_process1time,
                           'mean omhulsel maken time': Mean_process2time,
                           'stdev staal buigen time': stdev_process0time, 'stdev staal koppelen time': stdev_process1time,
                           'stdev omhulsel maken time': stdev_process2time,
                           'mean staal buigen breakdown': Mean_schakel_staalbuigen_breakdown,
                           'mean staal koppelen breakdown': Mean_schakel_staalkoppelen_breakdown,
                           'mean omhulsel maken breakdown': Mean_schakel_omhulselmaken_breakdown,
                           'mean fix staal buigen breakdown': Mean_fix_staalbuigen_breakdown,
                           'mean fix staal koppelen breakdown': Mean_fix_staalkoppelen_breakdown,
                           'mean fix omhulsel maken breakdown': Mean_fix_omhulselmaken_breakdown,
                           'capacity staal buigen': capacity_staalbuigen,
                           'capacity staal koppelen': capacity_staalkoppelen,
                           'capacity omhulsel maken': capacity_omhulselmaken,
                           'stddev order hoeveelheid als percentage van quantity': stdev_order_quantity_percentage_of_quantity,
                           'SS gebogen stangen': SS_gebogen_stangen,
                           'SS gekoppeld eenpersoons': SS_gekoppeld_eenpersoons,
                           'SS gekoppeld twijfelaar': SS_gekoppeld_twijfelaar,
                           'SS gekoppeld queensize': SS_gekoppeld_queensize,
                           'SS gekoppeld kingsize': SS_gekoppeld_kingsize,
                           'mean deadline order': Mean_order_deadline,
                           'stdev deadline order': stdev_order_deadline,
                           'high priority chance': high_priority_chance
                           }


##------------------------------------

fig_table_speelveld = plottingfunctions.make_fig_speelveld(settingdistibution_dict)

finished_orders_df, measures, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions = main_simulation.runsimulation(settingdistibution_dict)

sortfinisheddf = finished_orders_df.sort_values('total process time', ascending=False)
fig_some_order = plottingfunctions.plot_gantt_per_order(finished_orders_df, sortfinisheddf.iloc[0]['orderID'])

fig_pie_chart_reasons_queue = plottingfunctions.plot_fractions_wait_time_reasons(finished_orders_df, 20)

fig_order_deadlines_met = plottingfunctions.plot_fraction_deadlines_met(finished_orders_df)

testt = finished_orders_df[finished_orders_df['high priority'] == True]
if len(testt)>0:
    figorderdeadlinesmet_priority = plottingfunctions.plot_fraction_deadlines_met(finished_orders_df[finished_orders_df['high priority'] == True])


fig_stocklevels = plottingfunctions.plot_stocklevels_through_time(measures['stock levels']['raw materials']['stalen stangen'])

fig_VSM_statistics = plottingfunctions.make_fig_VSM_statistics(means, lower_5_quantiles, upper_95_quantiles)

app = dash.Dash(__name__)

app.layout = html.Div([
            html.H1("Simulation results with the given settings", style={'text-align':'center'}),
            # dcc.Dropdown(id='select speelvelddeel', options=[{'label': 'Total throughout time', 'value': 1}, {'label': 'Total queueing time', 'value': 2},
            #                 {'label': 'Queueing time staal buigen', 'value': 3}, {'label': 'Queueing time staal koppelen', 'value': 4}, {'label': 'Queueing time omhulsel maken', 'value': 5}], multi=False,
            #      value=1, style={'width': '100%'}),
            dcc.Graph(id = 'speelveld',figure =  fig_table_speelveld),
            dcc.Graph(id = 'orders met',figure =  fig_order_deadlines_met),
            dcc.Graph(id='priority orders met', figure=figorderdeadlinesmet_priority),
            dcc.Graph(id = 'VSMstatistics',figure =  fig_VSM_statistics),
            dcc.Dropdown(id = 'select measure', options = [{'label': 'Total throughout time', 'value': 1},{'label': 'Total queueing time', 'value': 2},
                          {'label': 'Queueing time staal buigen', 'value': 3},{'label': 'Queueing time staal koppelen', 'value': 4},{'label': 'Queueing time omhulsel maken', 'value': 5}], multi = False,
                        value = 1, style = {'width':'100%'}),
            html.Div(id = 'output_container', children = []),
            html.Br(),
            #dcc.Graph(id = 'queue time staal koppelen', figure = fig_queue_time_staal_koppelen),
            dcc.Graph(id = 'process measure', figure ={}),
            dcc.Graph(id = 'Gantt_all_disruptions', figure = fig_gantt_disruptions),
            dcc.Slider(0,100, id = 'slider disruption measure percentage', value = 5),
            dcc.Graph(id = 'Pie reason queue', figure ={}),
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
            dcc.Graph(id = 'stock level graph', figure ={}),
            dcc.Input(id = 'input specific order', type = 'text', placeholder= 'type orderID'),
            dcc.Graph(id = 'specific order disruptions', figure = fig_some_order),



])

@app.callback(Output(component_id= 'process measure', component_property= 'figure'),
              [Input(component_id='select measure', component_property= 'value')])
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

@app.callback(Output(component_id= 'Pie reason queue', component_property= 'figure'),
              [Input(component_id='slider disruption measure percentage', component_property= 'value')])
def update_single_order_graph(option_slctd):
    #if text in finished_orders_df['orderID']:
    figure = plottingfunctions.plot_fractions_wait_time_reasons(sortfinisheddf, option_slctd)
    return figure

@app.callback(Output(component_id= 'stock level graph', component_property= 'figure'),
              [Input(component_id='select stock graph', component_property= 'value')])
def update_stocklevelsgraph(option_slctd):
    #if text in finished_orders_df['orderID']:
    print(option_slctd)
    figure = plottingfunctions.plot_stocklevels_through_time(measures['stock levels'][option_slctd[0]][option_slctd[1]])
    return figure

@app.callback(Output(component_id= 'specific order disruptions', component_property= 'figure'),
              [Input(component_id='input specific order', component_property= 'value')])
def update_single_order_graph(option_slctd):
    #if text in finished_orders_df['orderID']:
    print(option_slctd)
    figure = plottingfunctions.plot_gantt_per_order(finished_orders_df, option_slctd)
    return figure

if __name__ == '__main__':
    app.run_server()