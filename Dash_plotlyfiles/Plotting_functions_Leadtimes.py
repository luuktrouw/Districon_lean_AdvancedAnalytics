import plotly.express as px
import datetime
import plotly.graph_objects as go
import Plotting_functions_Management

'''
This file makes all figures which are meant to be on the Lead Times page. 
It ends with the get_Leadtimes_figures function, which calls each function and stores them in a dictionary so they can be called when needed
'''

# This function plots a violin plot of the throughout times of all inventory steps and process steps
# It is handed a finished order dataframe with all the data of those orders. A boxplot or violin plot can both be used by uncommenting one
# If the one filters the longest order out, a shorter dataframe is handed in.
# it plots everything in chart using the plotly bar/violin chart function and returns this figure
def make_violin_VSM_statistics(finished_order_df):

    Step_names = ["tijd inventory staal buigen", 'tijd staal buigen', 'tijd inventory staal koppelen', 'tijd staal koppelen',
                            'tijd inventory omhulsel maken', 'tijd omhulsel maken', 'total queue time', 'total process time']

    fig = go.Figure()

    #### violin below
    # for stepname in Step_names:
    #     fig.add_trace(go.Violin(x=finished_order_df[stepname],
    #                             name=stepname,
    #                             box_visible=True,
    #                             meanline_visible=True))

    #### boxplot below
    for stepname in Step_names:
        fig.add_trace(go.Box(x=finished_order_df[stepname],
                                name=stepname,
                                #meanline_visible=True,
                             ))

    return fig

