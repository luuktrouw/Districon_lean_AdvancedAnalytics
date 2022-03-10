from scipy.stats import norm
import numpy as np

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

def exponential_quantile(mean, quantile):
    return -math.log(1-quantile)*mean

def normal_quantile(mean, stdev, quantile):
    return mean + stdev * norm.ppf(quantile)

def histdata_quantile(data, quantile):
    return np.quantile(data, quantile)


