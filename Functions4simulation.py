import numpy as np
import math
from bisect import bisect
import random

# distribution orders
Mean_ordertime = 10 # 10
Mean_ordersize = 4
stdev_ordertime = 2 # 2
stdev_ordersize = 1

# distributions processes
Mean_process0time = 20
Mean_process1time = 20
Mean_process2time = 20
stdev_process0time = 4
stdev_process1time = 4
stdev_process2time = 4

orderID = 'Order-' + str(1)

def get_order_size():
    size = round(np.random.normal(Mean_ordersize, stdev_ordersize), 0)
    #print('size of next order: ', size)
    return size

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

def eventneworder(instance):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    sign1 = random.choice(letters)
    sign2 = random.choice(letters)
    sign3 = random.choice(letters)
    sign4 = random.choice(letters)
    orderID = 'Order-' + sign1 + sign2 + sign3 + sign4

    ordersize = get_order_size()
    #if ordersize <= 0:
        #print('gaat dit fout?')

    instance.t_neworder = instance.tijd + get_length_neworder()

    if instance.capacities[0] - instance.work_state[0] >= ordersize and len(instance.inventories[0]) == 0:
        instance.work_state[0] += ordersize
        process_time_this_order =  get_duration_staal_buigen()
        finish_time_index = bisect(instance.orders_inprocess0, [instance.tijd + process_time_this_order])

        instance.orders_inprocess0.insert(finish_time_index, [instance.tijd + process_time_this_order, ordersize, orderID])

        # instance.t1klaar = instance.tijd + get_duration_staal_buigen()

    else:
        instance.inventories[0].append([math.inf, ordersize, orderID])

    return instance

def staal_buigen_klaar(instance):
    # update the machine itself
    processed_order = instance.orders_inprocess0.pop(0)
    instance.work_state[0] -= processed_order[1]

    # what goes in the machine:
    while len(instance.inventories[0]) > 0 and instance.capacities[0] - instance.work_state[0] >= instance.inventories[0][0][1]:
        newprocessing_order = instance.inventories[0].pop(0)

        instance.work_state[0] += newprocessing_order[1]
        process_time_this_order =  get_duration_staal_buigen()
        finish_time_index = bisect(instance.orders_inprocess0, [instance.tijd + process_time_this_order])

        newprocessing_order[0] = instance.tijd + process_time_this_order

        instance.orders_inprocess0.insert(finish_time_index, newprocessing_order)

    # what goes out of the machine:
    if instance.capacities[1] - instance.work_state[1] >= processed_order[1] and len(instance.inventories[1]) == 0:
        instance.work_state[1] += processed_order[1]
        process_time_this_order = get_length_staal_koppelen()
        finish_time_index = bisect(instance.orders_inprocess1, [instance.tijd + process_time_this_order])

        processed_order[0] = instance.tijd + process_time_this_order

        instance.orders_inprocess1.insert(finish_time_index, processed_order)
    else:
        processed_order[0] = math.inf
        instance.inventories[1].append(processed_order)

    return instance


def staal_koppelen_klaar(instance):
    # update the machine itself
    processed_order = instance.orders_inprocess1.pop(0)
    instance.work_state[1] -= processed_order[1]

    # what goes in the machine:
    while len(instance.inventories[1]) > 0 and instance.capacities[1] - instance.work_state[1] >= instance.inventories[1][0][1]:
        newprocessing_order = instance.inventories[1].pop(0)

        instance.work_state[1] += newprocessing_order[1]
        process_time_this_order =  get_length_staal_koppelen()
        finish_time_index = bisect(instance.orders_inprocess1, [instance.tijd + process_time_this_order])

        newprocessing_order[0] = instance.tijd + process_time_this_order

        instance.orders_inprocess1.insert(finish_time_index, newprocessing_order)

    # what goes out of the machine:
    if instance.capacities[2] - instance.work_state[2] >= processed_order[1] and len(instance.inventories[2]) == 0:
        instance.work_state[2] += processed_order[1]
        process_time_this_order = get_length_omhulsel_plaatsen()
        finish_time_index = bisect(instance.orders_inprocess2, [instance.tijd + process_time_this_order])

        processed_order[0] = instance.tijd + process_time_this_order

        instance.orders_inprocess2.insert(finish_time_index, processed_order)
    else:
        processed_order[0] = math.inf
        instance.inventories[2].append(processed_order)

    return instance

def omhulsel_klaar(instance):
    # update the machine itself
    processed_order = instance.orders_inprocess2.pop(0)
    instance.work_state[2] -= processed_order[1]

    # update amount produced
    print('one batch produced of size:', processed_order[1])
    instance.amountproduced += processed_order[1]

    # what goes in the machine:
    while len(instance.inventories[2]) > 0 and instance.capacities[2] - instance.work_state[2] >= instance.inventories[2][0][1]:
        newprocessing_order = instance.inventories[2].pop(0)

        instance.work_state[2] += newprocessing_order[1]
        process_time_this_order =  get_length_omhulsel_plaatsen()
        finish_time_index = bisect(instance.orders_inprocess2, [instance.tijd + process_time_this_order])

        newprocessing_order[0] = instance.tijd + process_time_this_order

        instance.orders_inprocess2.insert(finish_time_index, newprocessing_order)

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

    return instance
