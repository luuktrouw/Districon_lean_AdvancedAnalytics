import plotly.express as px
import plotly.graph_objects as go

'''
This file contains plotting functions which are not used in the dash dashboard, but can be added if wanted
'''

# This figure plots the level of inventory of one process step in a violin plot against the fraction of time.
# It does this in a violin or box plot.
# all inventories at a certain prodcution step combined, so that the capacity of the warehouse can be investigated (weights not included yet)
def total_inventory_per_step(timeseriesstocklevel):
    # first it loops over the time series of the stock levels and determine the how long it has been in that state
    totalstocklevels = {}
    for i in timeseriesstocklevel.keys():
        for j in range(0,len(timeseriesstocklevel[i])-1 , 2 ):
            if timeseriesstocklevel[i][j][0] in totalstocklevels.keys():
                totalstocklevels[timeseriesstocklevel[i][j][0]] += timeseriesstocklevel[i][j+1][1] - timeseriesstocklevel[i][j][1]
            else:
                totalstocklevels[timeseriesstocklevel[i][j][0]] = timeseriesstocklevel[i][j + 1][1] - timeseriesstocklevel[i][j][1]
    print(totalstocklevels)
    # afterwards (THIS TAKES LONG FOR LARGE INSTANCES, SO look for solution) it makes one data point for each unit of time in a certain state
    # and plots it in a violin/boxplot afterwards, this is a very long list so takes long. Afterwards returns the figure of one process step
    violindata = [i  for i in totalstocklevels.keys() for j in range(int(totalstocklevels[i]/10))]

    Step_names = ["inventory"]

    fig = go.Figure()

    #### violin below
    # for stepname in Step_names:
    #     fig.add_trace(go.Violin(x=finished_order_df[stepname],
    #                             name=stepname,
    #                             box_visible=True,
    #                             meanline_visible=True))

    #### boxplot below
    for stepname in Step_names:
        fig.add_trace(go.Box(y=violindata,
                                name=stepname,
                                #meanline_visible=True,
                             ))

    fig.show()

    return fig

# This function makes a table of the 'Statistics' in the VSM, namely the throughput times of all inventory steps and process steps with its quantiles
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






