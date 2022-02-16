import numpy as np
import math
from bisect import bisect
import random

# distribution orders
Mean_ordertime = 110 # 10
Mean_ordersize = 4
stdev_ordertime = 10 # 2
stdev_ordersize = 1

# stalen stangen supply
Mean_supplytime_stalen_stangen = 2500
stdev_supplytime_stalen_stangen = 2
reorderpoint_stalenstangen = 20
reorder_upto_point_stalenstangen = 10000

# distributions processes
Mean_process0time = 100
Mean_process1time = 120
Mean_process2time = 100
stdev_process0time = 10
stdev_process1time = 0
stdev_process2time = 10

def get_order_size():
    size = round(np.random.normal(Mean_ordersize, stdev_ordersize), 0)
    #print('size of next order: ', size)
    return size

def get_supplytime_stalen_stangen():
    time = round(np.random.normal(Mean_supplytime_stalen_stangen, stdev_supplytime_stalen_stangen), 0)
    #print('size of next order: ', size)
    return time

def get_length_neworder():

    #tijd = round(np.random.exponential(Mean_ordertime), 1)
    tijd = round(np.random.normal(Mean_ordertime, stdev_ordertime), 1)
    #print('time until next order: ', tijd)
    return tijd

def get_duration_staal_buigen():
    tijd = round(np.random.normal(Mean_process0time, stdev_process0time), 1)
    #print('new time schakel 0: ', tijd)
    return tijd

def get_length_staal_koppelen():
    tijd = round(np.random.normal(Mean_process1time, stdev_process1time), 1)
    #print('new time schakel 1: ', tijd)
    return tijd

def get_length_omhulsel_plaatsen():
    tijd = round(np.random.normal(Mean_process2time, stdev_process2time), 1)
    #print('new time schakel 2: ', tijd)
    return tijd

def get_neworderinfo():
    ordersize = get_order_size()
    if ordersize <= 0:
        print('gaat dit fout?')
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

    if sizethisorder == 'eenpersoons':
        billofmaterials['stalen stangen'] = 8
        billofmaterials['koppeldraad'] = 4
        if softness == 'soft':
            billofmaterials['soft stuffing'] = 1
        elif softness == 'medium':
            billofmaterials['medium stuffing'] = 1
        elif softness == 'hard':
            billofmaterials['hard stuffing'] = 1

    elif sizethisorder == 'twijfelaar':
        billofmaterials['stalen stangen'] = 10
        billofmaterials['koppeldraad'] = 4
        if softness == 'soft':
            billofmaterials['soft stuffing'] = 1
        elif softness == 'medium':
            billofmaterials['medium stuffing'] = 1
        elif softness == 'hard':
            billofmaterials['hard stuffing'] = 1

    elif sizethisorder == 'queen size':
        billofmaterials['stalen stangen'] = 14
        billofmaterials['koppeldraad'] = 6
        if softness == 'soft':
            billofmaterials['soft stuffing'] = 1
        elif softness == 'medium':
            billofmaterials['medium stuffing'] = 1
        elif softness == 'hard':
            billofmaterials['hard stuffing'] = 1

    elif sizethisorder == 'king size':
        billofmaterials['stalen stangen'] = 16
        billofmaterials['koppeldraad'] = 6
        if softness == 'soft':
            billofmaterials['soft stuffing'] = 1
        elif softness == 'medium':
            billofmaterials['medium stuffing'] = 1
        elif softness == 'hard':
            billofmaterials['hard stuffing'] = 1

    return orderID, ordersize, softness, sizethisorder, billofmaterials

