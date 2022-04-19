import plotly.express as px
import plotly.graph_objects as go

'''
This file contains plotting functions which are not used in the dash dashboard, but can be added if wanted
'''

# This function plots the fraction of time that the process step staal buigen is working on x products (so ranging from 0 to the capacity)
# with the plotly bar chart function
def plotworkstates_fractions_staalbuigen(work_state_times):
    # first the function makes a list of the workstates with the time the step has been in that workstate, afterwards it simply makes a bar chart
    workstates_staalbuigen = []
    values_staalbuigen = []
    totalvaluesstaalbuigen = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates_staalbuigen.append(i)
        values_staalbuigen.append(work_state_times[i]/totalvaluesstaalbuigen)
    fig1 = px.bar(dict(workstates_staalbuigen = workstates_staalbuigen, values_staalbuigen =values_staalbuigen), x='workstates_staalbuigen', y='values_staalbuigen')
    fig1.show()

# This function plots the fraction of time that the process step staal koppelen is working on x products (so ranging from 0 to the capacity)
# with the plotly bar chart function
def plotworkstates_fractions_staalkoppelen(work_state_times):
    # first the function makes a list of the workstates with the time the step has been in that workstate, afterwards it simply makes a bar chart
    workstates_staalkoppelen = []
    values_staalkoppelen = []
    totalvaluesstaalkoppelen = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates_staalkoppelen.append(i)
        values_staalkoppelen.append(work_state_times[i]/totalvaluesstaalkoppelen)
    fig2 = px.bar(dict(workstates_staalkoppelen = workstates_staalkoppelen, values_staalkoppelen =values_staalkoppelen), x='workstates_staalkoppelen', y='values_staalkoppelen')
    fig2.show()

# This function plots the fraction of time that the process step omhulsel maken is working on x products (so ranging from 0 to the capacity)
# with the plotly bar chart function
def plotworkstates_fractions_omhulselmaken(work_state_times):
    # first the function makes a list of the workstates with the time the step has been in that workstate, afterwards it simply makes a bar chart
    workstates_omhulselmaken = []
    values_omhulselmaken = []
    totalvaluesomhulselmaken = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates_omhulselmaken.append(i)
        values_omhulselmaken.append(work_state_times[i]/totalvaluesomhulselmaken)
    fig3 = px.bar(dict(workstates_omhulselmaken = workstates_omhulselmaken, values_omhulselmaken =values_omhulselmaken), x='workstates_omhulselmaken', y='values_omhulselmaken')
    fig3.show()

# This function plots the waiting time of orders before the staal buigen step in a histogram
# with the plotly histogram chart function
def wachttijd_voor_staal_buigen(finishedorders):
    # the funtion makes a list with the waiting times of all orders before staal buigen.
    wachttijd_lijst = []
    for i in range(len(finishedorders)):
        wachttijd_lijst.append(finishedorders[i]['tijd inventory staal buigen'])
    fig4 = px.histogram(dict(wachttijd_lijst = wachttijd_lijst), x = 'wachttijd_lijst')
    fig4.show()

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






