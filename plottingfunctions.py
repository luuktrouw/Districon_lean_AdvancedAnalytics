import pandas as pd
import plotly.express as px
import datetime
import plotly.graph_objects as go



def plotworkstates_fractions_staalbuigen(work_state_times):
    workstates_staalbuigen = []
    values_staalbuigen = []
    totalvaluesstaalbuigen = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates_staalbuigen.append(i)
        values_staalbuigen.append(work_state_times[i]/totalvaluesstaalbuigen)
    fig1 = px.bar(dict(workstates_staalbuigen = workstates_staalbuigen, values_staalbuigen =values_staalbuigen), x='workstates_staalbuigen', y='values_staalbuigen')
    fig1.show()

def plotworkstates_fractions_staalkoppelen(work_state_times):
    workstates_staalkoppelen = []
    values_staalkoppelen = []
    totalvaluesstaalkoppelen = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates_staalkoppelen.append(i)
        values_staalkoppelen.append(work_state_times[i]/totalvaluesstaalkoppelen)
    fig2 = px.bar(dict(workstates_staalkoppelen = workstates_staalkoppelen, values_staalkoppelen =values_staalkoppelen), x='workstates_staalkoppelen', y='values_staalkoppelen')
    fig2.show()

def plotworkstates_fractions_omhulselmaken(work_state_times):
    workstates_omhulselmaken = []
    values_omhulselmaken = []
    totalvaluesomhulselmaken = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates_omhulselmaken.append(i)
        values_omhulselmaken.append(work_state_times[i]/totalvaluesomhulselmaken)
    fig3 = px.bar(dict(workstates_omhulselmaken = workstates_omhulselmaken, values_omhulselmaken =values_omhulselmaken), x='workstates_omhulselmaken', y='values_omhulselmaken')
    fig3.show()


def wachttijd_voor_staal_buigen(finishedorders):
    wachttijd_lijst = []
    for i in range(len(finishedorders)):
        wachttijd_lijst.append(finishedorders[i]['tijd inventory staal buigen'])
    fig4 = px.histogram(dict(wachttijd_lijst = wachttijd_lijst), x = 'wachttijd_lijst')
    fig4.show()

def total_through_time(finished_orders_df):
    fig = px.histogram(finished_orders_df, x="total process time")
    fig.show()