def eventneworder(instance):

    orderID, ordersize, softness, sizethisorder, billofmaterials = get_neworderinfo()

    orderdict = {'orderID': orderID, 'softnesstype': softness, 'size': sizethisorder, 'bill of materials': billofmaterials, 'time received': instance.tijd}

    instance.t_neworder = instance.tijd + get_length_neworder()

    if instance.capacities[0] - instance.work_state[0][0] >= ordersize and len(instance.inventories[0]) == 0 and instance.materialstate[0]['stalen stangen'] >= orderdict['bill of materials']['stalen stangen']:
        instance.materialstate[0]['stalen stangen'] -= orderdict['bill of materials']['stalen stangen']
        # if materials to low, order up to a certain level.
        if instance.materialstate[0]['stalen stangen'] <= reorderpoint_stalenstangen and len(instance.supplyorders_stalenstangen_inprocess) == 1:
            instance.supplyorders_stalenstangen_inprocess.insert(0,[instance.tijd + get_supplytime_stalen_stangen(), reorder_upto_point_stalenstangen -instance.materialstate[0]['stalen stangen']])

        instance.work_state_times[0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
        instance.work_state[0][0] += ordersize
        instance.work_state[0][1] = instance.tijd
        finish_time_this_order =  instance.tijd + get_duration_staal_buigen()
        finish_time_index = bisect(instance.orders_inprocess0, [finish_time_this_order])

        orderdict['start tijd staal buigen'] = instance.tijd
        orderdict['eind tijd staal buigen'] = finish_time_this_order
        orderdict['tijd staal buigen'] = finish_time_this_order - instance.tijd
        orderdict['start tijd inventory staal buigen'] = instance.tijd
        orderdict['eind tijd inventory staal buigen'] = instance.tijd
        orderdict['tijd inventory staal buigen']  = 0

        instance.orders_inprocess0.insert(finish_time_index, [finish_time_this_order, ordersize, orderdict])

        # instance.t1klaar = instance.tijd + get_duration_staal_buigen()

    else:
        orderdict['start tijd inventory staal buigen'] = instance.tijd
        instance.inventories[0].append([math.inf, ordersize, orderdict])

    return instance

def staal_buigen_klaar(instance):
    # update the machine itself
    processed_order = instance.orders_inprocess0.pop(0)
    instance.work_state_times[0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
    instance.work_state[0][0] -= processed_order[1]
    instance.work_state[0][1] = instance.tijd

    # what goes in the machine:
    while len(instance.inventories[0]) > 0 and instance.capacities[0] - instance.work_state[0][0] >= instance.inventories[0][0][1] and instance.materialstate[0]['stalen stangen'] >= instance.inventories[0][0][2]['bill of materials']['stalen stangen']:
        newprocessing_order = instance.inventories[0].pop(0)

        instance.materialstate[0]['stalen stangen'] -= newprocessing_order[2]['bill of materials']['stalen stangen']
        # if materials to low, order up to a certain level.
        if instance.materialstate[0]['stalen stangen'] <= reorderpoint_stalenstangen and len(instance.supplyorders_stalenstangen_inprocess) == 1:
            instance.supplyorders_stalenstangen_inprocess.insert(0,[instance.tijd + get_supplytime_stalen_stangen(), reorder_upto_point_stalenstangen -instance.materialstate[0]['stalen stangen']])

        instance.work_state_times[0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
        instance.work_state[0][0] += newprocessing_order[1]
        instance.work_state[0][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_duration_staal_buigen()
        finish_time_index = bisect(instance.orders_inprocess0, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal buigen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal buigen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal buigen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal buigen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal buigen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal buigen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess0.insert(finish_time_index, newprocessing_order)

    # what goes out of the machine:
    if instance.capacities[1] - instance.work_state[1][0] >= processed_order[1] and len(instance.inventories[1]) == 0 and instance.materialstate[1]['koppeldraad'] >= processed_order[2]['bill of materials']['koppeldraad']:
        instance.work_state_times[1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
        instance.work_state[1][0] += processed_order[1]
        instance.work_state[1][1] = instance.tijd
        instance.materialstate[1]['koppeldraad'] -= processed_order[2]['bill of materials']['koppeldraad']
        finish_time_this_order = instance.tijd + get_length_staal_koppelen()
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
        instance.inventories[1].append(processed_order)

    return instance

def staal_koppelen_klaar(instance):
    # update the machine itself
    processed_order = instance.orders_inprocess1.pop(0)
    instance.work_state_times[1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
    instance.work_state[1][0] -= processed_order[1]
    instance.work_state[1][1] = instance.tijd

    # what goes in the machine:
    while len(instance.inventories[1]) > 0 and instance.capacities[1] - instance.work_state[1][0] >= instance.inventories[1][0][1] and instance.materialstate[1]['koppeldraad'] >= instance.inventories[1][0][2]['bill of materials']['koppeldraad']:
        newprocessing_order = instance.inventories[1].pop(0)

        instance.work_state_times[1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
        instance.work_state[1][0] += newprocessing_order[1]
        instance.work_state[1][1] = instance.tijd
        instance.materialstate[1]['koppeldraad'] -= newprocessing_order[2]['bill of materials']['koppeldraad']
        finish_time_this_order =  instance.tijd + get_length_staal_koppelen()
        finish_time_index = bisect(instance.orders_inprocess1, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal koppelen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal koppelen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal koppelen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal koppelen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal koppelen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal koppelen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess1.insert(finish_time_index, newprocessing_order)

    # what goes out of the machine:
    if instance.capacities[2] - instance.work_state[2][0] >= processed_order[1] and len(instance.inventories[2]) == 0:
        instance.work_state_times[2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
        instance.work_state[2][0] += processed_order[1]
        instance.work_state[2][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_length_omhulsel_plaatsen()
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
        instance.inventories[2].append(processed_order)

    return instance

def omhulsel_klaar(instance):
    # update the machine itself
    processed_order = instance.orders_inprocess2.pop(0)
    instance.work_state_times[2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
    instance.work_state[2][0] -= processed_order[1]
    instance.work_state[2][1] = instance.tijd

    processed_order[2]['finish time'] = instance.tijd
    processed_order[2]['total process time'] =  processed_order[2]['finish time'] - processed_order[2]['time received']
    instance.finishedorders.append(processed_order[2])

    # update amount produced
    #print('one batch produced of size:', processed_order[1])
    instance.amountproduced += processed_order[1]

    # what goes in the machine:
    while len(instance.inventories[2]) > 0 and instance.capacities[2] - instance.work_state[2][0] >= instance.inventories[2][0][1]:
        newprocessing_order = instance.inventories[2].pop(0)

        instance.work_state_times[2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
        instance.work_state[2][0] += newprocessing_order[1]
        instance.work_state[2][1] = instance.tijd
        finish_time_this_order =  instance.tijd + get_length_omhulsel_plaatsen()
        finish_time_index = bisect(instance.orders_inprocess2, [finish_time_this_order])

        newprocessing_order[2]['start tijd omhulsel maken'] = instance.tijd
        newprocessing_order[2]['eind tijd omhulsel maken'] = finish_time_this_order
        newprocessing_order[2]['tijd omhulsel maken'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory omhulsel maken'] = instance.tijd
        newprocessing_order[2]['tijd inventory omhulsel maken'] = instance.tijd - newprocessing_order[2]['start tijd inventory omhulsel maken']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess2.insert(finish_time_index, newprocessing_order)

    return instance

def supplyorder_stalen_stangen(instance):

    instance.materialstate[0]['stalen stangen'] += instance.supplyorders_stalenstangen_inprocess[0][1]
    instance.supplyorders_stalenstangen_inprocess.pop(0)

    #if those materials were needed for een order staal buigen om te beginnnen, zet deze in gang.
    while len(instance.inventories[0]) > 0 and instance.capacities[0] - instance.work_state[0][0] >= instance.inventories[0][0][1] and instance.materialstate[0]['stalen stangen'] >= instance.inventories[0][0][2]['bill of materials']['stalen stangen']:
        newprocessing_order = instance.inventories[0].pop(0)

        instance.materialstate[0]['stalen stangen'] -= newprocessing_order[2]['bill of materials']['stalen stangen']
        instance.work_state_times[0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
        instance.work_state[0][0] += newprocessing_order[1]
        instance.work_state[0][1] = instance.tijd
        finish_time_this_order = instance.tijd + get_duration_staal_buigen()
        finish_time_index = bisect(instance.orders_inprocess0, [finish_time_this_order])

        newprocessing_order[2]['start tijd staal buigen'] = instance.tijd
        newprocessing_order[2]['eind tijd staal buigen'] = finish_time_this_order
        newprocessing_order[2]['tijd staal buigen'] = finish_time_this_order - instance.tijd
        newprocessing_order[2]['eind tijd inventory staal buigen'] = instance.tijd
        newprocessing_order[2]['tijd inventory staal buigen'] = instance.tijd - newprocessing_order[2]['start tijd inventory staal buigen']

        newprocessing_order[0] = finish_time_this_order

        instance.orders_inprocess0.insert(finish_time_index, newprocessing_order)

    return instance

def updatevariables(instance, event, next_t_event):

    #print('updating this move: ', event)
    instance.tijd = next_t_event

    if event == "new order":
        instance = eventneworder(instance)

    elif event == "staal buigen klaar":
        instance = staal_buigen_klaar(instance)

    elif event == "staal koppelen klaar":
        instance = staal_koppelen_klaar(instance)

    elif event == "omhulsel klaar":
        instance = omhulsel_klaar(instance)

    elif event == 'supply stalen stangen':
        instance = supplyorder_stalen_stangen(instance)

    return instance
