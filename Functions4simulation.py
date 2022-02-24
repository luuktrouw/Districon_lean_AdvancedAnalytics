import numpy as np
import math
from bisect import bisect
import random


def get_order_size(Mean_ordersize, stdev_ordersize):
    size = round(np.random.normal(Mean_ordersize, stdev_ordersize), 0)
    #print('size of next order: ', size)
    return size

def get_length_next_staalbuigen_breakdown(Mean_schakel_staalbuigen_breakdown):
    time = round(np.random.exponential(Mean_schakel_staalbuigen_breakdown), 0)
    return time

def get_length_next_staalkoppelen_breakdown(Mean_schakel_staalkoppelen_breakdown):
    time = round(np.random.exponential(Mean_schakel_staalkoppelen_breakdown), 0)
    return time

def get_length_next_omhulselmaken_breakdown(Mean_schakel_omhulselmaken_breakdown):
    time = round(np.random.exponential(Mean_schakel_omhulselmaken_breakdown), 0)
    return time

def get_length_fix_staalbuigen_breakdown(Mean_fix_staalbuigen_breakdown):
    time = round(np.random.exponential(Mean_fix_staalbuigen_breakdown), 0)
    return time

def get_length_fix_staalkoppelen_breakdown(Mean_fix_staalkoppelen_breakdown):
    time = round(np.random.exponential(Mean_fix_staalkoppelen_breakdown), 0)
    return time

def get_length_fix_omhulselmaken_breakdown(Mean_fix_omhulselmaken_breakdown):
    time = round(np.random.exponential(Mean_fix_omhulselmaken_breakdown), 0)
    return time

def get_supplytime_stalen_stangen(Mean_supplytime_stalen_stangen, stdev_supplytime_stalen_stangen):
    time = round(np.random.normal(Mean_supplytime_stalen_stangen, stdev_supplytime_stalen_stangen), 0)
    #time = round(np.random.exponential(Mean_supplytime_stalen_stangen), 0)
    #print('size of next order: ', size)
    return time

def get_supplytime_koppeldraad(Mean_supplytime_koppeldraad, stdev_supplytime_koppeldraad):
    time = round(np.random.normal(Mean_supplytime_koppeldraad, stdev_supplytime_koppeldraad), 0)
    #time = round(np.random.exponential(Mean_supplytime_koppeldraad), 0)
    #print('size of next order: ', size)
    return time

def get_supplytime_stuffing(Mean_supplytime_stuffing, stdev_supplytime_stuffing):
    time = round(np.random.normal(Mean_supplytime_stuffing, stdev_supplytime_stuffing), 0)
    #time = round(np.random.exponential(Mean_supplytime_stuffing), 0)
    #print('size of next order: ', size)
    return time

def get_length_neworder(Mean_ordertime, stdev_ordersize):

    #tijd = round(np.random.exponential(Mean_ordertime, stdev_ordersize), 1)
    tijd = round(np.random.exponential(Mean_ordertime), 1)
    #print('time until next order: ', tijd)
    return tijd

def get_length_staal_buigen(Mean_process0time):
    #tijd = round(np.random.normal(Mean_process0time, stdev_process0time), 1)
    tijd = round(np.random.exponential(Mean_process0time), 1)
    #print('new time schakel 0: ', tijd)
    return tijd

def get_length_staal_koppelen(Mean_process1time):
    #tijd = round(np.random.normal(Mean_process1time, stdev_process1time), 1)
    tijd = round(np.random.exponential(Mean_process1time), 1)
    #print('new time schakel 1: ', tijd)
    return tijd

def get_length_omhulsel_plaatsen(Mean_process2time, stdev_process2time):
    tijd = round(np.random.normal(Mean_process2time, stdev_process2time), 1)
    #print('new time schakel 2: ', tijd)
    return tijd

