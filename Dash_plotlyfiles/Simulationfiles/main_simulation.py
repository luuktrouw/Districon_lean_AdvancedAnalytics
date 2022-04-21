'''
This is a sample simulation of a simple production process
The production process consists of 3 sequential parts, with each a inventory level in front of them
Supplier-> inv-> productionstep A-> inv-> productionstep B-> inv-> productionstep C-> final inv-> customer
The production steps each have certain distribution of lead times (for example N(4,2))
Everything is in seconds
'''
import math
from Simulationfiles import Simulation_event_functions
import pandas as pd
import Functions
from Simulationfiles import Functions_get_info




def runsimulation(settingdistibution_dict):

    ###########################
    # the class instancezero initializes the state (instance) of the production process.
    # most initial state variables are received from the setting distribution dictionary which is input
    # each instance variable is described and implemented below
    class instancezero():
        def __init__(self):
            # the work state variables displays the amount of capacity of each production step is currently being used
            # with also the starting time of that working state illustration below:
            # [[workstateprocess 1, start time this workstate], [workstateprocess 2, start time this workstate], [workstateprocess 3, start time this workstate]]
            self.work_state= [[0,0], [0,0], [0,0]]
            # material state is a list which describes the current inventory of raw materials at each process step example below:
            # [{dictionary with raw materials and its current amount in step 1}, {dictionary with raw materials and its current amount in step 2}, {...}]
            self.materialstate = [{'stalen stangen': settingdistibution_dict['reorder upto stalen stangen']},
                                  {'koppeldraad':settingdistibution_dict['reorder upto koppeldraad']},
                                  {'soft stuffing': settingdistibution_dict['reorder upto soft stuffing'],
                                   'medium stuffing': settingdistibution_dict['reorder upto medium stuffing'],
                                   'hard stuffing': settingdistibution_dict['reorder upto hard stuffing']}
                                  ]
            # idem as the work state for the subassemblies at each process step
            self.stockstate_subassemblies = [{},{'gebogen stangen':settingdistibution_dict['SS gebogen stangen']},
                                                {'gekoppeld eenpersoons': settingdistibution_dict['SS gekoppeld eenpersoons'],
                                                 'gekoppeld twijfelaar': settingdistibution_dict['SS gekoppeld twijfelaar'],
                                                 'gekoppeld queensize': settingdistibution_dict['SS gekoppeld queensize'],
                                                 'gekoppeld kingsize': settingdistibution_dict['SS gekoppeld kingsize'],
                                                 }]
            # the supplyorders_..._inprocess describes the placed orders at the supplier for a certain process step, which are in process (need to be delivered)
            # It is a sorted list containing all outstanding supplier orders, each order is a list which is [arrival time of order, ordered ammount]
            # At first, the outstanding order is initialized as 0 with an arrival time of inf to prevent conflicts
            # note that the order list of stalen stangen and koppeldraad have ordered quantitiy without a defined material, this is possible since those steps only contain 1 material
            self.supplyorders_stalenstangen_inprocess = [[math.inf,0]]
            self.supplyorders_koppeldraad_inprocess = [[math.inf,0]]
            self.supplyorders_stuffing_inprocess = [[math.inf,{'soft stuffing': 0, 'medium stuffing': 0, 'hard stuffing': 0}]]
            # the inventory state is also a list for each process.
            # For each process step it contains the orders which are waiting for a production step - in 'inventory' - since they can not be proceced for whatever reason.
            # Each process step has a sorted list based on priority if it is filled. Each order in that list has 3 attributes: [endtime inventory (inf since not determined), ordersize, orderdict (dict with details of order)]
            # Important is that the lists are sorted, and the first order will be the one which will go into the production step next
            # example: [[[math.inf, 4, orderdict_FH10], [math.inf, 2, orderdict_FH14]] , [] , [[math.inf, 2, orderdict_FH14]] ]
            self.inventories = [[], [], []]
            # tijd gives the current time of the simulation
            self.tijd = 0
            # orders_inprocessX contains the orders currently processing in production step X, they are sorted on first finishing time
            # Each order is also: [finish time, size, orderdict]
            # They are initialized as inf and capacity 0, to prevent conflicts
            self.orders_inprocess0 = [[math.inf,0, {}]] #first list is the finish times, second the order sizes
            self.orders_inprocess1 = [[math.inf,0, {}]]
            self.orders_inprocess2 = [[math.inf,0, {}]]
            # the nexteventtimes is a dictionary which contains the next times of each possible event.
            # they are needed to determine which event is executed next (the earliest time of those)
            # Most of them are initialized by the settingdistribution_dict, already with a given distribution, or infinite since they are not yet possible
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
            # amountproduced keeps track of the total amount produced
            self.amountproduced = 0
            # capacities contains the capacities of each production step, imported from the setting distribution dict
            self.capacities = [settingdistibution_dict['capacity staal buigen'],settingdistibution_dict['capacity staal koppelen'],settingdistibution_dict['capacity omhulsel maken']]
            # measures is a dictionary which keeps track of some important measures throughout the simulation
            # measures is updated during each event when something happens which we need to keep track of
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
            # finishedorders contains all orders which are finished, with their orderdict (orderdict is complemented with additional info during simulation)
            self.finishedorders = []

            # measures

    # here the instance is initialized by calling instancezero
    instance = instancezero()

    # the time limit for how long the simulation will run
    timelimit = 4800000

    # in the next while loop the simulation is performed. it keeps running until the time exceeded the time limit
    # first the next event and the time of the next event are determined from the instance.
    # afterwards the instance is updated using the updatevariable function
    while instance.tijd <= timelimit:
        next_event = min(instance.nexteventtimes, key=instance.nexteventtimes.get)
        next_t_event = instance.nexteventtimes[next_event]
        instance = Simulation_event_functions.updatevariables(instance, next_event, next_t_event, settingdistibution_dict)

    # close the disruption measures, if some breakdown or something is still going on, need and end time to evaluate it, so this is the end time of the simulation
    instance.measures = Functions.close_disruption_measures(instance.measures, instance.tijd)

    # Make dataframe of all finished orders and its data
    finished_orders_df = pd.DataFrame(instance.finishedorders)

    #below is used for error checking
    for i in range(len(finished_orders_df)):
        if i not in finished_orders_df.index:
            print('hoiiiiii')
            print(len(finished_orders_df))
            print(i)

    #sommige disruptions kunnen nog niet gesloten zijn, bijvoorbeeld als de order al wel klaar is (omhulsel maken klaar), maar nog niet staal buigen ding heeft afgerond en dan stopt de tijd plots. dam telt t niet als helemaal klaar, dus verwijder uit finished orders
    finished_orders_df = Functions.delete_nonfinished_orders_disruptions(finished_orders_df)

    #below used for error checking
    for i in range(len(finished_orders_df)):
        if i not in finished_orders_df.index:
            print('hoi')
            print(len(finished_orders_df))
            print(i)

    # add three important measures for the finished orders dataframe
    finished_orders_df['total queue time'] = [finished_orders_df['tijd inventory staal buigen'][i] + finished_orders_df['tijd inventory staal koppelen'][i] + finished_orders_df['tijd inventory omhulsel maken'][i] for i in range(len(finished_orders_df))]
    finished_orders_df['total producing time'] = [finished_orders_df['tijd staal buigen'][i] + finished_orders_df['tijd staal koppelen'][i] + finished_orders_df['tijd omhulsel maken'][i] for i in range(len(finished_orders_df))]
    finished_orders_df['lateness'] = [max(finished_orders_df['finish time'][i] - finished_orders_df['deadline order'][i],0) for i in range(len(finished_orders_df))]

    return finished_orders_df, instance.measures, instance.tijd

