import math
from Simulationfiles import Functions_get_info
from Simulationfiles import Functions_start_process_steps

######
'''
This file contains all possible events, and the needed functions to call if a certain event happens.
If for any reason the actions at one event change, they only need to be adjusted in that certain event function
'''
# ----------- BELOW are event functions

# event if a new order comes in
def event_neworder(instance, settingdistibution_dict):
    # first load in the details of the new order by calling the get_neworderinfo function and store the info in the orderdict
    orderID, ordersize, softness, sizethisorder, billofmaterials, highpriority = Functions_get_info.get_neworderinfo(settingdistibution_dict['order size mean'], settingdistibution_dict['order size stdev'], settingdistibution_dict['high priority chance'])
    totalordersize = ordersize

    # it is possible to create all seperate orders of size 1, if you want them to be able to split up.
    # In that case perform the loop below
    #ordersize = 1
    #for i in range(int(totalordersize)):

    orderdict = {'orderID': orderID,
                 #'portion':(i+1)/int(totalordersize),
                 'time received': instance.tijd,
                 'deadline order': instance.tijd + Functions_get_info.get_order_deadline(settingdistibution_dict['mean deadline order'], settingdistibution_dict['stdev deadline order']),
                 'softnesstype': softness, 'bedsize': sizethisorder, 'high priority': highpriority,
                 'bill of materials': billofmaterials,
                 'size of the order': totalordersize,
                 'reason inventory staal buigen': {'supply shortage':[], 'breakdown':[], 'waiting on other orders':[]},
                 'reason inventory staal koppelen': {'supply shortage':[], 'breakdown':[], 'waiting on other orders':[]},
                 'reason inventory omhulsel maken': {'supply shortage':[], 'breakdown':[], 'waiting on other orders':[]}}

    # input the new order in the inventory of the all processes and try starting the process.
    # if no high priority, add it at the end of the line, otherwise at the end of the high priorities
    if orderdict['high priority'] == False or len(instance.inventories[2]) == 0:
        instance.inventories[2].append([math.inf, ordersize, orderdict])
    else:
        for i in range(len(instance.inventories[2])):
            if instance.inventories[2][i][2]['high priority'] == False:
                instance.inventories[2].insert(i, [math.inf, ordersize, orderdict])
                # if it is the first in queue, dan kan het zijn dat deze kan met supply, waardoor er dus geen supply  shortage is voor even
                # dit zou resulteren in eventjes 0 seconde geen shortage supply voor die order, als je dat wil oplossen moet dat hier
                # if i == 0:

                break
            instance.inventories[2].append([math.inf, ordersize, orderdict])
    orderdict['start tijd inventory omhulsel maken'] = instance.tijd

    if orderdict['high priority'] == False or len(instance.inventories[1]) == 0:
        instance.inventories[1].append([math.inf, ordersize, orderdict])
    else:
        for i in range(len(instance.inventories[1])):
            if instance.inventories[1][i][2]['high priority'] == False:
                instance.inventories[1].insert(i, [math.inf, ordersize, orderdict])

                # if it is the first in queue, dan kan het zijn dat deze kan met supply, waardoor er dus geen supply  shortage is voor even
                # dit zou resulteren in eventjes 0 seconde geen shortage supply voor die order, als je dat wil oplossen moet dat hier

                break
            instance.inventories[1].append([math.inf, ordersize, orderdict])
    orderdict['start tijd inventory staal koppelen'] = instance.tijd

    if orderdict['high priority'] == False or len(instance.inventories[0]) == 0:
        instance.inventories[0].append([math.inf, ordersize, orderdict])
    else:
        for i in range(len(instance.inventories[0])):
            if instance.inventories[0][i][2]['high priority'] == False:
                instance.inventories[0].insert(i, [math.inf, ordersize, orderdict])
                # if it is the first in queue, dan kan het zijn dat deze kan met supply, waardoor er dus geen supply  shortage is voor even
                # dit zou resulteren in eventjes 0 seconde geen shortage supply voor die order, als je dat wil oplossen moet dat hier

                break
            instance.inventories[0].append([math.inf, ordersize, orderdict])
    orderdict['start tijd inventory staal buigen'] = instance.tijd

    ###### loop until here if seperate orders

    instance.nexteventtimes['new order'] = instance.tijd + Functions_get_info.get_length_neworder(settingdistibution_dict['order time mean'], settingdistibution_dict['order time stdev'])

    #  try starting each process with the new orders in inventory
    #  if they are busy nothing will happen, otherwise the order will start

    instance = Functions_start_process_steps.start_process_omhulsel_maken(instance, settingdistibution_dict)

    instance = Functions_start_process_steps.start_process_staal_koppelen(instance, settingdistibution_dict)

    instance = Functions_start_process_steps.start_process_staal_buigen(instance, settingdistibution_dict)

    # updat next event time for staal buigen and for the other processes, these could have changed if some orders started processing
    instance.nexteventtimes["staal buigen klaar"] = instance.orders_inprocess0[0][0]
    instance.nexteventtimes["staal koppelen klaar"] = instance.orders_inprocess1[0][0]
    instance.nexteventtimes["omhulsel klaar"] = instance.orders_inprocess2[0][0]

    return instance

