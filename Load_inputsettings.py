'''
This file reads and returns the input data in a dictionary by hand as settingdistibution_dict
If the input data needs to be changed, here the adjustments have to be made (and in some other functions such as get orderinfo)
'''

def load_settings():
    ############## SETTINGS

    # capacity of the schakels
    capacity_staalbuigen = 10
    capacity_staalkoppelen = 10
    capacity_omhulselmaken = 10

    # distribution binnenkomen van orders
    Mean_ordertime = 800
    Mean_ordersize = 2
    stdev_ordertime = 1
    stdev_ordersize = 1

    # deadline orders
    Mean_order_deadline = 750
    stdev_order_deadline = 30

    # high priority chance
    high_priority_chance = 0.03

    # supply (manual stock level determined)
    supply_order_interval_time = 24000
    Mean_supplytime_stalen_stangen = 480
    stdev_supplytime_stalen_stangen = 20
    # eorderpoint_stalenstangen = 20

    Mean_supplytime_koppeldraad = 480
    stdev_supplytime_koppeldraad = 20

    Mean_supplytime_stuffing = 480
    stdev_supplytime_stuffing = 20

    # suggested reorder up to point of raw materials
    reorder_upto_point_stalenstangen = 750
    reorder_upto_point_koppeldraad = 325
    reorder_upto_point_softstuffing = 50
    reorder_upto_point_mediumstuffing = 50
    reorder_upto_point_hardstuffing = 50

    # # manual reorder up to point of raw materials
    # reorder_upto_point_stalenstangen = 1700
    # reorder_upto_point_koppeldraad = 750
    # reorder_upto_point_softstuffing = 100
    # reorder_upto_point_mediumstuffing = 100
    # reorder_upto_point_hardstuffing = 100

    stdev_order_quantity_percentage_of_quantity = 0.01
    # distributions processes
    Mean_process0time = 720
    Mean_process1time = 650
    Mean_process2time = 700
    stdev_process0time = 20
    stdev_process1time = 40
    stdev_process2time = 20

    # schakel breakdowns
    Mean_schakel_staalbuigen_breakdown = 24000
    Mean_schakel_staalkoppelen_breakdown = 24000
    Mean_schakel_omhulselmaken_breakdown = 24000
    Mean_fix_staalbuigen_breakdown = 480
    Mean_fix_staalkoppelen_breakdown = 480
    Mean_fix_omhulselmaken_breakdown = 480

    # # suggested safety stocks sub assemblies
    # SS_gebogen_stangen = 75
    # SS_gekoppeld_eenpersoons = 10
    # SS_gekoppeld_twijfelaar =  10
    # SS_gekoppeld_queensize =  10
    # SS_gekoppeld_kingsize = 10

    # Manual safety stocks sub assemblies
    SS_gebogen_stangen = 100
    SS_gekoppeld_eenpersoons = 10
    SS_gekoppeld_twijfelaar = 10
    SS_gekoppeld_queensize = 10
    SS_gekoppeld_kingsize = 10

    # wanted succes rate
    wantedsuccesrate = 0.9

    settingdistibution_dict = {'order time mean': Mean_ordertime, 'order time stdev': stdev_ordertime,
                               'order size mean': Mean_ordersize, 'order size stdev': stdev_ordersize,
                               'supply interval order': supply_order_interval_time,
                               'mean supply time stalen stangen': Mean_supplytime_stalen_stangen,
                               'stdev supply time stalen stangen': stdev_supplytime_stalen_stangen,
                               'reorder upto stalen stangen': reorder_upto_point_stalenstangen,
                               'mean supply time koppeldraad': Mean_supplytime_koppeldraad,
                               'stdev supply time koppeldraad': stdev_supplytime_koppeldraad,
                               'reorder upto koppeldraad': reorder_upto_point_koppeldraad,
                               'mean supply time stuffing': Mean_supplytime_stuffing,
                               'stdev supply time stuffing': stdev_supplytime_stuffing,
                               'reorder upto soft stuffing': reorder_upto_point_softstuffing,
                               'reorder upto medium stuffing': reorder_upto_point_mediumstuffing,
                               'reorder upto hard stuffing': reorder_upto_point_hardstuffing,
                               'mean staal buigen time': Mean_process0time,
                               'mean staal koppelen time': Mean_process1time,
                               'mean omhulsel maken time': Mean_process2time,
                               'stdev staal buigen time': stdev_process0time,
                               'stdev staal koppelen time': stdev_process1time,
                               'stdev omhulsel maken time': stdev_process2time,
                               'mean staal buigen breakdown': Mean_schakel_staalbuigen_breakdown,
                               'mean staal koppelen breakdown': Mean_schakel_staalkoppelen_breakdown,
                               'mean omhulsel maken breakdown': Mean_schakel_omhulselmaken_breakdown,
                               'mean fix staal buigen breakdown': Mean_fix_staalbuigen_breakdown,
                               'mean fix staal koppelen breakdown': Mean_fix_staalkoppelen_breakdown,
                               'mean fix omhulsel maken breakdown': Mean_fix_omhulselmaken_breakdown,
                               'capacity staal buigen': capacity_staalbuigen,
                               'capacity staal koppelen': capacity_staalkoppelen,
                               'capacity omhulsel maken': capacity_omhulselmaken,
                               'stddev order hoeveelheid als percentage van quantity': stdev_order_quantity_percentage_of_quantity,
                               'SS gebogen stangen': SS_gebogen_stangen,
                               'SS gekoppeld eenpersoons': SS_gekoppeld_eenpersoons,
                               'SS gekoppeld twijfelaar': SS_gekoppeld_twijfelaar,
                               'SS gekoppeld queensize': SS_gekoppeld_queensize,
                               'SS gekoppeld kingsize': SS_gekoppeld_kingsize,
                               'mean deadline order': Mean_order_deadline,
                               'stdev deadline order': stdev_order_deadline,
                               'high priority chance': high_priority_chance,
                               'wanted succes rate': wantedsuccesrate,
                               }

    #settingdistibution_dict = Functions.calculateSafetyStocks(settingdistibution_dict)

    return settingdistibution_dict