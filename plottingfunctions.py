import pandas as pd
import plotly.express as px
import datetime
import plotly.graph_objects as go
from dash import Input, Output, State, html, dcc, dash_table
import dash_bootstrap_components as dbc


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
        if len(orderdf['reason inventory omhulsel maken']['supply shortage'][i]) == 1:
            print('hoi')
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

def plot_fractions_wait_time_reasons(sortfinisheddf, percentage):
    longestprocesstimesdf = sortfinisheddf.head(int(percentage/100 * len(sortfinisheddf)))

    print(len(longestprocesstimesdf))

    # neemt totaal van alle processen, dus niet specifiek voor staal buigen bijvoorbeeld
    sum_other_wait_time = 0
    sum_wait_time_shortage_supply = 0
    sum_wait_time_breakdowns = 0
    for i in range(len(longestprocesstimesdf)):
        sum_other_wait_time += longestprocesstimesdf.iloc[i]['total queue time']

        # loop over alle process stappen & dan disruptions erin
        for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['supply shortage'])):
            sum_wait_time_shortage_supply += longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['supply shortage'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['supply shortage'][j][0]
        for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['supply shortage'])):
            sum_wait_time_shortage_supply += longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['supply shortage'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['supply shortage'][j][0]
        for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['supply shortage'])):
            sum_wait_time_shortage_supply += longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['supply shortage'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['supply shortage'][j][0]
        for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['breakdown'])):
            sum_wait_time_breakdowns += longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['breakdown'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory staal buigen']['breakdown'][j][0]
        for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['breakdown'])):
            print(j)
            sum_wait_time_breakdowns += longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['breakdown'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['breakdown'][j][0]
        for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['breakdown'])):
            sum_wait_time_breakdowns += longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['breakdown'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['breakdown'][j][0]

    sum_other_wait_time -= sum_wait_time_shortage_supply + sum_wait_time_breakdowns
    print([sum_other_wait_time, sum_wait_time_breakdowns, sum_wait_time_shortage_supply])

    fig = px.pie(values=[sum_other_wait_time, sum_wait_time_breakdowns, sum_wait_time_shortage_supply], names=['other wait times', 'breaksdowns', 'shortage supply'], title='Wait time reasons')
    #fig.show()
    return fig

def plot_fractions_wait_time_reasons_perschakel(sortfinisheddf, percentage, schakel):
    longestprocesstimesdf = sortfinisheddf.head(int(percentage/100 * len(sortfinisheddf)))

    print(len(longestprocesstimesdf))

    # neemt totaal van alle processen, dus niet specifiek voor staal buigen bijvoorbeeld
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
        return plot_fractions_wait_time_reasons(sortfinisheddf, percentage)

    sum_other_wait_time -= sum_wait_time_shortage_supply + sum_wait_time_breakdowns
    print([sum_other_wait_time, sum_wait_time_breakdowns, sum_wait_time_shortage_supply])

    fig = px.pie(values=[sum_other_wait_time, sum_wait_time_breakdowns, sum_wait_time_shortage_supply], names=['other wait times', 'breaksdowns', 'shortage supply'], title='Wait time reasons')
    #fig.show()
    return fig

def get_perc_deadlines_met(finished_orders_df):
    counter_orders_met = 0

    for i in finished_orders_df.index:
        if finished_orders_df['finish time'][i] <= finished_orders_df['deadline order'][i]:
            counter_orders_met += 1

    fraction_orders_met = counter_orders_met/len(finished_orders_df)
    percentage = round(fraction_orders_met*100,2)

    return percentage

def get_cardtotalthroughput_time(means, lower_5_quantiles, upper_95_quantiles):
    meann = str(round(means['total process time'],2))
    quantiles = str(round(lower_5_quantiles['total process time'], 1)) + '-' + str(
                                round(upper_95_quantiles['total process time'], 1))
    cardthrougputtime = [
        dbc.CardHeader("Average throughput time"),
        dbc.CardBody(
            [
                html.P(meann, className="card-title"),
                html.P(quantiles),
            ]
        ),
    ]

    return cardthrougputtime

def get_cardlateness_time(means, lower_5_quantiles, upper_95_quantiles):
    meann = str(round(means['lateness'],2))
    quantiles = str(round(lower_5_quantiles['lateness'], 1)) + '-' + str(
                                round(upper_95_quantiles['lateness'], 1))
    cardlatenesstime = [
        dbc.CardHeader("Average lateness (nu incl on time orders als 0)"),
        dbc.CardBody(
            [
                html.P(meann, className="card-title"),
                html.P(quantiles),
            ]
        ),
    ]

    return cardlatenesstime

def get_cardtotalwaiting_time(means, lower_5_quantiles, upper_95_quantiles):
    meann = str(round(means['total queue time'],2))
    quantiles = str(round(lower_5_quantiles['total queue time'], 1)) + '-' + str(
                                round(upper_95_quantiles['total queue time'], 1))
    cardwaitingtime = [
        dbc.CardHeader("Average queue time"),
        dbc.CardBody(
            [
                html.P(meann, className="card-title"),
                html.P(quantiles),
            ]
        ),
    ]

    return cardwaitingtime

def get_cardtotalproducing_time(means, lower_5_quantiles, upper_95_quantiles):
    meann = str(round(means['total producing time'],2))
    quantiles = str(round(lower_5_quantiles['total producing time'], 1)) + '-' + str(
                                round(upper_95_quantiles['total producing time'], 1))
    cardproducingtime = [
        dbc.CardHeader("Average producing time"),
        dbc.CardBody(
            [
                html.P(meann, className="card-title"),
                html.P(quantiles),
            ]
        ),
    ]

    return cardproducingtime

def plot_stocklevels_through_time(timeseriesstocklevel):
    xas = [timeseriesstocklevel[i][1] for i in range(len(timeseriesstocklevel))]
    yas = [timeseriesstocklevel[i][0] for i in range(len(timeseriesstocklevel))]
    dfforgraph = pd.DataFrame(dict(x = xas,y=yas))
    fig = px.line(dfforgraph, x="x", y="y", title="timeseries stock levels")

    return fig

def make_fig_speelveldprocessschakels(settingdistibution_dict):
    headercontent = ['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev']

    tablecontent = [['doorlooptijd staal buigen', 'Normal', 'no', settingdistibution_dict['mean staal buigen time'], settingdistibution_dict['stdev staal buigen time']],
                        ['doorlooptijd staal koppelen', 'Normal', 'no', settingdistibution_dict['mean staal koppelen time'], settingdistibution_dict['stdev staal koppelen time']],
                        ['doorlooptijd omhulsel maken', 'Normal', 'no', settingdistibution_dict['mean omhulsel maken time'], settingdistibution_dict['stdev omhulsel maken time']],
                        ['capacity staal buigen', 'Deterministic', 'no',settingdistibution_dict['capacity staal buigen'], 'Nan' ],
                        ['capacity staal koppelen', 'Deterministic', 'no', settingdistibution_dict['capacity staal koppelen'], 'Nan'],
                        ['capacity omhulsel maken', 'Deterministic', 'no', settingdistibution_dict['capacity omhulsel maken'], 'Nan'],
                        ]
    fig_table_speelveldprocessschakels = go.Figure(data=[go.Table(
                                        header=dict(values=headercontent,
                                                    line_color='darkslategray',
                                                    fill_color='lightskyblue',
                                                    align='left'),
                                        cells=dict(values= [[tablecontent[i][j] for i in range(len(tablecontent))]  for j in range(len(headercontent))  ] ,
                                                   line_color='darkslategray',
                                                   fill_color='lightcyan',
                                                   align='left')),
                                        ],
                                   layout_width = 500
                                     )

    return fig_table_speelveldprocessschakels

def make_fig_speelveldbreakdowns(settingdistibution_dict):
    headercontent = ['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev']

    tablecontent = [['tijd tot nieuwe breakdown staal buigen', 'Exponential', 'no', settingdistibution_dict['mean staal buigen breakdown'], 'Nan'],
                        ['tijd tot nieuwe breakdown staal koppelen', 'Exponential', 'no', settingdistibution_dict['mean staal koppelen breakdown'], 'Nan'],
                        ['tijd tot nieuwe breakdown omhulsel maken', 'Exponential', 'no', settingdistibution_dict['mean omhulsel maken breakdown'], 'Nan'],
                        ['tijd breakdown fixen staal buigen', 'Exponential', 'no', settingdistibution_dict['mean fix staal buigen breakdown'], 'Nan'],
                        ['tijd breakdown fixen staal koppelen', 'Exponential', 'no', settingdistibution_dict['mean fix staal koppelen breakdown'], 'Nan'],
                        ['tijd breakdown fixen omhulsel maken', 'Exponential', 'no',settingdistibution_dict['mean fix omhulsel maken breakdown'] , 'Nan'],
                        ]
    fig_table_speelveldbreakdowns = go.Figure(data=[go.Table(
                                        header=dict(values=headercontent,
                                                    line_color='darkslategray',
                                                    fill_color='lightskyblue',
                                                    align='left'),
                                        cells=dict(values= [[tablecontent[i][j] for i in range(len(tablecontent))]  for j in range(len(headercontent))  ] ,
                                                   line_color='darkslategray',
                                                   fill_color='lightcyan',
                                                   align='left')),
                                        ],
                                   layout_width = 500
                                     )

    return fig_table_speelveldbreakdowns

def make_fig_speelveldorders(settingdistibution_dict):
    headercontent = ['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev']

    tablecontent = [['aankomst nieuwe orders', 'Exponential', 'no', settingdistibution_dict['order time mean'], 'Nan'],
                        ['order grootte nieuwe orders', 'Normal', 'no',settingdistibution_dict['order size mean'],settingdistibution_dict['order size stdev'] ],
                        ['new order deadlines', 'normal', 'no', settingdistibution_dict['mean deadline order'],settingdistibution_dict['stdev deadline order']],
                        ]
    fig_table_speelveldorders = go.Figure(data=[go.Table(
                                        header=dict(values=headercontent,
                                                    line_color='darkslategray',
                                                    fill_color='lightskyblue',
                                                    align='left'),
                                        cells=dict(values= [[tablecontent[i][j] for i in range(len(tablecontent))]  for j in range(len(headercontent))  ] ,
                                                   line_color='darkslategray',
                                                   fill_color='lightcyan',
                                                   align='left')),
                                        ],
                                   layout_width = 500
                                     )

    return fig_table_speelveldorders

def make_fig_speelveldsupply(settingdistibution_dict):
    headercontent = ['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev']

    tablecontent = [[ 'reorder per tijdunits', 'Deterministic', 'no',settingdistibution_dict['supply interval order'] , 'Nan'],
                        ['reorder up to point stalen stangen', 'Deterministic', 'no',settingdistibution_dict['reorder upto stalen stangen'], 'Nan'],
                        ['reorder up to point koppeldraad', 'Deterministic', 'no',settingdistibution_dict['reorder upto koppeldraad'], 'Nan'],
                        ['reorder up to point soft stuffing', 'Deterministic', 'no',settingdistibution_dict['reorder upto soft stuffing'], 'Nan'],
                        ['reorder up to point medium stuffing', 'Deterministic', 'no', settingdistibution_dict['reorder upto medium stuffing'], 'Nan'],
                        ['reorder up to point hard stuffing', 'Deterministic', 'no', settingdistibution_dict['reorder upto hard stuffing'], 'Nan'],
                        ['Component Safety Stock gebogen stangen', 'Deterministic', 'no',settingdistibution_dict['SS gebogen stangen'], 'Nan'],
                        ['Component Safety Stock gekoppeld eenpersoons', 'Deterministic', 'no',settingdistibution_dict['SS gekoppeld eenpersoons'], 'Nan'],
                        ['Component Safety Stock gekoppeld twijfelaar', 'Deterministic', 'no',settingdistibution_dict['SS gekoppeld twijfelaar'], 'Nan'],
                        ['Component Safety Stock gekoppeld queensize', 'Deterministic', 'no',settingdistibution_dict['SS gekoppeld queensize'], 'Nan'],
                        ['Component Safety Stock gekoppeld kingsize', 'Deterministic', 'no',settingdistibution_dict[ 'SS gekoppeld kingsize'], 'Nan'],
                        ['supply time stalen stangen', 'normal', 'no',settingdistibution_dict['mean supply time stalen stangen'],settingdistibution_dict['stdev supply time stalen stangen'] ],
                        ['supply time koppeldraad', 'normal', 'no',settingdistibution_dict['mean supply time koppeldraad'],settingdistibution_dict['stdev supply time koppeldraad']],
                        ['supply time stuffing', 'normal', 'no',settingdistibution_dict['mean supply time stuffing'],settingdistibution_dict['stdev supply time stuffing']],
                        ['supply quantity error (%stdev)', 'normal', 'no','Same as ordered quantity',settingdistibution_dict['stddev order hoeveelheid als percentage van quantity']],
                        ]
    fig_table_speelveldsupply = go.Figure(data=[go.Table(
                                        header=dict(values=headercontent,
                                                    line_color='darkslategray',
                                                    fill_color='lightskyblue',
                                                    align='left'),
                                        cells=dict(values= [[tablecontent[i][j] for i in range(len(tablecontent))]  for j in range(len(headercontent))  ] ,
                                                   line_color='darkslategray',
                                                   fill_color='lightcyan',
                                                   align='left')),
                                        ],
                                   layout_width = 500
                                     )

    return fig_table_speelveldsupply

def make_fig_editablespeelveldsupply(settingdistibution_dict):
    headercontent = ['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev']

    tablecontent = [
        ['reorder per tijdunits', 'Deterministic', 'no', settingdistibution_dict['supply interval order'], 'Nan'],
        ['reorder up to point stalen stangen', 'Deterministic', 'no',
         settingdistibution_dict['reorder upto stalen stangen'], 'Nan'],
        ['reorder up to point koppeldraad', 'Deterministic', 'no', settingdistibution_dict['reorder upto koppeldraad'],
         'Nan'],
        ['reorder up to point soft stuffing', 'Deterministic', 'no',
         settingdistibution_dict['reorder upto soft stuffing'], 'Nan'],
        ['reorder up to point medium stuffing', 'Deterministic', 'no',
         settingdistibution_dict['reorder upto medium stuffing'], 'Nan'],
        ['reorder up to point hard stuffing', 'Deterministic', 'no',
         settingdistibution_dict['reorder upto hard stuffing'], 'Nan'],
        ['Component Safety Stock gebogen stangen', 'Deterministic', 'no', settingdistibution_dict['SS gebogen stangen'],
         'Nan'],
        ['Component Safety Stock gekoppeld eenpersoons', 'Deterministic', 'no',
         settingdistibution_dict['SS gekoppeld eenpersoons'], 'Nan'],
        ['Component Safety Stock gekoppeld twijfelaar', 'Deterministic', 'no',
         settingdistibution_dict['SS gekoppeld twijfelaar'], 'Nan'],
        ['Component Safety Stock gekoppeld queensize', 'Deterministic', 'no',
         settingdistibution_dict['SS gekoppeld queensize'], 'Nan'],
        ['Component Safety Stock gekoppeld kingsize', 'Deterministic', 'no',
         settingdistibution_dict['SS gekoppeld kingsize'], 'Nan'],
        ['supply time stalen stangen', 'normal', 'no', settingdistibution_dict['mean supply time stalen stangen'],
         settingdistibution_dict['stdev supply time stalen stangen']],
        ['supply time koppeldraad', 'normal', 'no', settingdistibution_dict['mean supply time koppeldraad'],
         settingdistibution_dict['stdev supply time koppeldraad']],
        ['supply time stuffing', 'normal', 'no', settingdistibution_dict['mean supply time stuffing'],
         settingdistibution_dict['stdev supply time stuffing']],
        ['supply quantity error (%stdev)', 'normal', 'no', 'Same as ordered quantity',
         settingdistibution_dict['stddev order hoeveelheid als percentage van quantity']],
        ]

    fig_table_speelveldsupply = dash_table.DataTable(id = 'settingssupply',
                                                     columns = [{'name': headercontent[i], 'id': headercontent[i]} for i in range(len(headercontent))],
                                                     data = [{headercontent[j]: tablecontent[i][j]
                                                              for j in range(len(tablecontent[i]))}
                                                             for i in range(len(tablecontent))],
                                                     editable = True,
                                                     style_cell={'textAlign': 'left',
                                                                 'font-family':'sans-serif'},
                                                     style_data={
                                                         'color': 'black',
                                                         'backgroundColor': 'white',
                                                         'whiteSpace': 'normal',
                                                         'height': 'auto',
                                                     },
                                                     style_header={
                                                         'backgroundColor': 'rgb(210, 210, 210)',
                                                         'color': 'black',
                                                         'fontWeight': 'bold',
                                                         'textAlign': 'left'
                                                     },
                                                     style_data_conditional=[
                                                         {
                                                             'if': {'row_index': 'odd'},
                                                             'backgroundColor': 'rgb(220, 220, 220)',
                                                         }
                                                     ],
                                                     page_size=6
                                                     )

    # fig_table_speelveldsupply = go.Figure(data=[go.Table(
    #     header=dict(values=headercontent,
    #                 line_color='darkslategray',
    #                 fill_color='lightskyblue',
    #                 align='left'),
    #     cells=dict(values=[[tablecontent[i][j] for i in range(len(tablecontent))] for j in range(len(headercontent))],
    #                line_color='darkslategray',
    #                fill_color='lightcyan',
    #                align='left')),
    # ],
    #     layout_width=500
    # )

    return fig_table_speelveldsupply

def make_barchart_disruptionfracs(measures, totaltijd):

    totalbreakdowntimestaalbuigen = 0
    totalbreakdowntimestaalkoppelen = 0
    totalbreakdowntimeomhulselmaken = 0
    totalsupplyshortagetimestaalbuigen = 0
    totalsupplyshortagetimestaalkoppelen = 0
    totalsupplyshortagetimeomhulselmaken = 0

    for i in range(len(measures['breakdown periods']['staal buigen'])):
        totalbreakdowntimestaalbuigen += measures['breakdown periods']['staal buigen'][i][1] - measures['breakdown periods']['staal buigen'][i][0]

    for i in range(len(measures['breakdown periods']['staal koppelen'])):
        totalbreakdowntimestaalkoppelen += measures['breakdown periods']['staal koppelen'][i][1] - measures['breakdown periods']['staal koppelen'][i][0]

    for i in range(len(measures['breakdown periods']['omhulsel maken'])):
        totalbreakdowntimeomhulselmaken += measures['breakdown periods']['omhulsel maken'][i][1] - measures['breakdown periods']['omhulsel maken'][i][0]

    for i in range(len(measures['supply shortage periods']['staal buigen'])):
        totalsupplyshortagetimestaalbuigen += measures['supply shortage periods']['staal buigen'][i][1] -   measures['supply shortage periods']['staal buigen'][i][0]

    for i in range(len(measures['supply shortage periods']['staal koppelen'])):
        totalsupplyshortagetimestaalkoppelen += measures['supply shortage periods']['staal koppelen'][i][1] -  measures['supply shortage periods']['staal koppelen'][i][0]

    for i in range(len(measures['supply shortage periods']['omhulsel maken'])):
        totalsupplyshortagetimeomhulselmaken += measures['supply shortage periods']['omhulsel maken'][i][1] - measures['supply shortage periods']['omhulsel maken'][i][0]

    fracbreakdowntimestaalbuigen = round(totalbreakdowntimestaalbuigen/totaltijd,2)
    fracbreakdowntimestaalkoppelen = round(totalbreakdowntimestaalkoppelen/totaltijd,2)
    fracbreakdowntimeomhulselmaken = round(totalbreakdowntimeomhulselmaken/totaltijd,2)
    fracsupplyshortagetimestaalbuigen = round(totalsupplyshortagetimestaalbuigen/totaltijd,2)
    fracsupplyshortagetimestaalkoppelen = round(totalsupplyshortagetimestaalkoppelen/totaltijd,2)
    fracsupplyshortagetimeomhulselmaken = round(totalsupplyshortagetimeomhulselmaken/totaltijd,2)

    fractions = [fracbreakdowntimestaalbuigen, fracbreakdowntimestaalkoppelen, fracbreakdowntimeomhulselmaken,fracsupplyshortagetimestaalbuigen ,fracsupplyshortagetimestaalkoppelen,fracsupplyshortagetimeomhulselmaken]

    disruptionnames = ['breakdown staal buigen', 'breakdown staal koppelen','breakdown omhulsel maken','supply shortage staal buigen', 'supply shortage staal koppelen','supply shortage omhulsel maken',]


    barchart_disruptionsfracs = px.bar( y=fractions, x=disruptionnames, text_auto=True,)

    return barchart_disruptionsfracs

def make_fig_VSM_statistics(means, lower_5_quantiles, upper_95_quantiles):
    fig_VSM_statistics = go.Figure(data=[go.Table(
        header=dict(values=['process step', "inv staal buigen", 'staal buigen', 'inv staal koppelen', 'staal koppelen',
                            'inv omhulsel maken', 'omhulsel maken', 'total queue time', 'total process time'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[['mean', 'lower 0.05 quantile - upper 95 quantile'],
                           [round(means['queue staal buigen'], 1),
                            str(round(lower_5_quantiles['queue staal buigen'], 1)) + '-' + str(
                                round(upper_95_quantiles['queue staal buigen'], 1))],
                           [round(means['staal buigen'], 1),
                            str(round(lower_5_quantiles['staal buigen'], 1)) + '-' + str(
                                round(upper_95_quantiles['staal buigen'], 1))],
                           [round(means['queue staal koppelen'], 1),
                            str(round(lower_5_quantiles['queue staal koppelen'], 1)) + '-' + str(
                                round(upper_95_quantiles['queue staal koppelen'], 1))],
                           [round(means['staal koppelen'], 1),
                            str(round(lower_5_quantiles['staal koppelen'], 1)) + '-' + str(
                                round(upper_95_quantiles['staal koppelen'], 1))],
                           [round(means['queue omhulsel maken'], 1),
                            str(round(lower_5_quantiles['queue omhulsel maken'], 1)) + '-' + str(
                                round(upper_95_quantiles['queue omhulsel maken'], 1))],
                           [round(means['omhulsel maken'], 1),
                            str(round(lower_5_quantiles['omhulsel maken'], 1)) + '-' + str(
                                round(upper_95_quantiles['omhulsel maken'], 1))],
                           [round(means['total queue time'], 1),
                            str(round(lower_5_quantiles['total queue time'], 1)) + '-' + str(
                                round(upper_95_quantiles['total queue time'], 1))],
                           [round(means['total process time'], 1),
                            str(round(lower_5_quantiles['total process time'], 1)) + '-' + str(
                                round(upper_95_quantiles['total process time'], 1))]
                           ],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left'))
    ])
    return fig_VSM_statistics

def make_violin_VSM_statistics(finished_order_df):

    Step_names = ["tijd inventory staal buigen", 'tijd staal buigen', 'tijd inventory staal koppelen', 'tijd staal koppelen',
                            'tijd inventory omhulsel maken', 'tijd omhulsel maken', 'total queue time', 'total process time']

    fig = go.Figure()

    #### violin below
    for stepname in Step_names:
        fig.add_trace(go.Violin(x=finished_order_df[stepname],
                                name=stepname,
                                box_visible=True,
                                meanline_visible=True))

    #### boxplot below
    # for stepname in Step_names:
    #     fig.add_trace(go.Box(x=finished_order_df[stepname],
    #                             name=stepname,
    #                             #meanline_visible=True,
    #                          ))

    return fig


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