def get_neworderinfo(Mean_ordersize, stdev_ordersize):
    ordersize = get_order_size(Mean_ordersize, stdev_ordersize)
    if ordersize <= 0:
        ordersize = 1

    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    sign1 = random.choice(letters)
    sign2 = random.choice(letters)
    sign3 = random.choice(letters)
    sign4 = random.choice(letters)
    orderID = 'Order-' + sign1 + sign2 + sign3 + sign4

    softnesstypes = ['hard', 'medium', 'soft']
    softness = random.choice(softnesstypes)

    sizetypes = ['eenpersoons', 'twijfelaar', 'queen size', 'king size']
    sizethisorder = random.choice(sizetypes)

    billofmaterials = {}
    billofmaterials['staal buigen'] = {}
    billofmaterials['staal koppelen'] = {}
    billofmaterials['omhulsel maken'] = {}

    if sizethisorder == 'eenpersoons':
        billofmaterials['staal buigen']['stalen stangen'] = 8
        billofmaterials['staal koppelen']['koppeldraad'] = 4
        if softness == 'soft':
            billofmaterials['omhulsel maken']['soft stuffing'] = 1
        elif softness == 'medium':
            billofmaterials['omhulsel maken']['medium stuffing'] = 1
        elif softness == 'hard':
            billofmaterials['omhulsel maken']['hard stuffing'] = 1

    elif sizethisorder == 'twijfelaar':
        billofmaterials['staal buigen']['stalen stangen'] = 10
        billofmaterials['staal koppelen']['koppeldraad'] = 4
        if softness == 'soft':
            billofmaterials['omhulsel maken']['soft stuffing'] = 1
        elif softness == 'medium':
            billofmaterials['omhulsel maken']['medium stuffing'] = 1
        elif softness == 'hard':
            billofmaterials['omhulsel maken']['hard stuffing'] = 1

    elif sizethisorder == 'queen size':
        billofmaterials['staal buigen']['stalen stangen'] = 14
        billofmaterials['staal koppelen']['koppeldraad'] = 6
        if softness == 'soft':
            billofmaterials['omhulsel maken']['soft stuffing'] = 1
        elif softness == 'medium':
            billofmaterials['omhulsel maken']['medium stuffing'] = 1
        elif softness == 'hard':
            billofmaterials['omhulsel maken']['hard stuffing'] = 1

    elif sizethisorder == 'king size':
        billofmaterials['staal buigen']['stalen stangen'] = 16
        billofmaterials['staal koppelen']['koppeldraad'] = 6
        if softness == 'soft':
            billofmaterials['omhulsel maken']['soft stuffing'] = 1
        elif softness == 'medium':
            billofmaterials['omhulsel maken']['medium stuffing'] = 1
        elif softness == 'hard':
            billofmaterials['omhulsel maken']['hard stuffing'] = 1

    return orderID, ordersize, softness, sizethisorder, billofmaterials

###### ----------- BELOW are event functions, above are time/size functions

