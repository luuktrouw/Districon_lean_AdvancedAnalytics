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

# This function calls the functions which have no callback, and stores them in a dictionary so that they only have to be loaded once
def get_Inventory_figures(measures, totaltijd):
    Inventory_fig_dict = {}

    Inventory_fig_dict['frac out of order'] = make_barchart_disruptionfracs(measures, totaltijd)
    Inventory_fig_dict['total inventory per step'] = total_inventory_per_step(measures['stock levels']['raw materials'])

    return Inventory_fig_dict


