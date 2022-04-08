from scipy.stats import norm
import numpy as np
import statistics

# it might be possible disruptions are going on at the end of the simulation, in that case we set the finish time as the end time of the simuolation
# this function closes all disruption measures if they are not closed yet (so still going on)
def close_disruption_measures(measures, time):
    if len(measures['breakdown periods']['staal buigen']) >0:
        if len(measures['breakdown periods']['staal buigen'][-1]) == 1:
            measures['breakdown periods']['staal buigen'][-1].append(time)

    if len(measures['breakdown periods']['staal koppelen']) >0:
        if len(measures['breakdown periods']['staal koppelen'][-1]) == 1:
            measures['breakdown periods']['staal koppelen'][-1].append(time)

    if len(measures['breakdown periods']['omhulsel maken']) >0:
        if len(measures['breakdown periods']['omhulsel maken'][-1]) == 1:
            measures['breakdown periods']['omhulsel maken'][-1].append(time)

    if len(measures['supply shortage periods']['staal buigen']) > 0:
        if len(measures['supply shortage periods']['staal buigen'][-1]) == 1:
            measures['supply shortage periods']['staal buigen'][-1].append(time)

    if len(measures['supply shortage periods']['staal koppelen']) > 0:
        if len(measures['supply shortage periods']['staal koppelen'][-1]) == 1:
            measures['supply shortage periods']['staal koppelen'][-1].append(time)

    if len(measures['supply shortage periods']['omhulsel maken']) > 0:
        if len(measures['supply shortage periods']['omhulsel maken'][-1]) == 1:
            measures['supply shortage periods']['omhulsel maken'][-1].append(time)
    return measures

# this function checks whether the input value is float or not (used for settings table, values should be float)
def checkiffloat_editabledata(string):
    try:
        float(string)
        return float(string)
    except ValueError:
        return string

