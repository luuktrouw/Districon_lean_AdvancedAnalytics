'''
This is a sample simulation of a simple production process
The production process consists of 3 sequential parts, with each a inventory level in front of them
Supplier-> inv-> productionstep A-> inv-> productionstep B-> inv-> productionstep C-> final inv-> customer
The production steps each have certain distribution of lead times (for example N(4,2))
Everything is in seconds
'''
import math

import Functions4simulation
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import statistics

numberloops = 1

totalinventorie_measure = []

eventnames = ["new order", "staal buigen klaar", "staal koppelen klaar", "omhulsel klaar"]

###########################
class instancezero():
    def __init__(self):
        self.work_state= [0, 0, 0]
        self.inventories = [[], [], []]
        self.tijd = 0
        self.t_neworder = 4
        self.t1klaar = math.inf
        self.t2klaar = math.inf
        self.t3klaar = math.inf
        self.orders_inprocess0 = [[math.inf],[0]] #first list is the finish times, second the order sizes
        self.orders_inprocess1 = [[math.inf],[0]]
        self.orders_inprocess2 = [[math.inf],[0]]
        self.amountproduced = 0
        self.capacities = [10,10,10]

        # measures


for loopcounter in range(numberloops):
    print('current loop number: ', loopcounter)
    inventories_measure = [[], [], []]
    eventcounter = 0

    instance = instancezero()

    while instance.tijd <= 5000:
        previoustime = instance.tijd

        next_t_event = min(instance.t_neworder, instance.orders_inprocess0[0][0], instance.orders_inprocess1[0][0], instance.orders_inprocess2[0][0])
        next_event = eventnames[np.argmin([instance.t_neworder, instance.orders_inprocess0[0][0], instance.orders_inprocess1[0][0], instance.orders_inprocess2[0][0]])]
        instance = Functions4simulation.updatevariables(instance, next_event, next_t_event)
        #print('tijd: ', instance.tijd)
        #print('inventories: ', sum(instance.inventories[0]), sum(instance.inventories[1]), sum(instance.inventories[2]))


        if len(instance.inventories[0]) > 0:
            firstorder0 = instance.inventories[0][0]
        else:
            firstorder0 =0
        if len(instance.inventories[1]) > 0:
            firstorder1 = instance.inventories[1][0]
        else:
            firstorder1 =0
        if len(instance.inventories[2]) > 0:
            firstorder2 = instance.inventories[2][0]
        else:
            firstorder2 =0


        #print('size fifo order:', firstorder0, firstorder1, firstorder2)
        #print('what is working on how many? ', instance.work_state)
        #print('')

        eventcounter += 1

        nexttime = instance.tijd
        timeunits = int(round(nexttime - previoustime,0))
        for i in range(timeunits):
            inventories_measure[0].append(sum(instance.inventories[0]))
            inventories_measure[1].append(sum(instance.inventories[1]))
            inventories_measure[2].append(sum(instance.inventories[2]))

    totalinventorie_measure.append(inventories_measure)



print('total inventories at the end of time:', sum(instance.inventories[0]), sum(instance.inventories[1]),sum(instance.inventories[2]))
'''
plt.hist(x=inventories_measure[0], alpha = 0.3, label = 'inv before 0')
plt.hist(x=inventories_measure[1], alpha = 0.3, label = 'inv before 1')
plt.hist(x=inventories_measure[2], alpha = 0.3, label = 'inv before 2')
plt.legend()
plt.show()
'''
print('average inventory before point 0:', statistics.mean(inventories_measure[0]))
print('average inventory before point 1:', statistics.mean(inventories_measure[1]))
print('average inventory before point 2:', statistics.mean(inventories_measure[2]))


print_inventory = [[totalinventorie_measure[i][0][j] for i in range(len(totalinventorie_measure)) for j in range(len(totalinventorie_measure[i][0]))]  , [totalinventorie_measure[i][1][j] for i in range(len(totalinventorie_measure)) for j in range(len(totalinventorie_measure[i][1]))]  ,  [totalinventorie_measure[i][2][j] for i in range(len(totalinventorie_measure)) for j in range(len(totalinventorie_measure[i][2]))] ]

plt.hist([print_inventory[0],print_inventory[1], print_inventory[2]], weights=[np.ones(len(print_inventory[0])) / len(print_inventory[0]) for w in range(3)], label = ['inv before 0','inv before 1', 'inv before 2'])
#plt.hist(x=print_inventory[1], bins = 50, label = 'inv before 1')
#plt.hist(x=print_inventory[2], bins = 50, label = 'inv before 2')
plt.legend()
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()





