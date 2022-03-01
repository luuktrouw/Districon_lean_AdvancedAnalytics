import dash
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import main_simulation

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

# supply
supply_order_interval_time = 2400
Mean_supplytime_stalen_stangen = 480
stdev_supplytime_stalen_stangen = 0
#eorderpoint_stalenstangen = 20
reorder_upto_point_stalenstangen = 100

Mean_supplytime_koppeldraad = 480
stdev_supplytime_koppeldraad = 0
reorder_upto_point_koppeldraad = 10

Mean_supplytime_stuffing = 480
stdev_supplytime_stuffing = 0
reorder_upto_point_softstuffing = 1000
reorder_upto_point_mediumstuffing = 1000
reorder_upto_point_hardstuffing = 1000

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
                           'capacity omhulsel maken': capacity_omhulselmaken
                           }
fig_table_speelveld = go.Figure(data=[go.Table(
    header=dict(values=['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[['doorlooptijd staal buigen', 'doorlooptijd staal koppelen', 'doorlooptijd omhulsel maken', 'aankomst nieuwe orders',
                        'order grootte nieuwe orders', 'tijd tot nieuwe breakdown staal buigen', 'tijd tot nieuwe breakdown staal koppelen',
                        'tijd tot nieuwe breakdown omhulsel maken','tijd breakdown fixen staal buigen', 'tijd breakdown fixen staal koppelen',
                        'tijd breakdown fixen omhulsel maken', 'reorder per tijdunits', 'capacity staal buigen',
                        'capacity staal koppelen', 'capacity omhulsel maken'],
                       ['Exponential', 'Exponential', 'Normal', 'Exponential',
                        'Normal', 'Exponential','Exponential',
                        'Exponential','Exponential','Exponential',
                        'Exponential','Deterministic', 'Deterministic',
                        'Deterministic', 'Deterministic'],
                       ['no','no','no','no',
                        'no','no','no',
                        'no','no','no',
                        'no','no','no',
                        'no','no'],
                       [settingdistibution_dict['mean staal buigen time'], settingdistibution_dict['mean staal koppelen time'], settingdistibution_dict['mean omhulsel maken time'],settingdistibution_dict['order time mean'],
                        settingdistibution_dict['order size mean'], settingdistibution_dict['mean staal buigen breakdown'], settingdistibution_dict['mean staal koppelen breakdown'],
                        settingdistibution_dict['mean omhulsel maken breakdown'], settingdistibution_dict['mean fix staal buigen breakdown'], settingdistibution_dict['mean fix staal koppelen breakdown'],
                        settingdistibution_dict['mean fix omhulsel maken breakdown'], settingdistibution_dict['supply interval order'], settingdistibution_dict['capacity staal buigen'],
                        settingdistibution_dict['capacity staal koppelen'], settingdistibution_dict['capacity omhulsel maken']],
                       ['Nan', 'Nan',settingdistibution_dict['stdev omhulsel maken time'],'Nan',
                        settingdistibution_dict['order size stdev'],'Nan','Nan',
                        'Nan','Nan','Nan',
                        'Nan','Nan','Nan',
                        'Nan','Nan']
                       ],
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
], layout_height = 500 )





# fig_sankey_VSM = go.Figure(data=[go.Sankey(
#         node = dict(
#           pad = 1,
#           thickness = 20,
#           line = dict(color = "black", width = 0.1),
#           label = ["supply", "inv staal buigen", 'staal buigen', 'inv staal koppelen', 'staal koppelen', 'inv omhulsel maken', 'omhulsel maken'],
#           color = "blue"
#         ),
#         link = dict(
#           source = [0, 1, 2, 3, 4, 5, 6], # indices correspond to labels, eg A1, A2, A1, B1, ...
#           target = [1, 2, 3, 4, 5, 6, 7],
#           value = ['test', 1, 1, 1, 1, 1, 1]
#       ))])



##------------------------------------

finished_orders_df, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions = main_simulation.runsimulation(settingdistibution_dict)

fig_VSM_statistics = go.Figure(data=[go.Table(
    header=dict(values=['process step',"inv staal buigen", 'staal buigen', 'inv staal koppelen', 'staal koppelen',
                        'inv omhulsel maken', 'omhulsel maken', 'total queue time', 'total process time'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[['mean','lower 0.05 quantile - upper 95 quantile'],
                         [round(means['queue staal buigen'],1),str(round(lower_5_quantiles['queue staal buigen'],1)) + '-' +  str(round(upper_95_quantiles['queue staal buigen'],1))],
                         [round(means['staal buigen'],1),str(round(lower_5_quantiles['staal buigen'],1)) + '-' + str(round(upper_95_quantiles['staal buigen'],1))],
                         [round(means['queue staal koppelen'],1),str(round(lower_5_quantiles['queue staal koppelen'],1)) + '-' + str(round(upper_95_quantiles['queue staal koppelen'],1))],
                         [round(means['staal koppelen'],1),str(round(lower_5_quantiles['staal koppelen'],1)) + '-' +  str(round(upper_95_quantiles['staal koppelen'],1))],
                         [round(means['queue omhulsel maken'],1),str(round(lower_5_quantiles['queue omhulsel maken'],1)) + '-' + str(round(upper_95_quantiles['queue omhulsel maken'],1))],
                         [round(means['omhulsel maken'],1),str(round(lower_5_quantiles['omhulsel maken'],1)) +'-' +  str(round(upper_95_quantiles['omhulsel maken'],1))],
                         [round(means['total queue time'],1),str(round(lower_5_quantiles['total queue time'],1)) + '-' + str(round(upper_95_quantiles['total queue time'],1))],
                         [round(means['total process time'],1),str(round(lower_5_quantiles['total process time'],1)) + '-' + str(round(upper_95_quantiles['total process time'],1))]
                         ],
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])

app = dash.Dash(__name__)

app.layout = html.Div([
            html.H1("Simulation results with the given settings", style={'text-align':'center'}),
            dcc.Graph(id = 'speelveld',figure =  fig_table_speelveld),
            #dcc.Graph(id = 'VSM',figure =  fig_sankey_VSM),
            dcc.Graph(id = 'VSMstatistics',figure =  fig_VSM_statistics),
            dcc.Dropdown(id = 'select measure', options = [{'label': 'Total throughout time', 'value': 1},{'label': 'Total queueing time', 'value': 2},
                          {'label': 'Queueing time staal buigen', 'value': 3},{'label': 'Queueing time staal koppelen', 'value': 4},{'label': 'Queueing time omhulsel maken', 'value': 5}], multi = False,
                        value = 1, style = {'width':'100%'}),
            html.Div(id = 'output_container', children = []),
            html.Br(),
            #dcc.Graph(id = 'total thoughouttime', figure = fig_total_thoughout_time),
            #dcc.Graph(id = 'total queue time', figure = fig_total_queue_time),
            #dcc.Graph(id = 'queue time staal buigen', figure = fig_queue_time_staal_buigen),
            #dcc.Graph(id = 'queue time staal koppelen', figure = fig_queue_time_staal_koppelen),
            dcc.Graph(id = 'process measure', figure ={}),
            dcc.Graph(id = 'disruption_periods',figure =  fig_gantt_disruptions),



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


if __name__ == '__main__':
    app.run_server()