# event if a staal buigen order in process is finished
def event_staal_buigen_klaar(instance, settingdistibution_dict):
    # update the machine itself (its workstate and the measures)
    processed_order = instance.orders_inprocess0.pop(0)
    instance.measures['workstate times'][0][instance.work_state[0][0]] += instance.tijd - instance.work_state[0][1]
    instance.work_state[0][0] -= processed_order[1]
    instance.work_state[0][1] = instance.tijd
    #update subassembly stock which is produced
    for i in processed_order[2]['bill of materials']['staal koppelen']['subassembly'].keys():
        # for the measures, add before and after the updating to have the complete lines
        instance.measures['stock levels']['subassemblies'][i].append([instance.stockstate_subassemblies[1][i], instance.tijd])
        instance.stockstate_subassemblies[1][i] += processed_order[2]['bill of materials']['staal koppelen']['subassembly'][i]
        instance.measures['stock levels']['subassemblies'][i].append([instance.stockstate_subassemblies[1][i], instance.tijd])

    # check whether this solves sub assembly shortage in stock, if there was one (first part of if)
    if len(instance.measures['supply shortage periods']['staal koppelen']) > 0 and len(instance.measures['supply shortage periods']['staal koppelen'][-1]) == 1 \
            and all(instance.materialstate[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen']['raw material'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen']['raw material'].keys()) \
            and all(instance.stockstate_subassemblies[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen']['subassembly'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen']['subassembly'].keys()):
        for i in range(len(instance.inventories[1])):
            if len(instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage']) > 0 and len(instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage'][-1]) == 1:
                instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage'][-1].append(instance.tijd)
        # update the supply shortage measure, als er hiervoor supply shortage was
        instance.measures['supply shortage periods']['staal koppelen'][-1].append(instance.tijd)

    # what goes in the machine, try starting from inventory:
    instance = Functions_start_process_steps.start_process_staal_buigen(instance, settingdistibution_dict)

    # what goes out of the machine (might needed the subassembly to start), try starting from inventory
    instance = Functions_start_process_steps.start_process_staal_koppelen(instance, settingdistibution_dict)

    instance.nexteventtimes["staal buigen klaar"] = instance.orders_inprocess0[0][0]
    instance.nexteventtimes['staal koppelen klaar'] = instance.orders_inprocess1[0][0]

    return instance