# This function plots the fraction of each reason for waiting times for a certain process step in a pie chart
# The input is the finished order dataframe with all its data and the specific process step and returns the figrue afterwards
def plot_fractions_wait_time_reasons_perschakel(finished_order_df, schakel):
    longestprocesstimesdf = finished_order_df
    percentage = 100

    # The disruption times of the specific steps are calculated by looping over all orders.
    # if the whole process is wanted, it calls the plot_fractions_wait_time_reasons function with 100% of the orders in Plotting_functions_Management.py
    sum_other_wait_time = 0
    sum_wait_time_shortage_supply = 0
    sum_wait_time_breakdowns = 0
    if schakel == 'staal buigen':
        for i in range(len(longestprocesstimesdf)):
            sum_other_wait_time += longestprocesstimesdf.iloc[i]['tijd inventory staal buigen']
            for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['supply shortage'])):
                sum_wait_time_shortage_supply += longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['supply shortage'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['supply shortage'][j][0]
            for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['breakdown'])):
                sum_wait_time_breakdowns += longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['breakdown'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['breakdown'][j][0]

    elif schakel == 'staal koppelen':
        for i in range(len(longestprocesstimesdf)):
            sum_other_wait_time += longestprocesstimesdf.iloc[i]['tijd inventory staal koppelen']
            for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['supply shortage'])):
                sum_wait_time_shortage_supply += longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['supply shortage'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['supply shortage'][j][0]
            for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['breakdown'])):
                sum_wait_time_breakdowns += longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['breakdown'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['breakdown'][j][0]

    elif schakel == 'omhulsel maken':
        for i in range(len(longestprocesstimesdf)):
            sum_other_wait_time += longestprocesstimesdf.iloc[i]['tijd inventory omhulsel maken']
            for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['supply shortage'])):
                sum_wait_time_shortage_supply += longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['supply shortage'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['supply shortage'][j][0]
            for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['breakdown'])):
                sum_wait_time_breakdowns += longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['breakdown'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['breakdown'][j][0]

    elif schakel == 'total process':
        return Plotting_functions_Management.plot_fractions_wait_time_reasons(finished_order_df, percentage)

    # the other wait times are simply the remaining bits which can not be explained by breakdowns or supply shortage
    sum_other_wait_time -= sum_wait_time_shortage_supply + sum_wait_time_breakdowns
    print([sum_other_wait_time, sum_wait_time_breakdowns, sum_wait_time_shortage_supply])

    # after all wait times are received it plots them in a pie chart using the plotly pie chart function
    fig = px.pie(values=[sum_other_wait_time, sum_wait_time_breakdowns, sum_wait_time_shortage_supply], names=['other wait times', 'breaksdowns', 'shortage supply'])

    return fig

# This figures plots all disruption during the simulation in a gantt chart.
# Its input is the measures dictionary and it used the plotly timeline function to return a figure
def plot_gantt_disruptions(measures):
    # A dictionary with all disruption names, the beginning of each interval and the ending of each interval is made
    # This is done by looping over the measures of all disruptions.
    dict_disruption_periods = {'disruptions_names': [], 'disruptions_begins':[], 'disruptions_ends':[]}

    # CURRENT DATETIME SPECIFIED date NOW
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)

    #append dict with the breakdown periods
    for i in range(len(measures['breakdown periods']['staal buigen'])):
        dict_disruption_periods['disruptions_names'].append('breakdowns staal buigen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + measures['breakdown periods']['staal buigen'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + measures['breakdown periods']['staal buigen'][i][1]))

    for i in range(len(measures['breakdown periods']['staal koppelen'])):
        dict_disruption_periods['disruptions_names'].append('breakdowns staal koppelen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + measures['breakdown periods']['staal koppelen'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + measures['breakdown periods']['staal koppelen'][i][1]))

    for i in range(len(measures['breakdown periods']['omhulsel maken'])):
        dict_disruption_periods['disruptions_names'].append('breakdowns omhulsel maken')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + measures['breakdown periods']['omhulsel maken'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + measures['breakdown periods']['omhulsel maken'][i][1]))

    #append dict with the supply shortages periods
    for i in range(len(measures['supply shortage periods']['staal buigen'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages staal buigen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + measures['supply shortage periods']['staal buigen'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + measures['supply shortage periods']['staal buigen'][i][1]))

    for i in range(len(measures['supply shortage periods']['staal koppelen'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages staal koppelen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + measures['supply shortage periods']['staal koppelen'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + measures['supply shortage periods']['staal koppelen'][i][1]))

    for i in range(len(measures['supply shortage periods']['omhulsel maken'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages omhulsel maken')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + measures['supply shortage periods']['omhulsel maken'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + measures['supply shortage periods']['omhulsel maken'][i][1]))

    # afterwards all disruptions are plotted using the ploty timeline function in one figure
    fig_all_disruptions_gantt = px.timeline(dict_disruption_periods,
                                            x_start = dict_disruption_periods['disruptions_begins'],
                                            x_end=dict_disruption_periods['disruptions_ends'],
                                            y = dict_disruption_periods['disruptions_names'])
    # one could set specific range for one day in seconds
    fig_all_disruptions_gantt.update_xaxes(range = [datetime.datetime.fromtimestamp(timestamp), datetime.datetime.fromtimestamp(timestamp + 86400)])
    #fig_all_disruptions_gantt.update_yaxes(visible=False, showticklabels=False)


    return fig_all_disruptions_gantt

# This function plots all disruptions and processing times which happened in the timespan of one certain order
# The input is the ordername and the finished order dataframe, which also contains the info of all disruptions during orders
# it returns a gantt chart with all events of that order
def plot_gantt_per_order(finishedordersdf, ordername):
    # it takes the row of the dataframe which is about the specific order
    dict_disruption_periods = {'disruptions_names': [], 'disruptions_begins': [], 'disruptions_ends': []}
    orderdf = finishedordersdf.loc[finishedordersdf['orderID'] == ordername]
    #orderdf = finishedordersdf[finishedordersdf.orderID == ordername]
    orderdf = orderdf.iloc[0]

    # CURRENT DATETIME SPECIFIED date NOW
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)

    # include the measures for when the order was in each process step
    #staal buigen
    dict_disruption_periods['disruptions_names'].append('processing staal buigen')
    dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['start tijd staal buigen']))
    dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['eind tijd staal buigen']))

    #staal koppelen
    dict_disruption_periods['disruptions_names'].append('processing staal koppelen')
    dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['start tijd staal koppelen']))
    dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['eind tijd staal koppelen']))

    #omhulsel maken
    dict_disruption_periods['disruptions_names'].append('processing omhulsel maken')
    dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['start tijd omhulsel maken']))
    dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['eind tijd omhulsel maken']))

    # make the disruption periods dict for that order
    for i in range(len(orderdf['reason inventory staal buigen']['supply shortage'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages staal buigen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory staal buigen']['supply shortage'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory staal buigen']['supply shortage'][i][1]))

    for i in range(len(orderdf['reason inventory staal buigen']['breakdown'])):
        dict_disruption_periods['disruptions_names'].append('breakdown staal buigen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory staal buigen']['breakdown'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory staal buigen']['breakdown'][i][1]))

    for i in range(len(orderdf['reason inventory staal koppelen']['supply shortage'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages staal koppelen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory staal koppelen']['supply shortage'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory staal koppelen']['supply shortage'][i][1]))

    for i in range(len(orderdf['reason inventory staal koppelen']['breakdown'])):
        dict_disruption_periods['disruptions_names'].append('breakdown staal koppelen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory staal koppelen']['breakdown'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory staal koppelen']['breakdown'][i][1]))

    for i in range(len(orderdf['reason inventory omhulsel maken']['supply shortage'])):
        if len(orderdf['reason inventory omhulsel maken']['supply shortage'][i]) == 1:
            print('hoi')
        dict_disruption_periods['disruptions_names'].append('supply shortages omhulsel maken')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory omhulsel maken']['supply shortage'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory omhulsel maken']['supply shortage'][i][1]))

    for i in range(len(orderdf['reason inventory omhulsel maken']['breakdown'])):
        dict_disruption_periods['disruptions_names'].append('breakdown omhulsel maken')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory omhulsel maken']['breakdown'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(timestamp + orderdf['reason inventory omhulsel maken']['breakdown'][i][1]))

    fig_disruptions_order_gantt = px.timeline(dict_disruption_periods,
                                            x_start = dict_disruption_periods['disruptions_begins'],
                                            x_end=dict_disruption_periods['disruptions_ends'],
                                            y = dict_disruption_periods['disruptions_names'])

    # one could set specific range as receiving order until finishing order
    #fig_disruptions_order_gantt.update_xaxes(range = [datetime.datetime.fromtimestamp(orderdf['time received']), datetime.datetime.fromtimestamp(orderdf['finish time'])])

    return fig_disruptions_order_gantt

