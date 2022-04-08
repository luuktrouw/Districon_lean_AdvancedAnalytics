import numpy as np
import random

'''
Thile file contains functions which return the length of a specific operation based on the distributions. 
Each function speaks mostly for itself
'''
###### ----------- BELOW are time/size functions

# this function returns the size of an incoming order
def get_order_size(Mean_ordersize, stdev_ordersize):
    size = round(np.random.normal(Mean_ordersize, stdev_ordersize), 0)
    #print('size of next order: ', size)
    return size

# this function returns the deadline of an incoming order
def get_order_deadline(Mean_order_deadline, stdev_order_deadline):
    time = round(np.random.normal(Mean_order_deadline, stdev_order_deadline), 0)
    return time

# this function returns the time until the next staal buigen breakdown
def get_length_next_staalbuigen_breakdown(Mean_schakel_staalbuigen_breakdown):
    time = round(np.random.exponential(Mean_schakel_staalbuigen_breakdown), 0)
    return time

# this function returns the time until the next staal koppelen breakdown
def get_length_next_staalkoppelen_breakdown(Mean_schakel_staalkoppelen_breakdown):
    time = round(np.random.exponential(Mean_schakel_staalkoppelen_breakdown), 0)
    return time

# this function returns the time until the next omhulsel maken breakdown
def get_length_next_omhulselmaken_breakdown(Mean_schakel_omhulselmaken_breakdown):
    time = round(np.random.exponential(Mean_schakel_omhulselmaken_breakdown), 0)
    return time

# this function returns the time until the staal buigen breakdown is fixed
def get_length_fix_staalbuigen_breakdown(Mean_fix_staalbuigen_breakdown):
    time = round(np.random.exponential(Mean_fix_staalbuigen_breakdown), 0)
    return time

# this function returns the time until the staal koppelen breakdown is fixed
def get_length_fix_staalkoppelen_breakdown(Mean_fix_staalkoppelen_breakdown):
    time = round(np.random.exponential(Mean_fix_staalkoppelen_breakdown), 0)
    return time

# this function returns the time until the omhulsel maken breakdown is fixed
def get_length_fix_omhulselmaken_breakdown(Mean_fix_omhulselmaken_breakdown):
    time = round(np.random.exponential(Mean_fix_omhulselmaken_breakdown), 0)
    return time

# this function returns the time the stalen stangen supplier takes to deliver its materials
def get_supplytime_stalen_stangen(Mean_supplytime_stalen_stangen, stdev_supplytime_stalen_stangen):
    time = round(np.random.normal(Mean_supplytime_stalen_stangen, stdev_supplytime_stalen_stangen), 0)
    #time = round(np.random.exponential(Mean_supplytime_stalen_stangen), 0)
    #print('size of next order: ', size)
    return time

# this function returns the time the koppeldraad supplier takes to deliver its materials
def get_supplytime_koppeldraad(Mean_supplytime_koppeldraad, stdev_supplytime_koppeldraad):
    time = round(np.random.normal(Mean_supplytime_koppeldraad, stdev_supplytime_koppeldraad), 0)
    #time = round(np.random.exponential(Mean_supplytime_koppeldraad), 0)
    #print('size of next order: ', size)
    return time

# this function returns the time the stuffing supplier takes to deliver its materials
def get_supplytime_stuffing(Mean_supplytime_stuffing, stdev_supplytime_stuffing):
    time = round(np.random.normal(Mean_supplytime_stuffing, stdev_supplytime_stuffing), 0)
    #time = round(np.random.exponential(Mean_supplytime_stuffing), 0)
    #print('size of next order: ', size)
    return time

# this function returns the actual delivered order quantify of a supplier
def get_delivered_order_quantity(orderquantity, stdev):
    quantity = round(np.random.normal(orderquantity, stdev), 0)
    return quantity

# this function returns the time until the next incoming order
def get_length_neworder(Mean_ordertime, stdev_ordersize):

    #tijd = round(np.random.exponential(Mean_ordertime, stdev_ordersize), 1)
    tijd = round(np.random.exponential(Mean_ordertime), 1)
    #print('time until next order: ', tijd)
    return tijd

# this function returns the time the new staal buigen process takes
def get_length_staal_buigen(Mean_process0time, stdev_process0time):
    tijd = round(np.random.normal(Mean_process0time, stdev_process0time), 1)

    #tijd = round(np.random.exponential(Mean_process0time), 1)
    #print('new time schakel 0: ', tijd)
    return tijd

# this function returns the time the new staal koppelen process takes
def get_length_staal_koppelen(Mean_process1time, stdev_process1time):
    tijd = round(np.random.normal(Mean_process1time, stdev_process1time), 1)
    #tijd = round(np.random.exponential(Mean_process1time), 1)
    #print('new time schakel 1: ', tijd)
    return tijd

