import numpy as np
import math
from bisect import bisect

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

orderID = 'Order-' + 1

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
    ordersize = get_order_size()
    #if ordersize <= 0:
        #print('gaat dit fout?')

    instance.t_neworder = instance.tijd + get_length_neworder()


    if instance.capacities[0] - instance.work_state[0] >= ordersize and len(instance.inventories[0]) == 0:
        instance.work_state[0] += ordersize
        process_time_this_order =  get_duration_staal_buigen()
        finish_time_index = bisect(instance.orders_inprocess0[0], instance.tijd + process_time_this_order)

        instance.orders_inprocess0[0].insert(finish_time_index, instance.tijd + process_time_this_order) # insert the finish time of the order in the right spot
        instance.orders_inprocess0[1].insert(finish_time_index, ordersize) # insert the size of the order in the right spot

        # instance.t1klaar = instance.tijd + get_duration_staal_buigen()

    else:
        instance.inventories[0].append(ordersize)

    return instance

def staal_buigen_klaar(instance):
    # update the machine itself
    instance.orders_inprocess0[0].pop(0)
    finished_ordersize = instance.orders_inprocess0[1].pop(0)
    instance.work_state[0] -= finished_ordersize

    # what goes in the machine:
    while len(instance.inventories[0]) > 0 and instance.capacities[0] - instance.work_state[0] >= instance.inventories[0][0]:
        instance.work_state[0] += instance.inventories[0][0]
        process_time_this_order =  get_duration_staal_buigen()
        finish_time_index = bisect(instance.orders_inprocess0[0], instance.tijd + process_time_this_order)

        instance.orders_inprocess0[0].insert(finish_time_index, instance.tijd + process_time_this_order) # insert the finish time of the order in the right spot
        instance.orders_inprocess0[1].insert(finish_time_index, instance.inventories[0][0]) # insert the size of the order in the right spot

        instance.inventories[0].pop(0)

    # what goes out of the machine:
    if instance.capacities[1] - instance.work_state[1] >= finished_ordersize and len(instance.inventories[1]) == 0:
        instance.work_state[1] += finished_ordersize
        process_time_this_order = get_length_staal_koppelen()
        finish_time_index = bisect(instance.orders_inprocess1[0], instance.tijd + process_time_this_order)

        instance.orders_inprocess1[0].insert(finish_time_index, instance.tijd + process_time_this_order) # insert the finish time of the order in the right spot
        instance.orders_inprocess1[1].insert(finish_time_index, finished_ordersize)
    else:
        instance.inventories[1].append(finished_ordersize)

    return instance


def staal_koppelen_klaar(instance):
    # update the machine itself
    instance.orders_inprocess1[0].pop(0)
    finished_ordersize = instance.orders_inprocess1[1].pop(0)
    instance.work_state[1] -= finished_ordersize

    # what goes in the machine:
    while len(instance.inventories[1]) > 0 and instance.capacities[1] - instance.work_state[1] >= instance.inventories[1][0]:
        instance.work_state[1] += instance.inventories[1][0]
        process_time_this_order =  get_length_staal_koppelen()
        finish_time_index = bisect(instance.orders_inprocess1[0], instance.tijd + process_time_this_order)

        instance.orders_inprocess1[0].insert(finish_time_index, instance.tijd + process_time_this_order) # insert the finish time of the order in the right spot
        instance.orders_inprocess1[1].insert(finish_time_index, instance.inventories[1][0]) # insert the size of the order in the right spot

        instance.inventories[1].pop(0)

    # what goes out of the machine:
    if instance.capacities[2] - instance.work_state[2] >= finished_ordersize and len(instance.inventories[2]) == 0:
        instance.work_state[2] += finished_ordersize
        process_time_this_order = get_length_omhulsel_plaatsen()
        finish_time_index = bisect(instance.orders_inprocess2[0], instance.tijd + process_time_this_order)

        instance.orders_inprocess2[0].insert(finish_time_index, instance.tijd + process_time_this_order) # insert the finish time of the order in the right spot
        instance.orders_inprocess2[1].insert(finish_time_index, finished_ordersize)
    else:
        instance.inventories[2].append(finished_ordersize)

    return instance

def omhulsel_klaar(instance):
    # update the machine itself
    instance.orders_inprocess2[0].pop(0)
    finished_ordersize = instance.orders_inprocess2[1].pop(0)
    instance.work_state[2] -= finished_ordersize

    # update amount produced
    #print('one batch produced of size:', finished_ordersize)
    instance.amountproduced += finished_ordersize

    # what goes in the machine:
    while len(instance.inventories[2]) > 0 and instance.capacities[2] - instance.work_state[2] >= instance.inventories[2][0]:
        instance.work_state[2] += instance.inventories[2][0]
        process_time_this_order =  get_length_omhulsel_plaatsen()
        finish_time_index = bisect(instance.orders_inprocess2[0], instance.tijd + process_time_this_order)

        instance.orders_inprocess2[0].insert(finish_time_index, instance.tijd + process_time_this_order) # insert the finish time of the order in the right spot
        instance.orders_inprocess2[1].insert(finish_time_index, instance.inventories[2][0]) # insert the size of the order in the right spot

        instance.inventories[2].pop(0)

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