def event_neworder(instance, settingdistibution_dict):

    orderID, ordersize, softness, sizethisorder, billofmaterials = get_neworderinfo(settingdistibution_dict['order size mean'], settingdistibution_dict['order size stdev'])

    orderdict = {'orderID': orderID, 'softnesstype': softness, 'size': sizethisorder, 'bill of materials': billofmaterials, 'time received': instance.tijd,
                 'reason inventory staal buigen': {'supply shortage':[], 'breakdown':[], 'waiting on other orders':[]},
                 'reason inventory staal koppelen': {'supply shortage':[], 'breakdown':[], 'waiting on other orders':[]},
                 'reason inventory omhulsel maken':{'supply shortage':[], 'breakdown':[], 'waiting on other orders':[]}}

    #instance.t_neworder = instance.tijd + get_length_neworder()
    instance.nexteventtimes['new order'] = instance.tijd + get_length_neworder(settingdistibution_dict['order time mean'], settingdistibution_dict['order time stdev'])
    if instance.capacities[0] - instance.work_state[0][0] >= ordersize and len(instance.inventories[0]) == 0 and all(instance.materialstate[0][i] >= orderdict['bill of materials']['staal buigen'][i] for i in orderdict['bill of materials']['staal buigen'].keys()):

        for i in orderdict['bill of materials']['staal buigen'].keys():
            instance.materialstate[0][i] -= orderdict['bill of materials']['staal buigen'][i]

        '''
        # if materials too low, order up to a certain level.
        if instance.materialstate[0]['stalen stangen'] <= reorderpoint_stalenstangen and len(instance.supplyorders_stalenstangen_inprocess) == 1:
            instance.supplyorders_stalenstangen_inprocess.insert(0,[instance.tijd + get_supplytime_stalen_stangen(), reorder_upto_point_stalenstangen -instance.materialstate[0]['stalen stangen']])
        '''

        instance.measures['workstate times'][0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
        instance.work_state[0][0] += ordersize
        instance.work_state[0][1] = instance.tijd
        finish_time_this_order =  instance.tijd + get_length_staal_buigen(settingdistibution_dict['mean staal buigen time'])
        finish_time_index = bisect(instance.orders_inprocess0, [finish_time_this_order])

        orderdict['start tijd staal buigen'] = instance.tijd
        orderdict['eind tijd staal buigen'] = finish_time_this_order
        orderdict['tijd staal buigen'] = finish_time_this_order - instance.tijd
        orderdict['start tijd inventory staal buigen'] = instance.tijd
        orderdict['eind tijd inventory staal buigen'] = instance.tijd
        orderdict['tijd inventory staal buigen']  = 0

        instance.orders_inprocess0.insert(finish_time_index, [finish_time_this_order, ordersize, orderdict])

    else:
        orderdict['start tijd inventory staal buigen'] = instance.tijd
        instance.inventories[0].append([math.inf, ordersize, orderdict])

        # update measures // reason of going into inventory(queue)
        if all(instance.materialstate[0][i] >= instance.inventories[0][0][2]['bill of materials']['staal buigen'][i] for i in instance.inventories[0][0][2]['bill of materials']['staal buigen'].keys()) == False:
            orderdict['reason inventory staal buigen']['supply shortage'].append([instance.tijd])
        if instance.capacities[0] == 0:
            orderdict['reason inventory staal buigen']['breakdown'].append([instance.tijd])


    instance.nexteventtimes["staal buigen klaar"] = instance.orders_inprocess0[0][0]

    return instance

def event_staal_buigen_klaar(instance, settingdistibution_dict):
    # update the machine itself
    processed_order = instance.orders_inprocess0.pop(0)
    instance.measures['workstate times'][0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
    instance.work_state[0][0] -= processed_order[1]
    instance.work_state[0][1] = instance.tijd

    # what goes in the machine:
    while len(instance.inventories[0]) > 0 and instance.capacities[0] - instance.work_state[0][0] >= instance.inventories[0][0][1] and all(instance.materialstate[0][i] >= instance.inventories[0][0][2]['bill of materials']['staal buigen'][i] for i in instance.inventories[0][0][2]['bill of materials']['staal buigen'].keys()):
        newprocessing_order = instance.inventories[0].pop(0)

        for i in newprocessing_order[2]['bill of materials']['staal buigen'].keys():
            instance.materialstate[0][i] -= newprocessing_order[2]['bill of materials']['staal buigen'][i]

        '''
        # if materials to low, order up to a certain level.
        if instance.materialstate[0]['stalen stangen'] <= reorderpoint_stalenstangen and len(instance.supplyorders_stalenstangen_inprocess) == 1:
            instance.supplyorders_stalenstangen_inprocess.insert(0,[instance.tijd + get_supplytime_stalen_stangen(), reorder_upto_point_stalenstangen -instance.materialstate[0]['stalen stangen']])
        '''


        instance.measures['workstate times'][0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
        instance.work_state[0][0] += newprocessing_order[1]
        instance.work_state[0][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_length_staal_buigen(settingdistibution_dict['mean staal buigen time'])
        finish_time_index = bisect(instance.orders_inprocess0, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal buigen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal buigen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal buigen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal buigen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal buigen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal buigen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess0.insert(finish_time_index, newprocessing_order)

    # what goes out of the machine:
    if instance.capacities[1] - instance.work_state[1][0] >= processed_order[1] and len(instance.inventories[1]) == 0 and all(instance.materialstate[1][i] >= processed_order[2]['bill of materials']['staal koppelen'][i] for i in processed_order[2]['bill of materials']['staal koppelen'].keys()):
        instance.measures['workstate times'][1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
        instance.work_state[1][0] += processed_order[1]
        instance.work_state[1][1] = instance.tijd

        for i in processed_order[2]['bill of materials']['staal koppelen'].keys():
            instance.materialstate[1][i] -= processed_order[2]['bill of materials']['staal koppelen'][i]


        finish_time_this_order = instance.tijd + get_length_staal_koppelen(settingdistibution_dict['mean staal koppelen time'])
        finish_time_index = bisect(instance.orders_inprocess1, [finish_time_this_order])

        processed_order[2]['start tijd staal koppelen'] = instance.tijd
        processed_order[2]['eind tijd staal koppelen'] = finish_time_this_order
        processed_order[2]['tijd staal koppelen'] = finish_time_this_order - instance.tijd
        processed_order[2]['start tijd inventory staal koppelen'] = instance.tijd
        processed_order[2]['eind tijd inventory staal koppelen'] = instance.tijd
        processed_order[2]['tijd inventory staal koppelen'] = 0

        processed_order[0] = finish_time_this_order

        instance.orders_inprocess1.insert(finish_time_index, processed_order)
    else:
        processed_order[0] = math.inf
        processed_order[2]['start tijd inventory staal koppelen'] = instance.tijd

        # if breakdown, houdt dit bij in de measure van de order
        if instance.capacities[1] == 0:
            processed_order[2]['reason inventory staal koppelen']['breakdown'].append([instance.tijd])
        if len(instance.inventories[1]) >0:
            if all(instance.materialstate[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen'].keys()) == False:
                processed_order['reason inventory staal koppelen']['supply shortage'].append([instance.tijd])
        else:
            if all(instance.materialstate[1][i] >= processed_order[2]['bill of materials']['staal koppelen'][i] for i in processed_order[2]['bill of materials']['staal koppelen'].keys()) == False:
                processed_order['reason inventory staal koppelen']['supply shortage'].append([instance.tijd])

        instance.inventories[1].append(processed_order)

    instance.nexteventtimes["staal buigen klaar"] = instance.orders_inprocess0[0][0]
    instance.nexteventtimes['staal koppelen klaar'] = instance.orders_inprocess1[0][0]

    return instance

def event_staal_koppelen_klaar(instance, settingdistibution_dict):
    # update the machine itself
    processed_order = instance.orders_inprocess1.pop(0)
    instance.measures['workstate times'][1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
    instance.work_state[1][0] -= processed_order[1]
    instance.work_state[1][1] = instance.tijd

    # what goes in the machine:
    while len(instance.inventories[1]) > 0 and instance.capacities[1] - instance.work_state[1][0] >= instance.inventories[1][0][1] and all(instance.materialstate[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen'].keys()):
        newprocessing_order = instance.inventories[1].pop(0)

        instance.measures['workstate times'][1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
        instance.work_state[1][0] += newprocessing_order[1]
        instance.work_state[1][1] = instance.tijd

        for i in newprocessing_order[2]['bill of materials']['staal koppelen'].keys():
            instance.materialstate[1][i] -= newprocessing_order[2]['bill of materials']['staal koppelen'][i]

        finish_time_this_order =  instance.tijd + get_length_staal_koppelen(settingdistibution_dict['mean staal koppelen time'])
        finish_time_index = bisect(instance.orders_inprocess1, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal koppelen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal koppelen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal koppelen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal koppelen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal koppelen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal koppelen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess1.insert(finish_time_index, newprocessing_order)

    # what goes out of the machine:
    if instance.capacities[2] - instance.work_state[2][0] >= processed_order[1] and len(instance.inventories[2]) == 0 and all(instance.materialstate[2][i] >= processed_order[2]['bill of materials']['omhulsel maken'][i] for i in processed_order[2]['bill of materials']['omhulsel maken'].keys()):
        instance.measures['workstate times'][2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
        instance.work_state[2][0] += processed_order[1]
        instance.work_state[2][1] = instance.tijd

        for i in processed_order[2]['bill of materials']['omhulsel maken'].keys():
            instance.materialstate[2][i] -= processed_order[2]['bill of materials']['omhulsel maken'][i]

        finish_time_this_order = instance.tijd + get_length_omhulsel_plaatsen(settingdistibution_dict['mean omhulsel maken time'], settingdistibution_dict['stdev omhulsel maken time'])
        finish_time_index = bisect(instance.orders_inprocess2, [finish_time_this_order])

        processed_order[2]['start tijd omhulsel maken'] = instance.tijd
        processed_order[2]['eind tijd omhulsel maken'] = finish_time_this_order
        processed_order[2]['tijd omhulsel maken'] = finish_time_this_order - instance.tijd
        processed_order[2]['start tijd inventory omhulsel maken'] = instance.tijd
        processed_order[2]['eind tijd inventory omhulsel maken'] = instance.tijd
        processed_order[2]['tijd inventory omhulsel maken'] = 0

        processed_order[0] = finish_time_this_order

        instance.orders_inprocess2.insert(finish_time_index, processed_order)

    else:
        processed_order[0] = math.inf
        processed_order[2]['start tijd inventory omhulsel maken'] = instance.tijd

        # if breakdown, houdt dit bij in de measure van de order
        if instance.capacities[2] == 0:
            processed_order[2]['reason inventory omhulsel maken']['breakdown'].append([instance.tijd])
        if len(instance.inventories[2]) >0:
            if all(instance.materialstate[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken'].keys()) == False:
                processed_order['reason inventory omhulsel maken']['supply shortage'].append([instance.tijd])
        else:
            if all(instance.materialstate[2][i] >= processed_order[2]['bill of materials']['omhulsel maken'][i] for i in processed_order[2]['bill of materials']['omhulsel maken'].keys()) == False:
                processed_order['reason inventory omhulsel maken']['supply shortage'].append([instance.tijd])

        instance.inventories[2].append(processed_order)

    instance.nexteventtimes['staal koppelen klaar'] = instance.orders_inprocess1[0][0]
    instance.nexteventtimes["omhulsel klaar"] = instance.orders_inprocess2[0][0]

    return instance

def event_omhulsel_klaar(instance, settingdistibution_dict):
    # update the machine itself
    processed_order = instance.orders_inprocess2.pop(0)
    instance.measures['workstate times'][2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
    instance.work_state[2][0] -= processed_order[1]
    instance.work_state[2][1] = instance.tijd

    processed_order[2]['finish time'] = instance.tijd
    processed_order[2]['total process time'] =  processed_order[2]['finish time'] - processed_order[2]['time received']
    instance.finishedorders.append(processed_order[2])

    # update amount produced
    #print('one batch produced of size:', processed_order[1])
    instance.amountproduced += processed_order[1]

    # what goes in the machine:
    while len(instance.inventories[2]) > 0 and instance.capacities[2] - instance.work_state[2][0] >= instance.inventories[2][0][1] and all(instance.materialstate[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken'].keys()):
        newprocessing_order = instance.inventories[2].pop(0)

        instance.measures['workstate times'][2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
        instance.work_state[2][0] += newprocessing_order[1]
        instance.work_state[2][1] = instance.tijd

        for i in newprocessing_order[2]['bill of materials']['omhulsel maken'].keys():
            instance.materialstate[2][i] -= newprocessing_order[2]['bill of materials']['omhulsel maken'][i]

        finish_time_this_order =  instance.tijd + get_length_omhulsel_plaatsen(settingdistibution_dict['mean omhulsel maken time'],settingdistibution_dict['stdev omhulsel maken time'] )
        finish_time_index = bisect(instance.orders_inprocess2, [finish_time_this_order])

        newprocessing_order[2]['start tijd omhulsel maken'] = instance.tijd
        newprocessing_order[2]['eind tijd omhulsel maken'] = finish_time_this_order
        newprocessing_order[2]['tijd omhulsel maken'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory omhulsel maken'] = instance.tijd
        newprocessing_order[2]['tijd inventory omhulsel maken'] = instance.tijd - newprocessing_order[2]['start tijd inventory omhulsel maken']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess2.insert(finish_time_index, newprocessing_order)
    instance.nexteventtimes["omhulsel klaar"] = instance.orders_inprocess2[0][0]

    return instance

def event_order_new_stalen_stangen(instance, settingdistibution_dict):
    instance.nexteventtimes['order new stalen stangen'] += settingdistibution_dict['supply interval order']
    timeoftheorder = instance.tijd + get_supplytime_stalen_stangen(settingdistibution_dict['mean supply time stalen stangen'], settingdistibution_dict['stdev supply time stalen stangen'])
    instance.supplyorders_stalenstangen_inprocess.insert(0,[timeoftheorder, settingdistibution_dict['reorder upto stalen stangen'] -instance.materialstate[0]['stalen stangen']])
    instance.nexteventtimes['supply stalen stangen'] = timeoftheorder

    return instance

def event_order_new_koppeldraad(instance, settingdistibution_dict):
    instance.nexteventtimes['order new koppeldraad'] += settingdistibution_dict['supply interval order']
    timeoftheorder = instance.tijd + get_supplytime_koppeldraad(settingdistibution_dict['mean supply time koppeldraad'], settingdistibution_dict['stdev supply time koppeldraad'])
    instance.supplyorders_koppeldraad_inprocess.insert(0,[timeoftheorder, settingdistibution_dict['reorder upto koppeldraad'] -instance.materialstate[1]['koppeldraad']])
    instance.nexteventtimes['supply koppeldraad'] = timeoftheorder
    return instance

def event_order_new_stuffing(instance, settingdistibution_dict):
    instance.nexteventtimes['order new stuffing'] += settingdistibution_dict['supply interval order']
    timeoftheorder = instance.tijd + get_supplytime_stuffing(settingdistibution_dict['mean supply time stuffing'], settingdistibution_dict['stdev supply time stuffing'])
    instance.supplyorders_stuffing_inprocess.insert(0,[timeoftheorder, {'soft stuffing': settingdistibution_dict['reorder upto soft stuffing'] - instance.materialstate[2]['soft stuffing'], 'medium stuffing': settingdistibution_dict['reorder upto medium stuffing'] - instance.materialstate[2]['soft stuffing'], 'hard stuffing': settingdistibution_dict['reorder upto hard stuffing'] - instance.materialstate[2]['soft stuffing']}])
    instance.nexteventtimes['supply stuffing'] = timeoftheorder
    return instance

def event_supplyorder_stalen_stangen(instance, settingdistibution_dict):

    instance.materialstate[0]['stalen stangen'] += instance.supplyorders_stalenstangen_inprocess[0][1]
    instance.supplyorders_stalenstangen_inprocess.pop(0)
    instance.nexteventtimes['supply stalen stangen'] = instance.supplyorders_stalenstangen_inprocess[0][0]

    # update supply shortage measure of the orders in inventory
    for i in range(len(instance.inventories[0])):
        if len(instance.inventories[0][i][2]['reason inventory staal buigen']['supply shortage']) > 0 and len(instance.inventories[0][i][2]['reason inventory staal buigen']['supply shortage'][-1]) == 1:
            instance.inventories[0][i][2]['reason inventory staal buigen']['supply shortage'][-1].append(instance.tijd)

    #if those materials were needed for een order staal buigen om te beginnnen, zet deze in gang.
    while len(instance.inventories[0]) > 0 and instance.capacities[0] - instance.work_state[0][0] >= instance.inventories[0][0][1] and all(instance.materialstate[0][i] >= instance.inventories[0][0][2]['bill of materials']['staal buigen'][i] for i in instance.inventories[0][0][2]['bill of materials']['staal buigen'].keys()):
        newprocessing_order = instance.inventories[0].pop(0)

        for i in newprocessing_order[2]['bill of materials']['staal buigen'].keys():
            instance.materialstate[0][i] -= newprocessing_order[2]['bill of materials']['staal buigen'][i]

        instance.measures['workstate times'][0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
        instance.work_state[0][0] += newprocessing_order[1]
        instance.work_state[0][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_length_staal_buigen(settingdistibution_dict['mean staal buigen time'])
        finish_time_index = bisect(instance.orders_inprocess0, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal buigen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal buigen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal buigen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal buigen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal buigen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal buigen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess0.insert(finish_time_index, newprocessing_order)

    instance.nexteventtimes["staal buigen klaar"] = instance.orders_inprocess0[0][0]

    return instance

def event_supplyorder_koppeldraad(instance, settingdistibution_dict):

    instance.materialstate[1]['koppeldraad'] += instance.supplyorders_koppeldraad_inprocess[0][1]
    instance.supplyorders_koppeldraad_inprocess.pop(0)
    instance.nexteventtimes['supply koppeldraad'] = instance.supplyorders_koppeldraad_inprocess[0][0]

    # update supply shortage measure of the orders in inventory
    for i in range(len(instance.inventories[1])):
        if len(instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage']) > 0 and len(instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage'][-1]) == 1:
            instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage'][-1].append(instance.tijd)

    #if those materials were needed for een order staal buigen om te beginnnen, zet deze in gang.
    while len(instance.inventories[1]) > 0 and instance.capacities[1] - instance.work_state[1][0] >= instance.inventories[1][0][1] and all(instance.materialstate[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen'].keys()):
        newprocessing_order = instance.inventories[1].pop(0)

        for i in newprocessing_order[2]['bill of materials']['staal koppelen'].keys():
            instance.materialstate[1][i] -= newprocessing_order[2]['bill of materials']['staal koppelen'][i]

        instance.measures['workstate times'][1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
        instance.work_state[1][0] += newprocessing_order[1]
        instance.work_state[1][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_length_staal_koppelen(settingdistibution_dict['mean staal koppelen time'])
        finish_time_index = bisect(instance.orders_inprocess1, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal koppelen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal koppelen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal koppelen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal koppelen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal koppelen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal koppelen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess1.insert(finish_time_index, newprocessing_order)
    instance.nexteventtimes['staal koppelen klaar'] = instance.orders_inprocess1[0][0]

    return instance

def event_supplyorder_stuffing(instance, settingdistibution_dict):

    instance.materialstate[2]['soft stuffing'] += instance.supplyorders_stuffing_inprocess[0][1]['soft stuffing']
    instance.materialstate[2]['medium stuffing'] += instance.supplyorders_stuffing_inprocess[0][1]['medium stuffing']
    instance.materialstate[2]['hard stuffing'] += instance.supplyorders_stuffing_inprocess[0][1]['hard stuffing']
    instance.supplyorders_stuffing_inprocess.pop(0)
    instance.nexteventtimes['supply stuffing'] = instance.supplyorders_stuffing_inprocess[0][0]

    # update supply shortage measure of the orders in inventory
    for i in range(len(instance.inventories[2])):
        if len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage']) > 0 and len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage'][-1]) == 1:
            instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage'][-1].append(instance.tijd)

    #if those materials were needed for een order staal buigen om te beginnnen, zet deze in gang.
    while len(instance.inventories[2]) > 0 and instance.capacities[2] - instance.work_state[2][0] >= instance.inventories[2][0][1] and all(instance.materialstate[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken'].keys()):
        newprocessing_order = instance.inventories[2].pop(0)

        for i in newprocessing_order[2]['bill of materials']['omhulsel maken'].keys():
            instance.materialstate[2][i] -= newprocessing_order[2]['bill of materials']['omhulsel maken'][i]

        instance.measures['workstate times'][2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
        instance.work_state[2][0] += newprocessing_order[1]
        instance.work_state[2][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_length_omhulsel_plaatsen(settingdistibution_dict['mean omhulsel maken time'], settingdistibution_dict['stdev omhulsel maken time'])
        finish_time_index = bisect(instance.orders_inprocess2, [finish_time_this_order])

        newprocessing_order[2]['start tijd omhulsel maken'] = instance.tijd
        newprocessing_order[2]['eind tijd omhulsel maken'] = finish_time_this_order
        newprocessing_order[2]['tijd omhulsel maken'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory omhulsel maken'] = instance.tijd
        newprocessing_order[2]['tijd inventory omhulsel maken'] = instance.tijd - newprocessing_order[2]['start tijd inventory omhulsel maken']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess2.insert(finish_time_index, newprocessing_order)
    instance.nexteventtimes["omhulsel klaar"] = instance.orders_inprocess2[0][0]

    return instance

def event_staalbuigen_breakdown(instance, settingdistibution_dict):
    instance.nexteventtimes['staal buigen breakdown'] = math.inf
    instance.capacities[0] = 0
    instance.nexteventtimes['fix staal buigen breakdown'] = instance.tijd + get_length_fix_staalbuigen_breakdown(settingdistibution_dict['mean fix staal buigen breakdown'])

    for i in range(len(instance.inventories[0])):
        instance.inventories[0][i][2]['reason inventory staal buigen']['breakdown'].append([instance.tijd])

    # update measures
    instance.measures['breakdown periods']['staal buigen'].append([instance.tijd])

    return instance

def event_fixed_staalbuigen_breakdown(instance, settingdistibution_dict):
    instance.nexteventtimes['staal buigen breakdown'] = instance.tijd + get_length_next_staalbuigen_breakdown(settingdistibution_dict['mean staal buigen breakdown'])
    instance.capacities[0] = settingdistibution_dict['capacity staal buigen']
    instance.nexteventtimes['fix staal buigen breakdown'] = math.inf

    for i in range(len(instance.inventories[0])):
        instance.inventories[0][i][2]['reason inventory staal buigen']['breakdown'][-1].append(instance.tijd)

    #if this capacity was needed for orders to start, start them
    while len(instance.inventories[0]) > 0 and instance.capacities[0] - instance.work_state[0][0] >= instance.inventories[0][0][1] and all(instance.materialstate[0][i] >= instance.inventories[0][0][2]['bill of materials']['staal buigen'][i] for i in instance.inventories[0][0][2]['bill of materials']['staal buigen'].keys()):
        newprocessing_order = instance.inventories[0].pop(0)

        # update breakdown measure of the orders in inventory
        for i in newprocessing_order[2]['bill of materials']['staal buigen'].keys():
            instance.materialstate[0][i] -= newprocessing_order[2]['bill of materials']['staal buigen'][i]

        instance.measures['workstate times'][0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
        instance.work_state[0][0] += newprocessing_order[1]
        instance.work_state[0][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_length_staal_buigen(settingdistibution_dict['mean staal buigen time'])
        finish_time_index = bisect(instance.orders_inprocess0, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal buigen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal buigen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal buigen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal buigen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal buigen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal buigen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess0.insert(finish_time_index, newprocessing_order)

    instance.nexteventtimes["staal buigen klaar"] = instance.orders_inprocess0[0][0]

    # update measures
    instance.measures['breakdown periods']['staal buigen'][-1].append(instance.tijd)
    return instance

def event_staalkoppelen_breakdown(instance, settingdistibution_dict):
    instance.nexteventtimes['staal koppelen breakdown'] = math.inf
    instance.capacities[1] = 0
    instance.nexteventtimes['fix staal koppelen breakdown'] = instance.tijd + get_length_fix_staalkoppelen_breakdown(settingdistibution_dict['mean fix staal koppelen breakdown'])

    for i in range(len(instance.inventories[1])):
        instance.inventories[1][i][2]['reason inventory staal koppelen']['breakdown'].append([instance.tijd])

    # update measures
    instance.measures['breakdown periods']['staal koppelen'].append([instance.tijd])
    return instance

def event_fixed_staalkoppelen_breakdown(instance, settingdistibution_dict):
    instance.nexteventtimes['staal koppelen breakdown'] = instance.tijd + get_length_next_staalkoppelen_breakdown(settingdistibution_dict['mean staal koppelen breakdown'])
    instance.capacities[1] = settingdistibution_dict['capacity staal koppelen']
    instance.nexteventtimes['fix staal koppelen breakdown'] = math.inf

    # update breakdown measure of the orders in inventory
    for i in range(len(instance.inventories[1])):
        instance.inventories[1][i][2]['reason inventory staal koppelen']['breakdown'][-1].append(instance.tijd)

    #if this capacity was needed for orders to start, start them
    while len(instance.inventories[1]) > 0 and instance.capacities[1] - instance.work_state[1][0] >= instance.inventories[1][0][1] and all(instance.materialstate[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen'].keys()):
        newprocessing_order = instance.inventories[1].pop(0)

        for i in newprocessing_order[2]['bill of materials']['staal koppelen'].keys():
            instance.materialstate[1][i] -= newprocessing_order[2]['bill of materials']['staal koppelen'][i]

        instance.measures['workstate times'][1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
        instance.work_state[1][0] += newprocessing_order[1]
        instance.work_state[1][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_length_staal_koppelen(settingdistibution_dict['mean staal koppelen time'])
        finish_time_index = bisect(instance.orders_inprocess1, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal koppelen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal koppelen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal koppelen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal koppelen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal koppelen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal koppelen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess1.insert(finish_time_index, newprocessing_order)

    instance.nexteventtimes['staal koppelen klaar'] = instance.orders_inprocess1[0][0]

    # update measures
    instance.measures['breakdown periods']['staal koppelen'][-1].append(instance.tijd)
    return instance

def event_omhulselmaken_breakdown(instance, settingdistibution_dict):
    instance.nexteventtimes['omhulsel maken breakdown'] = math.inf
    instance.capacities[2] = 0
    instance.nexteventtimes['fix omhulsel maken breakdown'] = instance.tijd + get_length_fix_omhulselmaken_breakdown(settingdistibution_dict['mean fix omhulsel maken breakdown'])

    for i in range(len(instance.inventories[2])):
        instance.inventories[2][i][2]['reason inventory omhulsel maken']['breakdown'].append([instance.tijd])

    # update measures
    instance.measures['breakdown periods']['omhulsel maken'].append([instance.tijd])
    return instance

def event_fixed_omhulselmaken_breakdown(instance, settingdistibution_dict):
    instance.nexteventtimes['omhulsel maken breakdown'] = instance.tijd + get_length_next_omhulselmaken_breakdown(settingdistibution_dict['mean omhulsel maken breakdown'])
    instance.capacities[2] = settingdistibution_dict['capacity omhulsel maken']
    instance.nexteventtimes['fix omhulsel maken breakdown'] = math.inf

    # update breakdown measure of the orders in inventory
    for i in range(len(instance.inventories[2])):
        instance.inventories[2][i][2]['reason inventory omhulsel maken']['breakdown'][-1].append(instance.tijd)

    # if this capacity was needed for orders to start, start them
    while len(instance.inventories[2]) > 0 and instance.capacities[2] - instance.work_state[2][0] >= instance.inventories[2][0][1] and all(instance.materialstate[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken'].keys()):
        newprocessing_order = instance.inventories[2].pop(0)

        for i in newprocessing_order[2]['bill of materials']['omhulsel maken'].keys():
            instance.materialstate[2][i] -= newprocessing_order[2]['bill of materials']['omhulsel maken'][i]

        instance.measures['workstate times'][2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
        instance.work_state[2][0] += newprocessing_order[1]
        instance.work_state[2][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_length_omhulsel_plaatsen(settingdistibution_dict['mean omhulsel maken time'], settingdistibution_dict['stdev omhulsel maken time'])
        finish_time_index = bisect(instance.orders_inprocess2, [finish_time_this_order])

        newprocessing_order[2]['start tijd omhulsel maken'] = instance.tijd
        newprocessing_order[2]['eind tijd omhulsel maken'] = finish_time_this_order
        newprocessing_order[2]['tijd omhulsel maken'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory omhulsel maken'] = instance.tijd
        newprocessing_order[2]['tijd inventory omhulsel maken'] = instance.tijd - newprocessing_order[2]['start tijd inventory omhulsel maken']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess2.insert(finish_time_index, newprocessing_order)
    instance.nexteventtimes["omhulsel klaar"] = instance.orders_inprocess2[0][0]

    # update measures
    instance.measures['breakdown periods']['omhulsel maken'][-1].append(instance.tijd)
    return instance

def updatevariables(instance, event, next_t_event, settingdistibution_dict):

    #print('updating this move: ', event)
    instance.tijd = next_t_event

    if event == "new order":
        instance = event_neworder(instance, settingdistibution_dict)

    elif event == "staal buigen klaar":
        instance = event_staal_buigen_klaar(instance, settingdistibution_dict)

    elif event == "staal koppelen klaar":
        instance = event_staal_koppelen_klaar(instance, settingdistibution_dict)

    elif event == "omhulsel klaar":
        instance = event_omhulsel_klaar(instance, settingdistibution_dict)

    elif event == 'order new stalen stangen':
        event_order_new_stalen_stangen(instance, settingdistibution_dict)

    elif event == 'order new koppeldraad':
        event_order_new_koppeldraad(instance, settingdistibution_dict)

    elif event == 'order new stuffing':
        event_order_new_stuffing(instance, settingdistibution_dict)

    elif event == 'supply stalen stangen':
        instance = event_supplyorder_stalen_stangen(instance, settingdistibution_dict)

    elif event == 'supply koppeldraad':
        instance = event_supplyorder_koppeldraad(instance, settingdistibution_dict)

    elif event == 'supply stuffing':
        instance = event_supplyorder_stuffing(instance, settingdistibution_dict)

    elif event == 'staal buigen breakdown':
        instance = event_staalbuigen_breakdown(instance, settingdistibution_dict)

    elif event == 'staal koppelen breakdown':
        instance = event_staalkoppelen_breakdown(instance, settingdistibution_dict)

    elif event == 'omhulsel maken breakdown':
        instance = event_omhulselmaken_breakdown(instance, settingdistibution_dict)

    elif event == 'fix staal buigen breakdown':
        instance = event_fixed_staalbuigen_breakdown(instance, settingdistibution_dict)

    elif event == 'fix staal koppelen breakdown':
        instance = event_fixed_staalkoppelen_breakdown(instance, settingdistibution_dict)

    elif event == 'fix omhulsel maken breakdown':
        instance = event_fixed_omhulselmaken_breakdown(instance, settingdistibution_dict)

    return instance
