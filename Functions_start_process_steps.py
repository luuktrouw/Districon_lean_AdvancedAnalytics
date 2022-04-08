import Functions_get_info
import math
from bisect import bisect

'''
This file contains functions which start the processing of orders in process steps
For each process step, they the relevant function tries to run the first item from queue, 
until there is nothing in queue anymore, or until the first order can not be processed due to any reason
A function should be called if something changes with respect to that process step (for example a new order in queue or process step finishes an order)
'''

def start_process_staal_buigen(instance, settingdistibution_dict):
    # what goes in the machine:
    while len(instance.inventories[0]) > 0 and instance.capacities[0] - instance.work_state[0][0] >= instance.inventories[0][0][1] and all(instance.materialstate[0][i] >= instance.inventories[0][0][2]['bill of materials']['staal buigen']['raw material'][i] for i in instance.inventories[0][0][2]['bill of materials']['staal buigen']['raw material'].keys()):
        newprocessing_order = instance.inventories[0].pop(0)

        # update the material state and the measures
        for i in newprocessing_order[2]['bill of materials']['staal buigen']['raw material'].keys():
            # for the measures, add before and after the updating to have the complete lines
            instance.measures['stock levels']['raw materials'][i].append([instance.materialstate[0][i], instance.tijd])
            instance.materialstate[0][i] -= newprocessing_order[2]['bill of materials']['staal buigen']['raw material'][i]
            instance.measures['stock levels']['raw materials'][i].append([instance.materialstate[0][i], instance.tijd])

        instance.measures['workstate times'][0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
        instance.work_state[0][0] += newprocessing_order[1]
        instance.work_state[0][1] = instance.tijd
        finish_time_this_order = instance.tijd + Functions_get_info.get_length_staal_buigen(settingdistibution_dict['mean staal buigen time'], settingdistibution_dict['stdev staal buigen time'])
        finish_time_index = bisect(instance.orders_inprocess0, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal buigen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal buigen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal buigen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal buigen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal buigen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal buigen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess0.insert(finish_time_index, newprocessing_order)

    #if there are still order in the queue, update de supply shortage measure als er te weinig matirials zijn
    if  len(instance.inventories[0])>0:
        if all(instance.materialstate[0][i] >= instance.inventories[0][0][2]['bill of materials']['staal buigen']['raw material'][i] for i in instance.inventories[0][0][2]['bill of materials']['staal buigen']['raw material'].keys()) == False:
            for i in range(len(instance.inventories[0])):
                if len(instance.inventories[0][i][2]['reason inventory staal buigen']['supply shortage']) == 0 or len(instance.inventories[0][i][2]['reason inventory staal buigen']['supply shortage'][-1]) == 2:
                    instance.inventories[0][i][2]['reason inventory staal buigen']['supply shortage'].append([instance.tijd])
            # if this is the first order with supply shortage, start the supply shortage measure
            if len(instance.measures['supply shortage periods']['staal buigen']) == 0 or len(instance.measures['supply shortage periods']['staal buigen'][-1]) == 2:
                instance.measures['supply shortage periods']['staal buigen'].append([instance.tijd])

        if instance.capacities[0] == 0:
            for i in range(len(instance.inventories[0])):
                if len(instance.inventories[0][i][2]['reason inventory staal buigen']['breakdown']) == 0 or len(instance.inventories[0][i][2]['reason inventory staal buigen']['breakdown'][-1]) == 2:
                    instance.inventories[0][i][2]['reason inventory staal buigen']['breakdown'].append([instance.tijd])

    return instance

def start_process_staal_koppelen(instance, settingdistibution_dict):
    # what goes in the machine:
    while len(instance.inventories[1]) > 0 and instance.capacities[1] - instance.work_state[1][0] >= instance.inventories[1][0][1] and all(instance.materialstate[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen']['raw material'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen']['raw material'].keys()) \
            and all(instance.stockstate_subassemblies[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen']['subassembly'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen']['subassembly'].keys()):
        newprocessing_order = instance.inventories[1].pop(0)

        instance.measures['workstate times'][1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
        instance.work_state[1][0] += newprocessing_order[1]
        instance.work_state[1][1] = instance.tijd

        # update the raw material state and the measures
        for i in newprocessing_order[2]['bill of materials']['staal koppelen']['raw material'].keys():
            # for the measures, add before and after the updating to have the complete lines
            instance.measures['stock levels']['raw materials'][i].append([instance.materialstate[1][i], instance.tijd])
            instance.materialstate[1][i] -= newprocessing_order[2]['bill of materials']['staal koppelen']['raw material'][i]
            instance.measures['stock levels']['raw materials'][i].append([instance.materialstate[1][i], instance.tijd])

        # update the subassembly state and the measures
        for i in newprocessing_order[2]['bill of materials']['staal koppelen']['subassembly'].keys():
            # for the measures, add before and after the updating to have the complete lines
            instance.measures['stock levels']['subassemblies'][i].append([instance.stockstate_subassemblies[1][i], instance.tijd])
            instance.stockstate_subassemblies[1][i] -= newprocessing_order[2]['bill of materials']['staal koppelen']['subassembly'][i]
            instance.measures['stock levels']['subassemblies'][i].append([instance.stockstate_subassemblies[1][i], instance.tijd])

        finish_time_this_order =  instance.tijd + Functions_get_info.get_length_staal_koppelen(settingdistibution_dict['mean staal koppelen time'], settingdistibution_dict['stdev staal koppelen time'])
        finish_time_index = bisect(instance.orders_inprocess1, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal koppelen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal koppelen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal koppelen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal koppelen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal koppelen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal koppelen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess1.insert(finish_time_index, newprocessing_order)


    #if there are still orders in the queue, update de supply shortage measure als er te weinig matirials zijn
    if  len(instance.inventories[1])>0:
        if all(instance.materialstate[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen']['raw material'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen']['raw material'].keys()) == False or \
                all(instance.stockstate_subassemblies[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen']['subassembly'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen']['subassembly'].keys()) == False:
            for i in range(len(instance.inventories[1])):
                if len(instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage']) == 0 or len(instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage'][-1]) == 2:
                    instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage'].append([instance.tijd])
            # if this is the first order with supply shortage, start the supply shortage measure
            if len(instance.measures['supply shortage periods']['staal koppelen']) == 0 or len(instance.measures['supply shortage periods']['staal koppelen'][-1]) == 2:
                instance.measures['supply shortage periods']['staal koppelen'].append([instance.tijd])

        if instance.capacities[1] == 0:
            for i in range(len(instance.inventories[1])):
                if len(instance.inventories[1][i][2]['reason inventory staal koppelen']['breakdown']) == 0 or len(instance.inventories[1][i][2]['reason inventory staal koppelen']['breakdown'][-1]) == 2:
                    instance.inventories[1][i][2]['reason inventory staal koppelen']['breakdown'].append([instance.tijd])

    return instance

def start_process_omhulsel_maken(instance, settingdistibution_dict):
    # what goes in the machine:
    while len(instance.inventories[2]) > 0 and instance.capacities[2] - instance.work_state[2][0] >= instance.inventories[2][0][1] and all(instance.materialstate[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['raw material'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['raw material'].keys())\
            and all(instance.stockstate_subassemblies[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['subassembly'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['subassembly'].keys()):
        newprocessing_order = instance.inventories[2].pop(0)

        instance.measures['workstate times'][2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
        instance.work_state[2][0] += newprocessing_order[1]
        instance.work_state[2][1] = instance.tijd

        # update the raw material state and the measures
        for i in newprocessing_order[2]['bill of materials']['omhulsel maken']['raw material'].keys():
            # for the measures, add before and after the updating to have the complete lines
            instance.measures['stock levels']['raw materials'][i].append([instance.materialstate[2][i], instance.tijd])
            instance.materialstate[2][i] -= newprocessing_order[2]['bill of materials']['omhulsel maken']['raw material'][i]
            instance.measures['stock levels']['raw materials'][i].append([instance.materialstate[2][i], instance.tijd])

        # update the subassembly state and the measures
        for i in newprocessing_order[2]['bill of materials']['omhulsel maken']['subassembly'].keys():
            # for the measures, add before and after the updating to have the complete lines
            instance.measures['stock levels']['subassemblies'][i].append([instance.stockstate_subassemblies[2][i], instance.tijd])
            instance.stockstate_subassemblies[2][i] -= newprocessing_order[2]['bill of materials']['omhulsel maken']['subassembly'][i]
            instance.measures['stock levels']['subassemblies'][i].append([instance.stockstate_subassemblies[2][i], instance.tijd])

        finish_time_this_order =  instance.tijd + Functions_get_info.get_length_omhulsel_plaatsen(settingdistibution_dict['mean omhulsel maken time'],settingdistibution_dict['stdev omhulsel maken time'] )
        finish_time_index = bisect(instance.orders_inprocess2, [finish_time_this_order])

        newprocessing_order[2]['start tijd omhulsel maken'] = instance.tijd
        newprocessing_order[2]['eind tijd omhulsel maken'] = finish_time_this_order
        newprocessing_order[2]['tijd omhulsel maken'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory omhulsel maken'] = instance.tijd
        newprocessing_order[2]['tijd inventory omhulsel maken'] = instance.tijd - newprocessing_order[2]['start tijd inventory omhulsel maken']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess2.insert(finish_time_index, newprocessing_order)

    #if there are still order in the queue, update de supply shortage measure als er te weinig matirials zijn
    if  len(instance.inventories[2])>0:
        if all(instance.materialstate[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['raw material'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['raw material'].keys()) == False or \
                all(instance.stockstate_subassemblies[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['subassembly'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['subassembly'].keys()) == False:
            for i in range(len(instance.inventories[2])):
                if len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage']) == 0 or len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage'][-1]) == 2:
                    instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage'].append([instance.tijd])
            # if this is the first order with supply shortage, start the supply shortage measure
            if len(instance.measures['supply shortage periods']['omhulsel maken']) == 0 or len(instance.measures['supply shortage periods']['omhulsel maken'][-1]) == 2:
                instance.measures['supply shortage periods']['omhulsel maken'].append([instance.tijd])

        if instance.capacities[2] == 0:
            for i in range(len(instance.inventories[2])):
                if len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['breakdown']) == 0 or len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['breakdown'][-1]) == 2:
                    instance.inventories[2][i][2]['reason inventory omhulsel maken']['breakdown'].append([instance.tijd])

    return instance
