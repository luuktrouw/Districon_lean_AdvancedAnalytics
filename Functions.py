from scipy.stats import norm
import numpy as np
import statistics

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

def read_supply_editabledata(data):



#sommige disruptions kunnen nog niet gesloten zijn, bijvoorbeeld als de order al wel klaar is (omhulsel maken klaar), maar nog niet staal buigen ding heeft afgerond en dan stopt de tijd plots. dam telt t niet als helemaal klaar, dus verwijder uit finished orders
def delete_nonfinished_orders_disruptions(finished_orders):
    for i in reversed(range(len(finished_orders))):
        if np.isnan(finished_orders['eind tijd staal buigen'][i]):
            finished_orders = finished_orders.drop(i)

        elif np.isnan(finished_orders['eind tijd staal koppelen'][i]):
            finished_orders = finished_orders.drop(i)

    return finished_orders

def exponential_quantile(mean, quantile):
    return -math.log(1-quantile)*mean

def normal_quantile(mean, stdev, quantile):
    return mean + stdev * norm.ppf(quantile)

def histdata_quantile(data, quantile):
    return np.quantile(data, quantile)

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