# reads in the data from the editable tables which is in dash. The values are set by hand, so changes also need to be made by hand in this function
def read_supply_editabledata(dataorders, datasupply, dataschakels, databreakdowns):
    # it creates a new settingdistribution dictionary and also checks it the elements are floats
    settingdistribution_dict = {}

    #orders settings
    settingdistribution_dict['order time mean'] = checkiffloat_editabledata(dataorders[0]['Mean'])
    settingdistribution_dict['order time stdev'] = checkiffloat_editabledata(dataorders[0]['stdev'])
    settingdistribution_dict['order size mean'] =checkiffloat_editabledata(dataorders[1]['Mean'])
    settingdistribution_dict['order size stdev'] =checkiffloat_editabledata(dataorders[1]['stdev'])
    settingdistribution_dict['mean deadline order'] =checkiffloat_editabledata(dataorders[2]['Mean'])
    settingdistribution_dict['stdev deadline order'] =checkiffloat_editabledata(dataorders[2]['stdev'])

    #supply settings
    settingdistribution_dict['supply interval order'] = checkiffloat_editabledata(datasupply[0]['Mean'])
    settingdistribution_dict['reorder upto stalen stangen'] = int(checkiffloat_editabledata(datasupply[1]['Mean']))
    settingdistribution_dict['reorder upto koppeldraad'] =int(checkiffloat_editabledata(datasupply[2]['Mean']))
    settingdistribution_dict['reorder upto soft stuffing'] =int(checkiffloat_editabledata(datasupply[3]['Mean']))
    settingdistribution_dict['reorder upto medium stuffing'] =int(checkiffloat_editabledata(datasupply[4]['Mean']))
    settingdistribution_dict['reorder upto hard stuffing'] =int(checkiffloat_editabledata(datasupply[5]['Mean']))
    settingdistribution_dict['SS gebogen stangen'] = int(checkiffloat_editabledata(datasupply[6]['Mean']))
    settingdistribution_dict['SS gekoppeld eenpersoons'] =int(checkiffloat_editabledata(datasupply[7]['Mean']))
    settingdistribution_dict['SS gekoppeld twijfelaar'] =int(checkiffloat_editabledata(datasupply[8]['Mean']))
    settingdistribution_dict['SS gekoppeld queensize'] =int(checkiffloat_editabledata(datasupply[9]['Mean']))
    settingdistribution_dict['SS gekoppeld kingsize'] =int(checkiffloat_editabledata(datasupply[10]['Mean']))
    settingdistribution_dict['mean supply time stalen stangen'] =checkiffloat_editabledata(datasupply[11]['Mean'])
    settingdistribution_dict['stdev supply time stalen stangen'] =checkiffloat_editabledata(datasupply[11]['stdev'])
    settingdistribution_dict['mean supply time koppeldraad'] =checkiffloat_editabledata(datasupply[12]['Mean'])
    settingdistribution_dict['stdev supply time koppeldraad'] =checkiffloat_editabledata(datasupply[12]['stdev'])
    settingdistribution_dict['mean supply time stuffing'] = checkiffloat_editabledata(datasupply[13]['Mean'])
    settingdistribution_dict['stdev supply time stuffing'] =checkiffloat_editabledata(datasupply[13]['stdev'])
    settingdistribution_dict['stddev order hoeveelheid als percentage van quantity'] =checkiffloat_editabledata(datasupply[14]['stdev'])

    # process schakels settings
    settingdistribution_dict['mean staal buigen time'] = checkiffloat_editabledata(dataschakels[0]['Mean'])
    settingdistribution_dict['stdev staal buigen time'] =checkiffloat_editabledata(dataschakels[0]['stdev'])
    settingdistribution_dict['mean staal koppelen time'] =checkiffloat_editabledata(dataschakels[1]['Mean'])
    settingdistribution_dict['stdev staal koppelen time'] =checkiffloat_editabledata(dataschakels[1]['stdev'])
    settingdistribution_dict['mean omhulsel maken time'] =checkiffloat_editabledata(dataschakels[2]['Mean'])
    settingdistribution_dict['stdev omhulsel maken time'] =checkiffloat_editabledata(dataschakels[2]['stdev'])
    settingdistribution_dict['capacity staal buigen'] =int(checkiffloat_editabledata(dataschakels[3]['Mean']))
    settingdistribution_dict['capacity staal koppelen'] =int(checkiffloat_editabledata(dataschakels[4]['Mean']))
    settingdistribution_dict['capacity omhulsel maken'] =int(checkiffloat_editabledata(dataschakels[5]['Mean']))

    # breakdowns settings
    settingdistribution_dict['mean staal buigen breakdown'] =checkiffloat_editabledata(databreakdowns[0]['Mean'])
    settingdistribution_dict['mean staal koppelen breakdown'] =checkiffloat_editabledata(databreakdowns[1]['Mean'])
    settingdistribution_dict['mean omhulsel maken breakdown'] =checkiffloat_editabledata(databreakdowns[2]['Mean'])
    settingdistribution_dict['mean fix staal buigen breakdown'] =checkiffloat_editabledata(databreakdowns[3]['Mean'])
    settingdistribution_dict['mean fix staal koppelen breakdown'] =checkiffloat_editabledata(databreakdowns[4]['Mean'])
    settingdistribution_dict['mean fix omhulsel maken breakdown'] =checkiffloat_editabledata(databreakdowns[5]['Mean'])

    # overig, nog toe te voegen in editable op dash
    settingdistribution_dict['high priority chance']= 0.01
    settingdistribution_dict['wanted succes rate']= 0.9

    return settingdistribution_dict

# some process steps might not be finished for some orders
# for example if omhulsel maken is done, the order is registered as finished, but it is possible the staal buigen fase is still in the process, due to intermediate stocks
# it deletes those order since they are not completely finished.
#sommige , bijvoorbeeld als de order al wel klaar is (omhulsel maken klaar), maar nog niet staal buigen ding heeft afgerond en dan stopt de tijd plots. dam telt t niet als helemaal klaar, dus verwijder uit finished orders
def delete_nonfinished_orders_disruptions(finished_orders):
    for i in reversed(range(len(finished_orders))):
        if np.isnan(finished_orders['eind tijd staal buigen'][i]):
            finished_orders = finished_orders.drop(i)

        elif np.isnan(finished_orders['eind tijd staal koppelen'][i]):
            finished_orders = finished_orders.drop(i)

    return finished_orders