# event if a staal koppelen order in process is finished
def event_staal_koppelen_klaar(instance, settingdistibution_dict):
    # update the machine itself (its workstate and the measures)
    processed_order = instance.orders_inprocess1.pop(0)
    instance.measures['workstate times'][1][instance.work_state[1][0]] += instance.tijd - instance.work_state[1][1]
    instance.work_state[1][0] -= processed_order[1]
    instance.work_state[1][1] = instance.tijd
    #update subassembly stock which is produced
    for i in processed_order[2]['bill of materials']['omhulsel maken']['subassembly'].keys():
        # for the measures, add before and after the updating to have the complete lines
        instance.measures['stock levels']['subassemblies'][i].append([instance.stockstate_subassemblies[2][i], instance.tijd])
        instance.stockstate_subassemblies[2][i] += processed_order[2]['bill of materials']['omhulsel maken']['subassembly'][i]
        instance.measures['stock levels']['subassemblies'][i].append([instance.stockstate_subassemblies[2][i], instance.tijd])

    # check whether this solves sub assembly shortage in stock, if there was one (first part of if)
    if len(instance.measures['supply shortage periods']['omhulsel maken']) > 0 and len(instance.measures['supply shortage periods']['omhulsel maken'][-1]) == 1 \
            and all(instance.materialstate[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['raw material'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['raw material'].keys()) \
            and all(instance.stockstate_subassemblies[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['subassembly'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['subassembly'].keys()):
        for i in range(len(instance.inventories[2])):
            if len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage']) > 0 and len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage'][-1]) == 1:
                instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage'][-1].append(instance.tijd)
        # update the supply shortage measure, als er hiervoor supply shortage was
        instance.measures['supply shortage periods']['omhulsel maken'][-1].append(instance.tijd)

    # what goes in the machine, try starting from inventory:
    instance = Functions_start_process_steps.start_process_staal_koppelen(instance, settingdistibution_dict)

    # what goes out of the machine (might needed the subassembly to start), try starting from inventory
    instance = Functions_start_process_steps.start_process_omhulsel_maken(instance, settingdistibution_dict)

    instance.nexteventtimes['staal koppelen klaar'] = instance.orders_inprocess1[0][0]
    instance.nexteventtimes["omhulsel klaar"] = instance.orders_inprocess2[0][0]

    return instance

# event if an omhulsel maken order in process is finished
def event_omhulsel_klaar(instance, settingdistibution_dict):
    # update the machine itself (its workstate and the measures)
    processed_order = instance.orders_inprocess2.pop(0)
    instance.measures['workstate times'][2][instance.work_state[2][0]] += instance.tijd - instance.work_state[2][1]
    instance.work_state[2][0] -= processed_order[1]
    instance.work_state[2][1] = instance.tijd

    processed_order[2]['finish time'] = instance.tijd
    processed_order[2]['total process time'] =  processed_order[2]['finish time'] - processed_order[2]['time received']
    instance.finishedorders.append(processed_order[2])

    # update amount produced
    instance.amountproduced += processed_order[1]

    # what goes in the machine, try starting from inventory:
    instance = Functions_start_process_steps.start_process_omhulsel_maken(instance, settingdistibution_dict)

    instance.nexteventtimes["omhulsel klaar"] = instance.orders_inprocess2[0][0]

    return instance

# event if a new order stalen stangen to the supplier is placed
def event_order_new_stalen_stangen(instance, settingdistibution_dict):
    # update the time of next order, determine the amount of stock to order, take the delivery time and quantity (with uncertainty) and add it io supplyorders in process
    instance.nexteventtimes['order new stalen stangen'] += settingdistibution_dict['supply interval order']
    timeoftheorder = instance.tijd + Functions_get_info.get_supplytime_stalen_stangen(settingdistibution_dict['mean supply time stalen stangen'], settingdistibution_dict['stdev supply time stalen stangen'])
    amountinqueuetorderextra = sum(instance.inventories[0][i][2]['bill of materials']['staal buigen']['raw material']['stalen stangen'] for i in range(len(instance.inventories[0])))
    instance.supplyorders_stalenstangen_inprocess.insert(0, [timeoftheorder, Functions_get_info.get_delivered_order_quantity(settingdistibution_dict['reorder upto stalen stangen'] + amountinqueuetorderextra - instance.materialstate[0]['stalen stangen'], settingdistibution_dict['stddev order hoeveelheid als percentage van quantity'])])
    instance.nexteventtimes['supply stalen stangen'] = timeoftheorder

    return instance

# event if a new order koppeldraad to the supplier is placed
def event_order_new_koppeldraad(instance, settingdistibution_dict):
    # update the time of next order, determine the amount of stock to order, take the delivery time and quantity (with uncertainty) and add it io supplyorders in process
    instance.nexteventtimes['order new koppeldraad'] += settingdistibution_dict['supply interval order']
    timeoftheorder = instance.tijd + Functions_get_info.get_supplytime_koppeldraad(settingdistibution_dict['mean supply time koppeldraad'], settingdistibution_dict['stdev supply time koppeldraad'])
    amountinqueuetorderextra = sum(instance.inventories[1][i][2]['bill of materials']['staal koppelen']['raw material']['koppeldraad'] for i in range(len(instance.inventories[1])))
    instance.supplyorders_koppeldraad_inprocess.insert(0, [timeoftheorder, Functions_get_info.get_delivered_order_quantity(settingdistibution_dict['reorder upto koppeldraad'] + amountinqueuetorderextra - instance.materialstate[1]['koppeldraad'], settingdistibution_dict['stddev order hoeveelheid als percentage van quantity'])])
    instance.nexteventtimes['supply koppeldraad'] = timeoftheorder
    return instance

# event if a new order stuffing to the supplier is placed
def event_order_new_stuffing(instance, settingdistibution_dict):
    # update the time of next order, determine the amount of stock to order, take the delivery time and quantity (with uncertainty) and add it io supplyorders in process
    instance.nexteventtimes['order new stuffing'] += settingdistibution_dict['supply interval order']
    timeoftheorder = instance.tijd + Functions_get_info.get_supplytime_stuffing(settingdistibution_dict['mean supply time stuffing'], settingdistibution_dict['stdev supply time stuffing'])
    amountinqueuetorderextra = {'soft stuffing': 0, 'medium stuffing': 0,'hard stuffing': 0,}
    for i in range(len(instance.inventories[2])):
        for j in instance.inventories[2][i][2]['bill of materials']['omhulsel maken']['raw material'].keys():
            amountinqueuetorderextra[j] += instance.inventories[2][i][2]['bill of materials']['omhulsel maken']['raw material'][j]

    instance.supplyorders_stuffing_inprocess.insert(0, [timeoftheorder, {'soft stuffing': Functions_get_info.get_delivered_order_quantity(settingdistibution_dict['reorder upto soft stuffing'] + amountinqueuetorderextra['soft stuffing'] - instance.materialstate[2]['soft stuffing'], settingdistibution_dict['stddev order hoeveelheid als percentage van quantity']), 'medium stuffing': Functions_get_info.get_delivered_order_quantity(settingdistibution_dict['reorder upto medium stuffing'] + amountinqueuetorderextra['medium stuffing'] - instance.materialstate[2]['medium stuffing'], settingdistibution_dict['stddev order hoeveelheid als percentage van quantity']), 'hard stuffing': Functions_get_info.get_delivered_order_quantity(settingdistibution_dict['reorder upto hard stuffing'] + amountinqueuetorderextra['hard stuffing'] - instance.materialstate[2]['hard stuffing'], settingdistibution_dict['stddev order hoeveelheid als percentage van quantity'])}])
    instance.nexteventtimes['supply stuffing'] = timeoftheorder
    return instance

# event if a new order stalen stangen to the supplier is delivered
def event_supplyorder_stalen_stangen(instance, settingdistibution_dict):
    # for the measures, add before and after the updating to have the complete lines, otherwise the measures only have a starting time but no end time
    instance.measures['stock levels']['raw materials']['stalen stangen'].append([instance.materialstate[0]['stalen stangen'], instance.tijd])
    instance.materialstate[0]['stalen stangen'] += instance.supplyorders_stalenstangen_inprocess[0][1]
    instance.measures['stock levels']['raw materials']['stalen stangen'].append([instance.materialstate[0]['stalen stangen'], instance.tijd])
    instance.supplyorders_stalenstangen_inprocess.pop(0)
    instance.nexteventtimes['supply stalen stangen'] = instance.supplyorders_stalenstangen_inprocess[0][0]

    # update supply shortage measure of the orders in inventory, this disruption is finished (might come back later tho)
    for i in range(len(instance.inventories[0])):
        if len(instance.inventories[0][i][2]['reason inventory staal buigen']['supply shortage']) > 0 and len(instance.inventories[0][i][2]['reason inventory staal buigen']['supply shortage'][-1]) == 1:
            instance.inventories[0][i][2]['reason inventory staal buigen']['supply shortage'][-1].append(instance.tijd)

    # update the supply shortage measure, if there was supply shortage before
    if len(instance.measures['supply shortage periods']['staal buigen']) > 0 and len(instance.measures['supply shortage periods']['staal buigen'][-1]) == 1:
        instance.measures['supply shortage periods']['staal buigen'][-1].append(instance.tijd)

    #if those materials were needed for een order staal buigen om te beginnnen, zet deze in gang.
    # what goes in the machine staal buigen
    instance = Functions_start_process_steps.start_process_staal_buigen(instance, settingdistibution_dict)

    instance.nexteventtimes["staal buigen klaar"] = instance.orders_inprocess0[0][0]

    return instance

# event if a new order koppeldraad to the supplier is delivered
def event_supplyorder_koppeldraad(instance, settingdistibution_dict):
    # for the measures, add before and after the updating to have the complete lines, otherwise the measures only have a starting time but no end time
    instance.measures['stock levels']['raw materials']['koppeldraad'].append([instance.materialstate[1]['koppeldraad'], instance.tijd])
    instance.materialstate[1]['koppeldraad'] += instance.supplyorders_koppeldraad_inprocess[0][1]
    instance.measures['stock levels']['raw materials']['koppeldraad'].append([instance.materialstate[1]['koppeldraad'], instance.tijd])
    instance.supplyorders_koppeldraad_inprocess.pop(0)
    instance.nexteventtimes['supply koppeldraad'] = instance.supplyorders_koppeldraad_inprocess[0][0]

    # update supply shortage measure of the orders in inventory , this disruption is finished (might come back later tho)
    if len(instance.measures['supply shortage periods']['staal koppelen']) > 0 and len(instance.measures['supply shortage periods']['staal koppelen'][-1]) == 1 \
            and all(instance.materialstate[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen']['raw material'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen']['raw material'].keys()) \
            and all(instance.stockstate_subassemblies[1][i] >= instance.inventories[1][0][2]['bill of materials']['staal koppelen']['subassembly'][i] for i in instance.inventories[1][0][2]['bill of materials']['staal koppelen']['subassembly'].keys()):
        for i in range(len(instance.inventories[1])):
            if len(instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage']) > 0 and len(instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage'][-1]) == 1:
                instance.inventories[1][i][2]['reason inventory staal koppelen']['supply shortage'][-1].append(instance.tijd)

        # update the supply shortage measure, if there was supply shortage before (is tested in the if statement
        instance.measures['supply shortage periods']['staal koppelen'][-1].append(instance.tijd)

    #if those materials were needed for een order staal buigen om te beginnnen, zet deze in gang.
    # what goes in the machine staal koppelen
    instance = Functions_start_process_steps.start_process_staal_koppelen(instance, settingdistibution_dict)

    instance.nexteventtimes['staal koppelen klaar'] = instance.orders_inprocess1[0][0]

    return instance

# event if a new order stuffing to the supplier is delivered
def event_supplyorder_stuffing(instance, settingdistibution_dict):
    # for the measures, add before and after the updating to have the complete lines, otherwise the measures only have a starting time but no end time
    instance.measures['stock levels']['raw materials']['soft stuffing'].append([instance.materialstate[2]['soft stuffing'], instance.tijd])
    instance.measures['stock levels']['raw materials']['medium stuffing'].append([instance.materialstate[2]['medium stuffing'], instance.tijd])
    instance.measures['stock levels']['raw materials']['hard stuffing'].append([instance.materialstate[2]['hard stuffing'], instance.tijd])
    instance.materialstate[2]['soft stuffing'] += instance.supplyorders_stuffing_inprocess[0][1]['soft stuffing']
    instance.materialstate[2]['medium stuffing'] += instance.supplyorders_stuffing_inprocess[0][1]['medium stuffing']
    instance.materialstate[2]['hard stuffing'] += instance.supplyorders_stuffing_inprocess[0][1]['hard stuffing']
    instance.measures['stock levels']['raw materials']['soft stuffing'].append([instance.materialstate[2]['soft stuffing'], instance.tijd])
    instance.measures['stock levels']['raw materials']['medium stuffing'].append([instance.materialstate[2]['medium stuffing'], instance.tijd])
    instance.measures['stock levels']['raw materials']['hard stuffing'].append([instance.materialstate[2]['hard stuffing'], instance.tijd])
    instance.supplyorders_stuffing_inprocess.pop(0)
    instance.nexteventtimes['supply stuffing'] = instance.supplyorders_stuffing_inprocess[0][0]

    # update supply shortage measure of the orders in inventory , this disruption is finished (might come back later tho)
    if len(instance.measures['supply shortage periods']['omhulsel maken']) > 0 and len(instance.measures['supply shortage periods']['omhulsel maken'][-1]) == 1 \
            and all(instance.materialstate[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['raw material'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['raw material'].keys()) \
            and all(instance.stockstate_subassemblies[2][i] >= instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['subassembly'][i] for i in instance.inventories[2][0][2]['bill of materials']['omhulsel maken']['subassembly'].keys()):
        for i in range(len(instance.inventories[2])):
            if len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage']) > 0 and len(instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage'][-1]) == 1:
                instance.inventories[2][i][2]['reason inventory omhulsel maken']['supply shortage'][-1].append(instance.tijd)

        # update the supply shortage measure, if there was supply shortage before (is tested in the if statement
        instance.measures['supply shortage periods']['omhulsel maken'][-1].append(instance.tijd)

    #if those materials were needed for een order staal buigen om te beginnnen, zet deze in gang.
    # what goes in the machine staal buigen
    instance = Functions_start_process_steps.start_process_omhulsel_maken(instance, settingdistibution_dict)

    instance.nexteventtimes["omhulsel klaar"] = instance.orders_inprocess2[0][0]

    return instance

# event if the staalbuigen step goes into breakdown
def event_staalbuigen_breakdown(instance, settingdistibution_dict):
    # set time until next breakdown to infinity, reduce capacity of this step to 0 and get the time when it is fixed
    instance.nexteventtimes['staal buigen breakdown'] = math.inf
    instance.capacities[0] = 0
    instance.nexteventtimes['fix staal buigen breakdown'] = instance.tijd + Functions_get_info.get_length_fix_staalbuigen_breakdown(settingdistibution_dict['mean fix staal buigen breakdown'])

    # update the reason of a product in inventory
    for i in range(len(instance.inventories[0])):
        instance.inventories[0][i][2]['reason inventory staal buigen']['breakdown'].append([instance.tijd])

    # update measures
    instance.measures['breakdown periods']['staal buigen'].append([instance.tijd])

    return instance

# event if the staalbuigen breakdown is fixed
def event_fixed_staalbuigen_breakdown(instance, settingdistibution_dict):
    # set to until next breakdown, set capacity to original capacity and set fixing time to infinity
    instance.nexteventtimes['staal buigen breakdown'] = instance.tijd + Functions_get_info.get_length_next_staalbuigen_breakdown(settingdistibution_dict['mean staal buigen breakdown'])
    instance.capacities[0] = settingdistibution_dict['capacity staal buigen']
    instance.nexteventtimes['fix staal buigen breakdown'] = math.inf

    # update the reason of a product in inventory
    for i in range(len(instance.inventories[0])):
        instance.inventories[0][i][2]['reason inventory staal buigen']['breakdown'][-1].append(instance.tijd)

    #if this capacity was needed for orders to start, start them
    # what goes in the machine staal buigen
    instance = Functions_start_process_steps.start_process_staal_buigen(instance, settingdistibution_dict)

    instance.nexteventtimes["staal buigen klaar"] = instance.orders_inprocess0[0][0]

    # update measures
    instance.measures['breakdown periods']['staal buigen'][-1].append(instance.tijd)
    return instance

# event if the staal koppelen step goes into breakdown
def event_staalkoppelen_breakdown(instance, settingdistibution_dict):
    # set time until next breakdown to infinity, reduce capacity of this step to 0 and get the time when it is fixed
    instance.nexteventtimes['staal koppelen breakdown'] = math.inf
    instance.capacities[1] = 0
    instance.nexteventtimes['fix staal koppelen breakdown'] = instance.tijd + Functions_get_info.get_length_fix_staalkoppelen_breakdown(settingdistibution_dict['mean fix staal koppelen breakdown'])

    # update the reason of a product in inventory
    for i in range(len(instance.inventories[1])):
        instance.inventories[1][i][2]['reason inventory staal koppelen']['breakdown'].append([instance.tijd])

    # update measures
    instance.measures['breakdown periods']['staal koppelen'].append([instance.tijd])
    return instance

# # event if the staal koppelen breakdown is fixed
def event_fixed_staalkoppelen_breakdown(instance, settingdistibution_dict):
    # set to until next breakdown, set capacity to original capacity and set fixing time to infinity
    instance.nexteventtimes['staal koppelen breakdown'] = instance.tijd + Functions_get_info.get_length_next_staalkoppelen_breakdown(settingdistibution_dict['mean staal koppelen breakdown'])
    instance.capacities[1] = settingdistibution_dict['capacity staal koppelen']
    instance.nexteventtimes['fix staal koppelen breakdown'] = math.inf

    # update breakdown measure of the orders in inventory
    for i in range(len(instance.inventories[1])):
        instance.inventories[1][i][2]['reason inventory staal koppelen']['breakdown'][-1].append(instance.tijd)

    #if this capacity was needed for orders to start, start them
    # what goes in the machine staal buigen
    instance = Functions_start_process_steps.start_process_staal_koppelen(instance, settingdistibution_dict)

    instance.nexteventtimes['staal koppelen klaar'] = instance.orders_inprocess1[0][0]

    # update measures
    instance.measures['breakdown periods']['staal koppelen'][-1].append(instance.tijd)
    return instance

# event if the omhulsel maken step goes into breakdown
def event_omhulselmaken_breakdown(instance, settingdistibution_dict):
    # set time until next breakdown to infinity, reduce capacity of this step to 0 and get the time when it is fixed
    instance.nexteventtimes['omhulsel maken breakdown'] = math.inf
    instance.capacities[2] = 0
    instance.nexteventtimes['fix omhulsel maken breakdown'] = instance.tijd + Functions_get_info.get_length_fix_omhulselmaken_breakdown(settingdistibution_dict['mean fix omhulsel maken breakdown'])

    # update the reason of a product in inventory
    for i in range(len(instance.inventories[2])):
        instance.inventories[2][i][2]['reason inventory omhulsel maken']['breakdown'].append([instance.tijd])

    # update measures
    instance.measures['breakdown periods']['omhulsel maken'].append([instance.tijd])
    return instance

# event if the omhulsel maken breakdown is fixed
def event_fixed_omhulselmaken_breakdown(instance, settingdistibution_dict):
    # set to until next breakdown, set capacity to original capacity and set fixing time to infinity
    instance.nexteventtimes['omhulsel maken breakdown'] = instance.tijd + Functions_get_info.get_length_next_omhulselmaken_breakdown(settingdistibution_dict['mean omhulsel maken breakdown'])
    instance.capacities[2] = settingdistibution_dict['capacity omhulsel maken']
    instance.nexteventtimes['fix omhulsel maken breakdown'] = math.inf

    # update breakdown measure of the orders in inventory
    for i in range(len(instance.inventories[2])):
        instance.inventories[2][i][2]['reason inventory omhulsel maken']['breakdown'][-1].append(instance.tijd)

    # if this capacity was needed for orders to start, start them
    # what goes in the machine staal buigen
    instance = Functions_start_process_steps.start_process_omhulsel_maken(instance, settingdistibution_dict)

    # update measures
    instance.measures['breakdown periods']['omhulsel maken'][-1].append(instance.tijd)
    return instance

# updatevariables calls the event function for the given event, thereby it also updates the current time
def updatevariables(instance, event, next_t_event, settingdistibution_dict):

    #print('updating this event type: ', event)
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