# this function returns the time the new omhulsel maken process takes
def get_length_omhulsel_plaatsen(Mean_process2time, stdev_process2time):
    tijd = round(np.random.normal(Mean_process2time, stdev_process2time), 1)
    #print('new time schakel 2: ', tijd)
    return tijd

# this function returns the info of the newly received order
# note that this is hand specified, and thus needs to be changed if some input changes
def get_neworderinfo(Mean_ordersize, stdev_ordersize, highprioritychance):
    ordersize = get_order_size(Mean_ordersize, stdev_ordersize)
    if ordersize <= 0:
        ordersize = 1

    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    sign1 = random.choice(letters)
    sign2 = random.choice(letters)
    sign3 = random.choice(letters)
    sign4 = random.choice(letters)
    orderID = 'Order-' + sign1 + sign2 + sign3 + sign4

    priorityrandom = random.random()
    if priorityrandom <= highprioritychance:
        highpriority = True
    else: highpriority = False

    softnesstypes = ['hard', 'medium', 'soft']
    softness = random.choice(softnesstypes)

    sizetypes = ['eenpersoons', 'twijfelaar', 'queen size', 'king size']
    sizethisorder = random.choice(sizetypes)

    billofmaterials = {}
    billofmaterials['staal buigen'] = {'raw material':{}, 'subassembly':{}}
    billofmaterials['staal koppelen'] = {'raw material':{}, 'subassembly':{}}
    billofmaterials['omhulsel maken'] = {'raw material':{}, 'subassembly':{}}

    if sizethisorder == 'eenpersoons':
        billofmaterials['staal buigen']['raw material']['stalen stangen'] = 8 *ordersize
        billofmaterials['staal koppelen']['raw material']['koppeldraad'] = 4 *ordersize
        billofmaterials['staal koppelen']['subassembly']['gebogen stangen'] = 8 *ordersize
        billofmaterials['omhulsel maken']['subassembly']['gekoppeld eenpersoons'] = 1 * ordersize
        if softness == 'soft':
            billofmaterials['omhulsel maken']['raw material']['soft stuffing'] = 1 *ordersize
        elif softness == 'medium':
            billofmaterials['omhulsel maken']['raw material']['medium stuffing'] = 1 *ordersize
        elif softness == 'hard':
            billofmaterials['omhulsel maken']['raw material']['hard stuffing'] = 1 *ordersize

    elif sizethisorder == 'twijfelaar':
        billofmaterials['staal buigen']['raw material']['stalen stangen'] = 10 *ordersize
        billofmaterials['staal koppelen']['raw material']['koppeldraad'] = 4 *ordersize
        billofmaterials['staal koppelen']['subassembly']['gebogen stangen'] = 10 *ordersize
        billofmaterials['omhulsel maken']['subassembly']['gekoppeld twijfelaar'] = 1 * ordersize
        if softness == 'soft':
            billofmaterials['omhulsel maken']['raw material']['soft stuffing'] = 1 *ordersize
        elif softness == 'medium':
            billofmaterials['omhulsel maken']['raw material']['medium stuffing'] = 1 *ordersize
        elif softness == 'hard':
            billofmaterials['omhulsel maken']['raw material']['hard stuffing'] = 1 *ordersize

    elif sizethisorder == 'queen size':
        billofmaterials['staal buigen']['raw material']['stalen stangen'] = 14 *ordersize
        billofmaterials['staal koppelen']['raw material']['koppeldraad'] = 6 *ordersize
        billofmaterials['staal koppelen']['subassembly']['gebogen stangen'] = 14 *ordersize
        billofmaterials['omhulsel maken']['subassembly']['gekoppeld queensize'] = 1 * ordersize
        if softness == 'soft':
            billofmaterials['omhulsel maken']['raw material']['soft stuffing'] = 1 *ordersize
        elif softness == 'medium':
            billofmaterials['omhulsel maken']['raw material']['medium stuffing'] = 1 *ordersize
        elif softness == 'hard':
            billofmaterials['omhulsel maken']['raw material']['hard stuffing'] = 1 *ordersize

    elif sizethisorder == 'king size':
        billofmaterials['staal buigen']['raw material']['stalen stangen'] = 16 *ordersize
        billofmaterials['staal koppelen']['raw material']['koppeldraad'] = 6 *ordersize
        billofmaterials['staal koppelen']['subassembly']['gebogen stangen'] = 16 *ordersize
        billofmaterials['omhulsel maken']['subassembly']['gekoppeld kingsize'] = 1 * ordersize
        if softness == 'soft':
            billofmaterials['omhulsel maken']['raw material']['soft stuffing'] = 1 *ordersize
        elif softness == 'medium':
            billofmaterials['omhulsel maken']['raw material']['medium stuffing'] = 1 *ordersize
        elif softness == 'hard':
            billofmaterials['omhulsel maken']['raw material']['hard stuffing'] = 1 *ordersize

    return orderID, ordersize, softness, sizethisorder, billofmaterials ,highpriority


