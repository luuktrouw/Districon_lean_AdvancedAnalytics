'''
This is a sample simulation of a simple production process
The production process consists of 3 sequential parts, with each a inventory level in front of them
Supplier-> inv-> productionstep A-> inv-> productionstep B-> inv-> productionstep C-> final inv-> customer
The production steps each have certain distribution of lead times (for example N(4,2))
Everything is in seconds
'''
import math
import plotly.express as px
import Functions4simulation
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import statistics
import plottingfunctions

numberloops = 1

totalinventorie_measure = []

eventnames = ["new order", "staal buigen klaar", "staal koppelen klaar", "omhulsel klaar", 'supply stalen stangen']

###########################
class instancezero():
    def __init__(self):
        initdict1 = {}
        initdict2 = {}
        initdict3 = {}
        self.work_state= [[0,0], [0,0], [0,0]]
        self.materialstate = [{'stalen stangen': 100},{'koppeldraad': 100000000},{'soft stuffing': math.inf, 'medium stuffing': math.inf,'hard stuffing': math.inf}]
        self.buffers = []
        self.supplyorders_stalenstangen_inprocess = [[math.inf,0]]
        self.supplyorders_stalenstangen_inprocess = [[math.inf,0]]
        self.supplyorders_softstuffing_inprocess = [[math.inf,0]]
        self.supplyorders_mediumstuffing_inprocess = [[math.inf,0]]
        self.supplyorders_hardstuffing_inprocess = [[math.inf,0]]
        self.inventories = [[], [], []]
        self.tijd = 0
        self.t_neworder = 4
        self.orders_inprocess0 = [[math.inf,0,initdict1]] #first list is the finish times, second the order sizes
        self.orders_inprocess1 = [[math.inf,0,initdict2]]
        self.orders_inprocess2 = [[math.inf,0,initdict3]]
        self.amountproduced = 0
        self.capacities = [10,10,10]
        self.work_state_times = [{i: 0 for i in range(self.capacities[0] + 1)}, {i: 0 for i in range(self.capacities[1] + 1)}, {i: 0 for i in range(self.capacities[2] + 1)}]
        self.finishedorders = [] # list consisting of dictionaries of orders

        # measures


for loopcounter in range(numberloops):
    print('current loop number: ', loopcounter)
    inventories_measure = [[], [], []]
    eventcounter = 0

    instance = instancezero()

    curtimeinterval = 100000
    timeinterval = 100000

    while instance.tijd <= 500000:
        previoustime = instance.tijd
        if instance.tijd > curtimeinterval:
            print('current time in simulation is: ', curtimeinterval)
            curtimeinterval += timeinterval

        next_t_event = min(instance.t_neworder, instance.orders_inprocess0[0][0], instance.orders_inprocess1[0][0], instance.orders_inprocess2[0][0], instance.supplyorders_stalenstangen_inprocess[0][0])
        next_event = eventnames[np.argmin([instance.t_neworder, instance.orders_inprocess0[0][0], instance.orders_inprocess1[0][0], instance.orders_inprocess2[0][0], instance.supplyorders_stalenstangen_inprocess[0][0]])]
        instance = Functions4simulation.updatevariables(instance, next_event, next_t_event)
        #print('tijd: ', instance.tijd)
        #print('inventories: ', sum(instance.inventories[0]), sum(instance.inventories[1]), sum(instance.inventories[2]))

        eventcounter += 1

        nexttime = instance.tijd
        timeunits = int(round(nexttime - previoustime,0))
        inventory_staalbuigen = 0
        for i in range(len(instance.inventories[0])):
            inventory_staalbuigen += instance.inventories[0][i][1]
        inventory_staalkoppelen = 0
        for i in range(len(instance.inventories[1])):
            inventory_staalkoppelen += instance.inventories[1][i][1]
        inventory_omhulselplaatsen = 0
        for i in range(len(instance.inventories[2])):
            inventory_omhulselplaatsen += instance.inventories[2][i][1]

        for i in range(timeunits):
            inventories_measure[0].append(inventory_staalbuigen)
            inventories_measure[1].append(inventory_staalkoppelen)
            inventories_measure[2].append(inventory_omhulselplaatsen)

    totalinventorie_measure.append(inventories_measure)


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


inventory_times_staalbuigen = []
for i in range(len(instance.finishedorders)):
    inventory_times_staalbuigen.append(instance.finishedorders[i]['tijd inventory staal buigen'])
plt.hist(inventory_times_staalbuigen, bins = 200)
plt.show()

totalprocesstime = []
for i in range(len(instance.finishedorders)):
    totalprocesstime.append(instance.finishedorders[i]['total process time'])
n, x,_ = plt.hist(totalprocesstime, bins = 50)
bin_centers = 0.5*(x[1:]+x[:-1])
listaveragevaluesn = []
for i in range(5):
    listaveragevaluesn.append(sum(n[:i])/5)
for i in range(5, len(n)):
    listaveragevaluesn.append(sum(n[i-5:i+5])/10)
plt.plot(bin_centers,listaveragevaluesn)
plt.show()

plottingfunctions.plotworkstates_fractions_staalbuigen(instance.work_state_times[0])

plottingfunctions.plotworkstates_fractions_staalkoppelen(instance.work_state_times[1])

plottingfunctions.plotworkstates_fractions_omhulselmaken(instance.work_state_times[2])

plottingfunctions.wachttijd_voor_staal_buigen(instance.finishedorders)