# This function calculates the theoretical (with multiple assumptions) reorder upto points and changes the setting distrubution dict to that
def calculateSafetyStocks(setting_dict):
    # determine average orders in order interval
    averagenumorders = setting_dict['supply interval order']/setting_dict['order time mean']

    # determine average deadline duration
    averagedeadlinestaalbuigen = setting_dict['mean deadline order']
    averagedeadlinestaalkoppelen = setting_dict['mean deadline order']
    averagedeadlineomhulselmaken = setting_dict['mean deadline order']

    # average breakdown disruption time per order
    averagebreakdownfraction_staalbuigen = setting_dict['mean fix staal buigen breakdown']/(setting_dict['mean fix staal buigen breakdown']+setting_dict['mean staal buigen breakdown'])
    averagebreakdownfraction_staalkoppelen = setting_dict['mean fix staal koppelen breakdown']/(setting_dict['mean fix staal koppelen breakdown']+setting_dict['mean staal koppelen breakdown'])
    averagebreakdownfraction_omhulselmaken = setting_dict['mean fix omhulsel maken breakdown']/(setting_dict['mean fix omhulsel maken breakdown']+setting_dict['mean omhulsel maken breakdown'])


    # determine average needed raw materials in order interval
    # based on functie in get order info qua hoeveelheden en kansen op wat voor order
    averageneededstalenstangen = (1/4*8 +1/4*10 +1/4*14 + 1/4*16) * averagenumorders
    averageneededkoppeldraad = (1/2*4 + 1/2*6)*averagenumorders
    averageneededsoftstuffing = 1/3*1*averagenumorders
    averageneededmediumstuffing = 1/3*1*averagenumorders
    averageneededhardstuffing = 1/3*1*averagenumorders

    #determine the right hand side uit WORD voor alle raw materials
    RHSstaalbuigen = averagedeadlinestaalbuigen*(1-averagebreakdownfraction_staalbuigen)/averageneededstalenstangen
    RHSstaalkoppelen = averagedeadlinestaalkoppelen*(1-averagebreakdownfraction_staalkoppelen)/averageneededkoppeldraad
    RHSsoftstuffuing = averagedeadlineomhulselmaken*(1-averagebreakdownfraction_omhulselmaken)/averageneededsoftstuffing
    RHSmediumstuffuing = averagedeadlineomhulselmaken*(1-averagebreakdownfraction_omhulselmaken)/averageneededmediumstuffing
    RHShardstuffuing = averagedeadlineomhulselmaken*(1-averagebreakdownfraction_omhulselmaken)/averageneededhardstuffing


    #voor normal distributions calculate the standard inverse cdf for the needed percentage
    stdnormalinvcdfvalue = statistics.NormalDist().inv_cdf(setting_dict['wanted succes rate'])

    #determine for normal distributed processes the needed value of SS
    SSstalenstangen = (setting_dict['mean staal buigen time'] + stdnormalinvcdfvalue*setting_dict['stdev staal buigen time'])/RHSstaalbuigen
    setting_dict['reorder upto stalen stangen'] = int(SSstalenstangen)

    SSkoppeldraad = (setting_dict['mean staal koppelen time'] + stdnormalinvcdfvalue*setting_dict['stdev staal koppelen time'])/RHSstaalkoppelen
    setting_dict['reorder upto koppeldraad'] = int(SSkoppeldraad)

    SSsoftstuffing = (setting_dict['mean omhulsel maken time'] + stdnormalinvcdfvalue*setting_dict['stdev omhulsel maken time'])/RHSsoftstuffuing
    setting_dict['reorder upto soft stuffing'] = int(SSsoftstuffing)

    SSmediumstuffing = (setting_dict['mean omhulsel maken time'] + stdnormalinvcdfvalue*setting_dict['stdev omhulsel maken time'])/RHSmediumstuffuing
    setting_dict['reorder upto medium stuffing'] = int(SSmediumstuffing)

    SShardstuffing = (setting_dict['mean omhulsel maken time'] + stdnormalinvcdfvalue*setting_dict['stdev omhulsel maken time'])/RHShardstuffuing
    setting_dict['reorder upto hard stuffing'] = int(SShardstuffing)

    return setting_dict



