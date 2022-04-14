
import plotly.express as px
from dash import html
import dash_bootstrap_components as dbc


def get_perc_deadlines_met(finished_orders_df):
    counter_orders_met = 0

    for i in finished_orders_df.index:
        if finished_orders_df['finish time'][i] <= finished_orders_df['deadline order'][i]:
            counter_orders_met += 1

    fraction_orders_met = counter_orders_met/len(finished_orders_df)
    percentage = round(fraction_orders_met*100,2)

    card_fracdeadlinesmade =[
        dbc.CardHeader("Deadlines made"),
        dbc.CardBody(
            [
                html.P(str(percentage)+'%', className="card-title"),
            ]
        ),
    ]

    return card_fracdeadlinesmade

def get_perc_prio_deadlines_met(finished_orders_df):
    counter_orders_met = 0
    if len(finished_orders_df)>0:
        for i in finished_orders_df.index:
            if finished_orders_df['finish time'][i] <= finished_orders_df['deadline order'][i]:
                counter_orders_met += 1

        fraction_orders_met = counter_orders_met / len(finished_orders_df)
        percentage = round(fraction_orders_met * 100, 2)

    else: percentage = 'no simulated priority orders'

    card_fracpriodeadlinesmade = [
        dbc.CardHeader("Priority deadlines made"),
        dbc.CardBody(
            [
                html.P(str(percentage) + '%', className="card-title"),
            ]
        ),
    ]

    return card_fracpriodeadlinesmade

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

def plot_fractions_wait_time_reasons(sortfinisheddf, percentage):
    longestprocesstimesdf = sortfinisheddf.head(int(percentage/100 * len(sortfinisheddf)))

    #print(len(longestprocesstimesdf))

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
            #print(j)
            sum_wait_time_breakdowns += longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['breakdown'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory staal koppelen']['breakdown'][j][0]
        for j in range(len(longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['breakdown'])):
            sum_wait_time_breakdowns += longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['breakdown'][j][1] - longestprocesstimesdf.iloc[i]['reason inventory omhulsel maken']['breakdown'][j][0]

    sum_other_wait_time -= sum_wait_time_shortage_supply + sum_wait_time_breakdowns
    print([sum_other_wait_time, sum_wait_time_breakdowns, sum_wait_time_shortage_supply])

    fig = px.pie(values=[sum_other_wait_time, sum_wait_time_breakdowns, sum_wait_time_shortage_supply], names=['other wait times', 'breaksdowns', 'shortage supply'], title='Wait time reasons')
    #fig.show()
    return fig

def get_Management_figures(finished_orders_df):
    Mananger_fig_dict = {}

    means = {'total process time': finished_orders_df['total process time'].mean(),
             'total queue time': finished_orders_df['total queue time'].mean(),
             'queue staal buigen': finished_orders_df['tijd inventory staal buigen'].mean(),
             'queue staal koppelen': finished_orders_df['tijd inventory staal koppelen'].mean(),
             'queue omhulsel maken': finished_orders_df['tijd inventory omhulsel maken'].mean(),
             'staal buigen': finished_orders_df['tijd staal buigen'].mean(),
             'staal koppelen': finished_orders_df['tijd staal koppelen'].mean(),
             'omhulsel maken': finished_orders_df['tijd omhulsel maken'].mean(),
             'total producing time': finished_orders_df['total producing time'].mean(),
             'lateness': finished_orders_df['lateness'].mean()}

    lower_5_quantiles = {'total process time': finished_orders_df['total process time'].quantile(.05),
                         'total queue time': finished_orders_df['total queue time'].quantile(.05),
                         'queue staal buigen': finished_orders_df['tijd inventory staal buigen'].quantile(.05),
                         'queue staal koppelen': finished_orders_df['tijd inventory staal koppelen'].quantile(.05),
                         'queue omhulsel maken': finished_orders_df['tijd inventory omhulsel maken'].quantile(.05),
                         'staal buigen': finished_orders_df['tijd staal buigen'].quantile(.05),
                         'staal koppelen': finished_orders_df['tijd staal koppelen'].quantile(.05),
                         'omhulsel maken': finished_orders_df['tijd omhulsel maken'].quantile(.05),
                         'total producing time': finished_orders_df['total producing time'].quantile(.05),
                         'lateness': finished_orders_df['lateness'].quantile(.05)}

    upper_95_quantiles = {'total process time': finished_orders_df['total process time'].quantile(.95),
                          'total queue time': finished_orders_df['total queue time'].quantile(.95),
                          'queue staal buigen': finished_orders_df['tijd inventory staal buigen'].quantile(.95),
                          'queue staal koppelen': finished_orders_df['tijd inventory staal koppelen'].quantile(.95),
                          'queue omhulsel maken': finished_orders_df['tijd inventory omhulsel maken'].quantile(.95),
                          'staal buigen': finished_orders_df['tijd staal buigen'].quantile(.95),
                          'staal koppelen': finished_orders_df['tijd staal koppelen'].quantile(.95),
                          'omhulsel maken': finished_orders_df['tijd omhulsel maken'].quantile(.95),
                          'total producing time': finished_orders_df['total producing time'].quantile(.95),
                          'lateness': finished_orders_df['lateness'].quantile(.95)}




    Mananger_fig_dict['card deadlines made'] = get_perc_deadlines_met(finished_orders_df)
    Mananger_fig_dict['card prio deadlines made'] = get_perc_prio_deadlines_met( finished_orders_df[finished_orders_df['high priority'] == True])
    Mananger_fig_dict['card throughout time'] = get_cardtotalthroughput_time(means, lower_5_quantiles, upper_95_quantiles)
    Mananger_fig_dict['card lateness'] = get_cardlateness_time(means, lower_5_quantiles, upper_95_quantiles)
    Mananger_fig_dict['card queue time'] = get_cardtotalwaiting_time(means, lower_5_quantiles, upper_95_quantiles)
    Mananger_fig_dict['card producing time'] = get_cardtotalproducing_time(means, lower_5_quantiles, upper_95_quantiles)

    return Mananger_fig_dict