def plot_gantt_disruptions(measures):
    dict_disruption_periods = {'disruptions_names': [], 'disruptions_begins':[], 'disruptions_ends':[]}

    #append dict with the breakdown periods
    for i in range(len(measures['breakdown periods']['staal buigen'])):
        dict_disruption_periods['disruptions_names'].append('breakdowns staal buigen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(measures['breakdown periods']['staal buigen'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(measures['breakdown periods']['staal buigen'][i][1]))

    for i in range(len(measures['breakdown periods']['staal koppelen'])):
        dict_disruption_periods['disruptions_names'].append('breakdowns staal koppelen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(measures['breakdown periods']['staal koppelen'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(measures['breakdown periods']['staal koppelen'][i][1]))

    for i in range(len(measures['breakdown periods']['omhulsel maken'])):
        dict_disruption_periods['disruptions_names'].append('breakdowns omhulsel maken')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(measures['breakdown periods']['omhulsel maken'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(measures['breakdown periods']['omhulsel maken'][i][1]))

    #append dict with the supply shortages periods
    for i in range(len(measures['supply shortage periods']['staal buigen'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages staal buigen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(measures['supply shortage periods']['staal buigen'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(measures['supply shortage periods']['staal buigen'][i][1]))

    for i in range(len(measures['supply shortage periods']['staal koppelen'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages staal koppelen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(measures['supply shortage periods']['staal koppelen'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(measures['supply shortage periods']['staal koppelen'][i][1]))

    for i in range(len(measures['supply shortage periods']['omhulsel maken'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages omhulsel maken')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(measures['supply shortage periods']['omhulsel maken'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(measures['supply shortage periods']['omhulsel maken'][i][1]))

    fig_all_disruptions_gantt = px.timeline(dict_disruption_periods,
                                            x_start = dict_disruption_periods['disruptions_begins'],
                                            x_end=dict_disruption_periods['disruptions_ends'],
                                            y = dict_disruption_periods['disruptions_names'])

    #fig_all_disruptions_gantt.show()

    return fig_all_disruptions_gantt

def plot_gantt_per_order(finishedordersdf, ordername):
    dict_disruption_periods = {'disruptions_names': [], 'disruptions_begins': [], 'disruptions_ends': []}
    orderdf = finishedordersdf.loc[finishedordersdf['orderID'] == ordername]
    orderdf = orderdf.iloc[0]

    # include the measures for when the order was in each process step
    #staal buigen
    dict_disruption_periods['disruptions_names'].append('processing staal buigen')
    dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(orderdf['start tijd staal buigen']))
    dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(orderdf['eind tijd staal buigen']))

    #staal koppelen
    dict_disruption_periods['disruptions_names'].append('processing staal koppelen')
    dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(orderdf['start tijd staal koppelen']))
    dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(orderdf['eind tijd staal koppelen']))

    #omhulsel maken
    dict_disruption_periods['disruptions_names'].append('processing omhulsel maken')
    dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(orderdf['start tijd omhulsel maken']))
    dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(orderdf['eind tijd omhulsel maken']))

    # make the disruption periods dict for that order
    for i in range(len(orderdf['reason inventory staal buigen']['supply shortage'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages staal buigen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory staal buigen']['supply shortage'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory staal buigen']['supply shortage'][i][1]))

    for i in range(len(orderdf['reason inventory staal buigen']['breakdown'])):
        dict_disruption_periods['disruptions_names'].append('breakdown staal buigen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory staal buigen']['breakdown'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory staal buigen']['breakdown'][i][1]))

    for i in range(len(orderdf['reason inventory staal koppelen']['supply shortage'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages staal koppelen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory staal koppelen']['supply shortage'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory staal koppelen']['supply shortage'][i][1]))

    for i in range(len(orderdf['reason inventory staal koppelen']['breakdown'])):
        dict_disruption_periods['disruptions_names'].append('breakdown staal koppelen')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory staal koppelen']['breakdown'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory staal koppelen']['breakdown'][i][1]))

    for i in range(len(orderdf['reason inventory omhulsel maken']['supply shortage'])):
        dict_disruption_periods['disruptions_names'].append('supply shortages omhulsel maken')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory omhulsel maken']['supply shortage'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory omhulsel maken']['supply shortage'][i][1]))

    for i in range(len(orderdf['reason inventory omhulsel maken']['breakdown'])):
        dict_disruption_periods['disruptions_names'].append('breakdown omhulsel maken')
        dict_disruption_periods['disruptions_begins'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory omhulsel maken']['breakdown'][i][0]))
        dict_disruption_periods['disruptions_ends'].append(datetime.datetime.fromtimestamp(orderdf['reason inventory omhulsel maken']['breakdown'][i][1]))

    fig_disruptions_order_gantt = px.timeline(dict_disruption_periods,
                                            x_start = dict_disruption_periods['disruptions_begins'],
                                            x_end=dict_disruption_periods['disruptions_ends'],
                                            y = dict_disruption_periods['disruptions_names'])

    #set range as receiving order until finishing order
    fig_disruptions_order_gantt.update_xaxes(range = [datetime.datetime.fromtimestamp(orderdf['time received']), datetime.datetime.fromtimestamp(orderdf['finish time'])])

    #fig_disruptions_order_gantt.show()

    return fig_disruptions_order_gantt

def plot_fractions_wait_time_reasons(finishedordersdf):

    # neemt totaal van alle processen, dus niet specifiek voor staal buigen bijvoorbeeld
    sum_other_wait_time = 0
    sum_wait_time_shortage_supply = 0
    sum_wait_time_breakdowns = 0
    for i in range(len(finishedordersdf)):
        sum_other_wait_time += finishedordersdf.iloc[i]['total queue time']

        # loop over alle process stappen & dan disruptions erin
        for j in range(len(finishedordersdf.iloc[i]['reason inventory staal buigen']['supply shortage'])):
            sum_wait_time_shortage_supply += finishedordersdf.iloc[i]['reason inventory staal buigen']['supply shortage'][j][1] - finishedordersdf.iloc[i]['reason inventory staal buigen']['supply shortage'][j][0]
        for j in range(len(finishedordersdf.iloc[i]['reason inventory staal koppelen']['supply shortage'])):
            sum_wait_time_shortage_supply += finishedordersdf.iloc[i]['reason inventory staal koppelen']['supply shortage'][j][1] - finishedordersdf.iloc[i]['reason inventory staal koppelen']['supply shortage'][j][0]
        for j in range(len(finishedordersdf.iloc[i]['reason inventory omhulsel maken']['supply shortage'])):
            sum_wait_time_shortage_supply += finishedordersdf.iloc[i]['reason inventory omhulsel maken']['supply shortage'][j][1] - finishedordersdf.iloc[i]['reason inventory omhulsel maken']['supply shortage'][j][0]

        for j in range(len(finishedordersdf.iloc[i]['reason inventory staal buigen']['breakdown'])):
            sum_wait_time_breakdowns += finishedordersdf.iloc[i]['reason inventory staal buigen']['breakdown'][j][1] - finishedordersdf.iloc[i]['reason inventory staal buigen']['breakdown'][j][0]
        for j in range(len(finishedordersdf.iloc[i]['reason inventory staal koppelen']['breakdown'])):
            sum_wait_time_breakdowns += finishedordersdf.iloc[i]['reason inventory staal koppelen']['breakdown'][j][1] - finishedordersdf.iloc[i]['reason inventory staal koppelen']['breakdown'][j][0]
        for j in range(len(finishedordersdf.iloc[i]['reason inventory omhulsel maken']['breakdown'])):
            sum_wait_time_breakdowns += finishedordersdf.iloc[i]['reason inventory omhulsel maken']['breakdown'][j][1] - finishedordersdf.iloc[i]['reason inventory omhulsel maken']['breakdown'][j][0]

    sum_other_wait_time -= sum_wait_time_shortage_supply + sum_wait_time_breakdowns

    fig = px.pie(values=[sum_other_wait_time, sum_wait_time_breakdowns, sum_wait_time_shortage_supply], names=['other wait times', 'breaksdowns', 'shortage supply'], title='Wait time reasons')
    #fig.show()
    return fig

def plot_fraction_deadlines_met(finished_orders_df):
    counter_orders_met = 0

    for i in range(len(finished_orders_df)):
        if finished_orders_df['finish time'][i] <= finished_orders_df['deadline order'][i]:
            counter_orders_met += 1

    fraction_orders_met = counter_orders_met/len(finished_orders_df)

    fig_order_deadlines_met = go.Figure(data=[go.Table(
        header=dict(values=['Percentage deadlines met'],
                    line_color='darkslategray',
                    fill_color='lightskyblue'),
        cells=dict(values=[[fraction_orders_met]]), columnwidth= 30)
    ])

    return fig_order_deadlines_met

def make_fig_speelveld(settingdistibution_dict):
    fig_table_speelveld = go.Figure(data=[go.Table(
        header=dict(values=['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[['doorlooptijd staal buigen', 'doorlooptijd staal koppelen', 'doorlooptijd omhulsel maken',
                            'aankomst nieuwe orders',
                            'order grootte nieuwe orders', 'tijd tot nieuwe breakdown staal buigen',
                            'tijd tot nieuwe breakdown staal koppelen',
                            'tijd tot nieuwe breakdown omhulsel maken', 'tijd breakdown fixen staal buigen',
                            'tijd breakdown fixen staal koppelen',
                            'tijd breakdown fixen omhulsel maken', 'reorder per tijdunits', 'capacity staal buigen',
                            'capacity staal koppelen', 'capacity omhulsel maken'],
                           ['Exponential', 'Exponential', 'Normal', 'Exponential',
                            'Normal', 'Exponential', 'Exponential',
                            'Exponential', 'Exponential', 'Exponential',
                            'Exponential', 'Deterministic', 'Deterministic',
                            'Deterministic', 'Deterministic'],
                           ['no', 'no', 'no', 'no',
                            'no', 'no', 'no',
                            'no', 'no', 'no',
                            'no', 'no', 'no',
                            'no', 'no'],
                           [settingdistibution_dict['mean staal buigen time'],
                            settingdistibution_dict['mean staal koppelen time'],
                            settingdistibution_dict['mean omhulsel maken time'],
                            settingdistibution_dict['order time mean'],
                            settingdistibution_dict['order size mean'],
                            settingdistibution_dict['mean staal buigen breakdown'],
                            settingdistibution_dict['mean staal koppelen breakdown'],
                            settingdistibution_dict['mean omhulsel maken breakdown'],
                            settingdistibution_dict['mean fix staal buigen breakdown'],
                            settingdistibution_dict['mean fix staal koppelen breakdown'],
                            settingdistibution_dict['mean fix omhulsel maken breakdown'],
                            settingdistibution_dict['supply interval order'],
                            settingdistibution_dict['capacity staal buigen'],
                            settingdistibution_dict['capacity staal koppelen'],
                            settingdistibution_dict['capacity omhulsel maken']],
                           ['Nan', 'Nan', settingdistibution_dict['stdev omhulsel maken time'], 'Nan',
                            settingdistibution_dict['order size stdev'], 'Nan', 'Nan',
                            'Nan', 'Nan', 'Nan',
                            'Nan', 'Nan', 'Nan',
                            'Nan', 'Nan']
                           ],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left'))
    ], layout_height=500)

    return fig_table_speelveld


def Make_kpi_figures(finished_orders_df):

    fig_total_thoughout_time = px.histogram(finished_orders_df,x = 'total process time')
    #fig_total_thoughout_time.show()

    #orted_finished_orders_df = finished_orders_df.sort_values('total process time', ascending=False)
    #fig_total_thoughout_time = px.bar(sorted_finished_orders_df,x = 'index', y = 'total process time', hover_name= 'orderID')

    fig_queue_time_staal_buigen = px.histogram(finished_orders_df, x='tijd inventory staal buigen')
    #fig_queue_time_staal_buigen.show()

    fig_queue_time_staal_koppelen = px.histogram(finished_orders_df, x='tijd inventory staal koppelen')
    #fig_queue_time_staal_koppelen.show()

    fig_queue_time_omhulsel_maken = px.histogram(finished_orders_df, x='tijd inventory omhulsel maken')
    #fig_queue_time_omhulsel_maken.show()

    fig_total_queue_time = px.histogram(finished_orders_df, x='total queue time')
    #fig_total_queue_time.show()

    return fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time


