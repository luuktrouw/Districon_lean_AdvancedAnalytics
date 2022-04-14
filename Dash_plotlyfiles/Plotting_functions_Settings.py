from dash import dash_table

def make_fig_editablespeelveldprocessschakels(settingdistibution_dict):
    headercontent = ['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev']

    tablecontent = [['doorlooptijd staal buigen', 'Normal', 'no', settingdistibution_dict['mean staal buigen time'], settingdistibution_dict['stdev staal buigen time']],
                        ['doorlooptijd staal koppelen', 'Normal', 'no', settingdistibution_dict['mean staal koppelen time'], settingdistibution_dict['stdev staal koppelen time']],
                        ['doorlooptijd omhulsel maken', 'Normal', 'no', settingdistibution_dict['mean omhulsel maken time'], settingdistibution_dict['stdev omhulsel maken time']],
                        ['capacity staal buigen', 'Deterministic', 'no',settingdistibution_dict['capacity staal buigen'], 'Nan' ],
                        ['capacity staal koppelen', 'Deterministic', 'no', settingdistibution_dict['capacity staal koppelen'], 'Nan'],
                        ['capacity omhulsel maken', 'Deterministic', 'no', settingdistibution_dict['capacity omhulsel maken'], 'Nan'],
                        ]

    fig_table_speelveldprocessschakels = dash_table.DataTable(id = 'settingsprocessschakels',
                                                     columns = [{'name': headercontent[i], 'id': headercontent[i]} for i in range(len(headercontent))],
                                                     data = [{headercontent[j]: tablecontent[i][j]
                                                              for j in range(len(tablecontent[i]))}
                                                             for i in range(len(tablecontent))],
                                                     editable = True,
                                                     style_cell={'textAlign': 'left',
                                                                 'font-family':'sans-serif'},
                                                     style_data={
                                                         'color': 'black',
                                                         'backgroundColor': 'white',
                                                         'whiteSpace': 'normal',
                                                         'height': 'auto',
                                                     },
                                                     style_header={
                                                         'backgroundColor': 'rgb(210, 210, 210)',
                                                         'color': 'black',
                                                         'fontWeight': 'bold',
                                                         'textAlign': 'left'
                                                     },
                                                     style_data_conditional=[
                                                         {
                                                             'if': {'row_index': 'odd'},
                                                             'backgroundColor': 'rgb(220, 220, 220)',
                                                         }
                                                     ],
                                                     page_size=6
                                                     )

    return fig_table_speelveldprocessschakels

def make_fig_editablespeelveldbreakdowns(settingdistibution_dict):
    headercontent = ['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev']

    tablecontent = [['tijd tot nieuwe breakdown staal buigen', 'Exponential', 'no', settingdistibution_dict['mean staal buigen breakdown'], 'Nan'],
                        ['tijd tot nieuwe breakdown staal koppelen', 'Exponential', 'no', settingdistibution_dict['mean staal koppelen breakdown'], 'Nan'],
                        ['tijd tot nieuwe breakdown omhulsel maken', 'Exponential', 'no', settingdistibution_dict['mean omhulsel maken breakdown'], 'Nan'],
                        ['tijd breakdown fixen staal buigen', 'Exponential', 'no', settingdistibution_dict['mean fix staal buigen breakdown'], 'Nan'],
                        ['tijd breakdown fixen staal koppelen', 'Exponential', 'no', settingdistibution_dict['mean fix staal koppelen breakdown'], 'Nan'],
                        ['tijd breakdown fixen omhulsel maken', 'Exponential', 'no',settingdistibution_dict['mean fix omhulsel maken breakdown'] , 'Nan'],
                        ]

    fig_table_speelveldbreakdowns = dash_table.DataTable(id = 'settingsbreakdowns',
                                                     columns = [{'name': headercontent[i], 'id': headercontent[i]} for i in range(len(headercontent))],
                                                     data = [{headercontent[j]: tablecontent[i][j]
                                                              for j in range(len(tablecontent[i]))}
                                                             for i in range(len(tablecontent))],
                                                     editable = True,
                                                     style_cell={'textAlign': 'left',
                                                                 'font-family':'sans-serif'},
                                                     style_data={
                                                         'color': 'black',
                                                         'backgroundColor': 'white',
                                                         'whiteSpace': 'normal',
                                                         'height': 'auto',
                                                     },
                                                     style_header={
                                                         'backgroundColor': 'rgb(210, 210, 210)',
                                                         'color': 'black',
                                                         'fontWeight': 'bold',
                                                         'textAlign': 'left'
                                                     },
                                                     style_data_conditional=[
                                                         {
                                                             'if': {'row_index': 'odd'},
                                                             'backgroundColor': 'rgb(220, 220, 220)',
                                                         }
                                                     ],
                                                     page_size=6
                                                     )

    return fig_table_speelveldbreakdowns

def make_fig_editablespeelveldorders(settingdistibution_dict):
    headercontent = ['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev']

    tablecontent = [['aankomst nieuwe orders', 'Exponential', 'no', settingdistibution_dict['order time mean'], 'Nan'],
                        ['order grootte nieuwe orders', 'Normal', 'no',settingdistibution_dict['order size mean'],settingdistibution_dict['order size stdev'] ],
                        ['new order deadlines', 'normal', 'no', settingdistibution_dict['mean deadline order'],settingdistibution_dict['stdev deadline order']],
                        ]

    fig_table_speelveldorders = dash_table.DataTable(id = 'settingsorders',
                                                     columns = [{'name': headercontent[i], 'id': headercontent[i]} for i in range(len(headercontent))],
                                                     data = [{headercontent[j]: tablecontent[i][j]
                                                              for j in range(len(tablecontent[i]))}
                                                             for i in range(len(tablecontent))],
                                                     editable = True,
                                                     style_cell={'textAlign': 'left',
                                                                 'font-family':'sans-serif'},
                                                     style_data={
                                                         'color': 'black',
                                                         'backgroundColor': 'white',
                                                         'whiteSpace': 'normal',
                                                         'height': 'auto',
                                                     },
                                                     style_header={
                                                         'backgroundColor': 'rgb(210, 210, 210)',
                                                         'color': 'black',
                                                         'fontWeight': 'bold',
                                                         'textAlign': 'left'
                                                     },
                                                     style_data_conditional=[
                                                         {
                                                             'if': {'row_index': 'odd'},
                                                             'backgroundColor': 'rgb(220, 220, 220)',
                                                         }
                                                     ],
                                                     page_size=6
                                                     )

    return fig_table_speelveldorders

