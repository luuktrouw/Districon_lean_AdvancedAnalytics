import pandas as pd
import plotly.express as px

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

def plot_stocklevels_through_time(timeseriesstocklevel):
    xas = [timeseriesstocklevel[i][1] for i in range(len(timeseriesstocklevel))]
    yas = [timeseriesstocklevel[i][0] for i in range(len(timeseriesstocklevel))]
    dfforgraph = pd.DataFrame(dict(x = xas,y=yas))
    fig = px.line(dfforgraph, x="x", y="y", title="timeseries stock levels")

    return fig

def get_Inventory_figures(measures, totaltijd):
    Inventory_fig_dict = {}

    Inventory_fig_dict['frac out of order'] = make_barchart_disruptionfracs(measures, totaltijd)

    return Inventory_fig_dict


