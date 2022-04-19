import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

'''
This file makes all figures which are meant to be on the inventory page. 
It ends with the get_inventory_figures function, which calls each function and stores them in a dictionary so they can be called when needed
'''

# This function plots the fraction of the total time that a specific disruption occurs
# it plots them in one bar chart using the plotly bar chart function
def make_barchart_disruptionfracs(measures, totaltijd):
    # the measures dictionary contains all fractions of the disruptions
    # therefore a loop over all disruptions is done to determine the total time the disruption occured.
    # (one could prevent performing the loops if one chooses to keep track of the total disruption times during the simulation as well

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

    # after the total disruption times are determined, they are divided by the total time to receive the fractions
    # after which they are plotted with the plotly bar function and the figure is returned
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

# This function plots the total time series of the stock levels of each material. To display the stock level at each time
# The input time series should be the time series of the material of interest
# it uses the plotly lines function for it
def plot_stocklevels_through_time(timeseriesstocklevel):
    # it makes x (times) values and y (stock levels) values and plots them
    xas = [timeseriesstocklevel[i][1] for i in range(len(timeseriesstocklevel))]
    yas = [timeseriesstocklevel[i][0] for i in range(len(timeseriesstocklevel))]
    dfforgraph = pd.DataFrame(dict(x = xas,y=yas))
    fig = px.line(dfforgraph, x="x", y="y", title="timeseries stock levels")

    return fig

# This function plots the fraction of time that the process step staal buigen is working on x products (so ranging from 0 to the capacity)
# with the plotly bar chart function
def plotworkstates_fractions(work_state_times):
    # first the function makes a list of the workstates with the time the step has been in that workstate, afterwards it simply makes a bar chart
    workstates = []
    fractions = []
    totalvalues = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates.append(i)
        fractions.append(round(work_state_times[i]/totalvalues,2))
    fig = px.bar(x=workstates, y=fractions, text_auto= True)
    return fig


# This function calls the functions which have no callback, and stores them in a dictionary so that they only have to be loaded once
def get_Inventory_figures(measures, totaltijd):
    Inventory_fig_dict = {}

    # create an dictionary for all work state fractions options for each process step to save all option figures
    Inventory_fig_dict['workstate fractions'] = {}

    Inventory_fig_dict['frac out of order'] = make_barchart_disruptionfracs(measures, totaltijd)
    Inventory_fig_dict['workstate fractions']['staal buigen'] = plotworkstates_fractions(measures['workstate times'][0])
    Inventory_fig_dict['workstate fractions']['staal koppelen'] = plotworkstates_fractions(measures['workstate times'][1])
    Inventory_fig_dict['workstate fractions']['omhulsel maken'] = plotworkstates_fractions(measures['workstate times'][2])

    return Inventory_fig_dict