# This function calls the functions which have no callback, and stores them in a dictionary so that they only have to be loaded once
# for the fraction wait times per schakel and the throughput times per schakel figures, the callbacks have only choice of limited options
# therefore, the figures for all options are stored for those callbacks
def get_Leadtimes_figures(finished_order_df, measures):
    Leadtimes_fig_dict = {}
    Leadtimes_fig_dict['fraction wait times per schakel'] = {}
    Leadtimes_fig_dict['throughput times per schakel'] = {}

    Leadtimes_fig_dict['VSM statistics times'] = make_violin_VSM_statistics(finished_order_df)
    Leadtimes_fig_dict['fraction wait times per schakel']['total process'] = plot_fractions_wait_time_reasons_perschakel(finished_order_df, 'total process')
    Leadtimes_fig_dict['fraction wait times per schakel']['staal buigen'] =plot_fractions_wait_time_reasons_perschakel(finished_order_df, 'staal buigen')
    Leadtimes_fig_dict['fraction wait times per schakel']['staal koppelen'] =plot_fractions_wait_time_reasons_perschakel(finished_order_df, 'staal koppelen')
    Leadtimes_fig_dict['fraction wait times per schakel']['omhulsel maken'] = plot_fractions_wait_time_reasons_perschakel(finished_order_df, 'omhulsel maken')
    Leadtimes_fig_dict['throughput times per schakel']['total throughput time'] = px.histogram(finished_order_df,x = 'total process time')
    Leadtimes_fig_dict['throughput times per schakel']['total queueing time'] = px.histogram(finished_order_df, x='total queue time')
    Leadtimes_fig_dict['throughput times per schakel']['Queueing time staal buigen'] = px.histogram(finished_order_df, x='tijd inventory staal buigen')
    Leadtimes_fig_dict['throughput times per schakel']['Queueing time staal koppelen'] = px.histogram(finished_order_df, x='tijd inventory staal koppelen')
    Leadtimes_fig_dict['throughput times per schakel']['Queueing time omhulsel maken'] = px.histogram(finished_order_df, x='tijd inventory omhulsel maken')
    Leadtimes_fig_dict['all disruption intervals'] = plot_gantt_disruptions(measures)

    return Leadtimes_fig_dict
