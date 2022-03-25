'''
This is a sample simulation of a simple production process
The production process consists of 3 sequential parts, with each a inventory level in front of them
Supplier-> inv-> productionstep A-> inv-> productionstep B-> inv-> productionstep C-> final inv-> customer
The production steps each have certain distribution of lead times (for example N(4,2))
Everything is in seconds
'''
import Functions4simulation
import math
import plotly.express as px
import plotly.graph_objects as go
import Functions4simulation
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import statistics
import pandas as pd
import plottingfunctions
import Functions
import Functions_get_info




def runsimulation(settingdistibution_dict):

    numberloops = 1

    totalinventorie_measure = []

    #EVENT NAMES IS IN ORDER, otherwise the next_t_event will not work
    eventnames = ["new order", "staal buigen klaar", "staal koppelen klaar", "omhulsel klaar", 'supply stalen stangen', 'supply koppeldraad', 'supply stuffing', 'order new stalen stangen', 'order new koppeldraad', 'order new stuffing']

    ###########################
    class instancezero():
        def __init__(self):
            initdict1 = {}
            initdict2 = {}
            initdict3 = {}
            self.work_state= [[0,0], [0,0], [0,0]]
            self.materialstate = [{'stalen stangen': settingdistibution_dict['reorder upto stalen stangen']},
                                  {'koppeldraad':settingdistibution_dict['reorder upto koppeldraad']},
                                  {'soft stuffing': settingdistibution_dict['reorder upto soft stuffing'],
                                   'medium stuffing': settingdistibution_dict['reorder upto medium stuffing'],
                                   'hard stuffing': settingdistibution_dict['reorder upto hard stuffing']}
                                  ]
            self.stockstate_subassemblies = [{},{'gebogen stangen':settingdistibution_dict['SS gebogen stangen']},
                                                {'gekoppeld eenpersoons': settingdistibution_dict['SS gekoppeld eenpersoons'],
                                                 'gekoppeld twijfelaar': settingdistibution_dict['SS gekoppeld twijfelaar'],
                                                 'gekoppeld queensize': settingdistibution_dict['SS gekoppeld queensize'],
                                                 'gekoppeld kingsize': settingdistibution_dict['SS gekoppeld kingsize'],
                                                 }]
            self.priority_materialstate = [{'stalen stangen': 100}, {'koppeldraad': 100}, {'soft stuffing': 100, 'medium stuffing': 100, 'hard stuffing': 100}]
            self.priority_stockstate_subassemblies = [{}, {'gebogen stangen': settingdistibution_dict['SS gebogen stangen']},
                                             {'gekoppeld eenpersoons': settingdistibution_dict['SS gekoppeld eenpersoons'],
                                              'gekoppeld twijfelaar': settingdistibution_dict['SS gekoppeld twijfelaar'],
                                              'gekoppeld queensize': settingdistibution_dict['SS gekoppeld queensize'],
                                              'gekoppeld kingsize': settingdistibution_dict['SS gekoppeld kingsize'],
                                              }]
            self.supplyorders_stalenstangen_inprocess = [[math.inf,0]]
            self.supplyorders_koppeldraad_inprocess = [[math.inf,0]]
            self.supplyorders_stuffing_inprocess = [[math.inf,{'soft stuffing': 0, 'medium stuffing': 0, 'hard stuffing': 0}]]
            self.inventories = [[], [], []]
            self.tijd = 0
            self.orders_inprocess0 = [[math.inf,0,initdict1]] #first list is the finish times, second the order sizes
            self.orders_inprocess1 = [[math.inf,0,initdict2]]
            self.orders_inprocess2 = [[math.inf,0,initdict3]]
            self.nexteventtimes = {'new order': Functions_get_info.get_length_neworder(settingdistibution_dict['order time mean'], settingdistibution_dict['order time stdev']),
                                   "staal buigen klaar" : self.orders_inprocess0[0][0],
                                   "staal koppelen klaar": self.orders_inprocess1[0][0],
                                   "omhulsel klaar": self.orders_inprocess2[0][0],
                                   'supply stalen stangen':self.supplyorders_stalenstangen_inprocess[0][0],
                                   'supply koppeldraad': self.supplyorders_koppeldraad_inprocess[0][0],
                                   'supply stuffing': self.supplyorders_stuffing_inprocess[0][0],
                                   'order new stalen stangen': settingdistibution_dict['supply interval order'],
                                   'order new koppeldraad': settingdistibution_dict['supply interval order'],
                                   'order new stuffing': settingdistibution_dict['supply interval order'],
                                   'staal buigen breakdown': Functions_get_info.get_length_next_staalbuigen_breakdown(settingdistibution_dict['mean staal buigen breakdown']),
                                   'staal koppelen breakdown': Functions_get_info.get_length_next_staalkoppelen_breakdown(settingdistibution_dict['mean staal koppelen breakdown']),
                                   'omhulsel maken breakdown': Functions_get_info.get_length_next_omhulselmaken_breakdown(settingdistibution_dict['mean omhulsel maken breakdown']),
                                   'fix staal buigen breakdown': math.inf,
                                   'fix staal koppelen breakdown': math.inf,
                                   'fix omhulsel maken breakdown': math.inf}
            self.amountproduced = 0
            self.capacities = [settingdistibution_dict['capacity staal buigen'],settingdistibution_dict['capacity staal koppelen'],settingdistibution_dict['capacity omhulsel maken']]
            self.measures = {'workstate times':[{i: 0 for i in range(self.capacities[0] + 1)},
                                                {i: 0 for i in range(self.capacities[1] + 1)},
                                                {i: 0 for i in range(self.capacities[2] + 1)}],
                             'breakdown periods': {'staal buigen':[], 'staal koppelen': [], 'omhulsel maken':[]},
                             'supply shortage periods': {'staal buigen':[], 'staal koppelen': [], 'omhulsel maken':[]},
                             'subassembly shortage periods': {'staal buigen': [], 'staal koppelen': [], 'omhulsel maken': []},
                             'stock levels': {'raw materials': {'stalen stangen': [[self.materialstate[0]['stalen stangen'],self.tijd]],
                                                                'koppeldraad': [[self.materialstate[1]['koppeldraad'],self.tijd]],
                                                                'soft stuffing': [[self.materialstate[2]['soft stuffing'],self.tijd]],
                                                                'medium stuffing': [[self.materialstate[2]['medium stuffing'],self.tijd]],
                                                                'hard stuffing':[[self.materialstate[2]['hard stuffing'],self.tijd]]},
                                               'subassemblies': {'gebogen stangen': [[self.stockstate_subassemblies[1]['gebogen stangen'],self.tijd]],
                                                                'gekoppeld eenpersoons': [[self.stockstate_subassemblies[2]['gekoppeld eenpersoons'],self.tijd]],
                                                                'gekoppeld twijfelaar':[[self.stockstate_subassemblies[2]['gekoppeld twijfelaar'],self.tijd]],
                                                                'gekoppeld queensize':[[self.stockstate_subassemblies[2]['gekoppeld queensize'],self.tijd]],
                                                                'gekoppeld kingsize':[[self.stockstate_subassemblies[2]['gekoppeld kingsize'],self.tijd]],
                                                                }
                                              }
                            }
            self.finishedorders = [] # list consisting of dictionaries of orders

            # measures

    for loopcounter in range(numberloops):
        print('current loop number: ', loopcounter)
        eventcounter = 0

        instance = instancezero()
        instance.tijd

        curtimeinterval = 4800000
        timeinterval = 4800000

        while instance.tijd <= 4800000:
            previoustime = instance.tijd
            if instance.tijd > curtimeinterval:
                print('current time in simulation is: ', curtimeinterval)
                curtimeinterval += timeinterval
            next_event = min(instance.nexteventtimes, key=instance.nexteventtimes.get)
            next_t_event = instance.nexteventtimes[next_event]
            instance = Functions4simulation.updatevariables(instance, next_event, next_t_event, settingdistibution_dict)
            #print('tijd: ', instance.tijd)
            #print('inventories: ', sum(instance.inventories[0]), sum(instance.inventories[1]), sum(instance.inventories[2]))

            eventcounter += 1

    # close the disruption measures
    instance.measures = Functions.close_disruption_measures(instance.measures, instance.tijd)

    #########
    # Make dataframe of all finished orders
    #########
    finished_orders_df = pd.DataFrame(instance.finishedorders)

    for i in range(len(finished_orders_df)):
        if i not in finished_orders_df.index:
            print('hoiiiiii')
            print(len(finished_orders_df))
            print(i)

    #sommige disruptions kunnen nog niet gesloten zijn, bijvoorbeeld als de order al wel klaar is (omhulsel maken klaar), maar nog niet staal buigen ding heeft afgerond en dan stopt de tijd plots. dam telt t niet als helemaal klaar, dus verwijder uit finished orders
    finished_orders_df = Functions.delete_nonfinished_orders_disruptions(finished_orders_df)

    for i in range(len(finished_orders_df)):
        if i not in finished_orders_df.index:
            print('hoi')
            print(len(finished_orders_df))
            print(i)

    finished_orders_df['total queue time'] = [finished_orders_df['tijd inventory staal buigen'][i] + finished_orders_df['tijd inventory staal koppelen'][i] + finished_orders_df['tijd inventory omhulsel maken'][i] for i in range(len(finished_orders_df))]

    finished_orders_df['total producing time'] = [finished_orders_df['tijd staal buigen'][i] + finished_orders_df['tijd staal koppelen'][i] + finished_orders_df['tijd omhulsel maken'][i] for i in range(len(finished_orders_df))]

    finished_orders_df['lateness'] = [max(finished_orders_df['finish time'][i] - finished_orders_df['deadline order'][i],0) for i in range(len(finished_orders_df))]

    means = {'total process time': finished_orders_df['total process time'].mean(), 'total queue time': finished_orders_df['total queue time'].mean(), 'queue staal buigen': finished_orders_df['tijd inventory staal buigen'].mean(), 'queue staal koppelen': finished_orders_df['tijd inventory staal koppelen'].mean(),'queue omhulsel maken': finished_orders_df['tijd inventory omhulsel maken'].mean(),
             'staal buigen': finished_orders_df['tijd staal buigen'].mean(), 'staal koppelen': finished_orders_df['tijd staal koppelen'].mean(), 'omhulsel maken': finished_orders_df['tijd omhulsel maken'].mean(), 'total producing time': finished_orders_df['total producing time'].mean(), 'lateness': finished_orders_df['lateness'].mean()}

    lower_5_quantiles = {'total process time': finished_orders_df['total process time'].quantile(.05), 'total queue time': finished_orders_df['total queue time'].quantile(.05), 'queue staal buigen': finished_orders_df['tijd inventory staal buigen'].quantile(.05), 'queue staal koppelen': finished_orders_df['tijd inventory staal koppelen'].quantile(.05),'queue omhulsel maken': finished_orders_df['tijd inventory omhulsel maken'].quantile(.05),
             'staal buigen': finished_orders_df['tijd staal buigen'].quantile(.05), 'staal koppelen': finished_orders_df['tijd staal koppelen'].quantile(.05), 'omhulsel maken': finished_orders_df['tijd omhulsel maken'].quantile(.05), 'total producing time': finished_orders_df['total producing time'].quantile(.05), 'lateness': finished_orders_df['lateness'].quantile(.05)}

    upper_95_quantiles = {'total process time': finished_orders_df['total process time'].quantile(.95),
                         'total queue time': finished_orders_df['total queue time'].quantile(.95),
                         'queue staal buigen': finished_orders_df['tijd inventory staal buigen'].quantile(.95),
                         'queue staal koppelen': finished_orders_df['tijd inventory staal koppelen'].quantile(.95),
                         'queue omhulsel maken': finished_orders_df['tijd inventory omhulsel maken'].quantile(.95),
                         'staal buigen': finished_orders_df['tijd staal buigen'].quantile(.95),
                         'staal koppelen': finished_orders_df['tijd staal koppelen'].quantile(.95),
                         'omhulsel maken': finished_orders_df['tijd omhulsel maken'].quantile(.95),
                         'total producing time': finished_orders_df['total producing time'].quantile(.95),
                         'lateness': finished_orders_df['lateness'].quantile(.95)}

    #########
    # Make dataframe of all finished orders
    #########

    work_state_times_df = pd.DataFrame(instance.measures['workstate times'])

    #print_inventory = [[totalinventorie_measure[i][0][j] for i in range(len(totalinventorie_measure)) for j in range(len(totalinventorie_measure[i][0]))]  , [totalinventorie_measure[i][1][j] for i in range(len(totalinventorie_measure)) for j in range(len(totalinventorie_measure[i][1]))]  ,  [totalinventorie_measure[i][2][j] for i in range(len(totalinventorie_measure)) for j in range(len(totalinventorie_measure[i][2]))] ]

    fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time = plottingfunctions.Make_kpi_figures(finished_orders_df)

    fig_gantt_disruptions = plottingfunctions.plot_gantt_disruptions(instance.measures)

    ffiiiff = plottingfunctions.make_violin_VSM_statistics(finished_orders_df)
    return finished_orders_df, instance.measures, means, lower_5_quantiles, upper_95_quantiles, fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time, fig_gantt_disruptions, instance.tijd


#fig = px.histogram(finished_orders_df, x="tijd inventory staal buigen")
#fig.show()

#fig = px.histogram(finished_orders_df, x="tijd inventory staal koppelen")
#fig.show()

#fig = px.histogram(finished_orders_df, x="tijd inventory omhulsel maken")
#fig.show()

#plottingfunctions.plotworkstates_fractions_staalbuigen(instance.work_state_times[0])

#plottingfunctions.plotworkstates_fractions_staalkoppelen(instance.work_state_times[1])

#plottingfunctions.plotworkstates_fractions_omhulselmaken(instance.work_state_times[2])

#plottingfunctions.wachttijd_voor_staal_buigen(instance.finishedorders)

'''
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
'''