def make_fig_editablespeelveldsupply(settingdistibution_dict):
    headercontent = ['Proces stap', 'Verdeling', 'based on historical data?', 'Mean', 'stdev']

    tablecontent = [
        ['reorder per tijdunits', 'Deterministic', 'no', settingdistibution_dict['supply interval order'], 'Nan'],
        ['reorder up to point stalen stangen', 'Deterministic', 'no',
         settingdistibution_dict['reorder upto stalen stangen'], 'Nan'],
        ['reorder up to point koppeldraad', 'Deterministic', 'no', settingdistibution_dict['reorder upto koppeldraad'],
         'Nan'],
        ['reorder up to point soft stuffing', 'Deterministic', 'no',
         settingdistibution_dict['reorder upto soft stuffing'], 'Nan'],
        ['reorder up to point medium stuffing', 'Deterministic', 'no',
         settingdistibution_dict['reorder upto medium stuffing'], 'Nan'],
        ['reorder up to point hard stuffing', 'Deterministic', 'no',
         settingdistibution_dict['reorder upto hard stuffing'], 'Nan'],
        ['Component Safety Stock gebogen stangen', 'Deterministic', 'no', settingdistibution_dict['SS gebogen stangen'],
         'Nan'],
        ['Component Safety Stock gekoppeld eenpersoons', 'Deterministic', 'no',
         settingdistibution_dict['SS gekoppeld eenpersoons'], 'Nan'],
        ['Component Safety Stock gekoppeld twijfelaar', 'Deterministic', 'no',
         settingdistibution_dict['SS gekoppeld twijfelaar'], 'Nan'],
        ['Component Safety Stock gekoppeld queensize', 'Deterministic', 'no',
         settingdistibution_dict['SS gekoppeld queensize'], 'Nan'],
        ['Component Safety Stock gekoppeld kingsize', 'Deterministic', 'no',
         settingdistibution_dict['SS gekoppeld kingsize'], 'Nan'],
        ['supply time stalen stangen', 'normal', 'no', settingdistibution_dict['mean supply time stalen stangen'],
         settingdistibution_dict['stdev supply time stalen stangen']],
        ['supply time koppeldraad', 'normal', 'no', settingdistibution_dict['mean supply time koppeldraad'],
         settingdistibution_dict['stdev supply time koppeldraad']],
        ['supply time stuffing', 'normal', 'no', settingdistibution_dict['mean supply time stuffing'],
         settingdistibution_dict['stdev supply time stuffing']],
        ['supply quantity error (%stdev)', 'normal', 'no', 'Same as ordered quantity',
         settingdistibution_dict['stddev order hoeveelheid als percentage van quantity']],
        ]

    fig_table_speelveldsupply = dash_table.DataTable(id = 'settingssupply',
                                                     columns = [{'name': headercontent[i], 'id': headercontent[i]} for i in range(len(headercontent))],
                                                     data = [{headercontent[j]: tablecontent[i][j]
                                                              for j in range(len(tablecontent[i]))}
                                                             for i in range(len(tablecontent))],
                                                     editable = True,
                                                     style_cell={'textAlign': 'left',
                                                                 'font-family':'sans-serif'},
                                                     style_data={
                                                         'color': 'black',
                                                         'backgroundColor': 'white',
                                                         'whiteSpace': 'normal',
                                                         'height': 'auto',
                                                     },
                                                     style_header={
                                                         'backgroundColor': 'rgb(210, 210, 210)',
                                                         'color': 'black',
                                                         'fontWeight': 'bold',
                                                         'textAlign': 'left'
                                                     },
                                                     style_data_conditional=[
                                                         {
                                                             'if': {'row_index': 'odd'},
                                                             'backgroundColor': 'rgb(220, 220, 220)',
                                                         }
                                                     ],
                                                     page_size=6
                                                     )

    # fig_table_speelveldsupply = go.Figure(data=[go.Table(
    #     header=dict(values=headercontent,
    #                 line_color='darkslategray',
    #                 fill_color='lightskyblue',
    #                 align='left'),
    #     cells=dict(values=[[tablecontent[i][j] for i in range(len(tablecontent))] for j in range(len(headercontent))],
    #                line_color='darkslategray',
    #                fill_color='lightcyan',
    #                align='left')),
    # ],
    #     layout_width=500
    # )

    return fig_table_speelveldsupply


def get_Settings_figures(settingdistibution_dict):
    Settings_fig_dict = {}

    Settings_fig_dict['editable process schakels'] = make_fig_editablespeelveldprocessschakels(settingdistibution_dict)
    Settings_fig_dict['editable breakdowns'] = make_fig_editablespeelveldbreakdowns(settingdistibution_dict)
    Settings_fig_dict['editable orders'] = make_fig_editablespeelveldorders(settingdistibution_dict)
    Settings_fig_dict['editable supply'] = make_fig_editablespeelveldsupply(settingdistibution_dict)

    return Settings_fig_dict