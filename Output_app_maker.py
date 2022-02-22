import dash
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import main_simulation

#https://www.youtube.com/watch?v=hSPmj7mK6ng

fig_total_thoughout_time, fig_queue_time_staal_buigen, fig_queue_time_staal_koppelen, fig_queue_time_omhulsel_maken, fig_total_queue_time = main_simulation.runsimulation()

app = dash.Dash(__name__)

app.layout = html.Div([
            html.H1("Simulation results with the given settings", style={'text-align':'center'}),
            dcc.Dropdown(id = 'slct_year', options = [{'label': '2015', 'value': 2015},{'label': '2016', 'value': 2016},
                          {'label': '2017', 'value': 2017},{'label': '2018', 'value': 2018}], multi = False,
                        value = 2015, style = {'width':'40%'}),
            html.Div(id = 'output_container', children = []),
            html.Br(),
            dcc.Graph(style = {'height': 300, 'width': 30000},id = 'output1'),
            dcc.Graph(style = {'height': 300, 'width': 30000},id = 'my_bee_map', figure = {})



],style={'display': 'flex', 'flex-direction': 'row'})

@app.callback([Output(component_id= 'output1', component_property= 'figure') , Output(component_id='my_bee_map', component_property='figure')],
              [Input(component_id='slct_year', component_property= 'value')])

def update_graph(option_slctd):
    if option_slctd == 2015:
        fig = fig_total_queue_time
    elif option_slctd == 2016:
        fig = fig_total_thoughout_time

    return fig_queue_time_omhulsel_maken, fig

if __name__ == '__main__':
    app.run_server()

'''
fig = go.Figure(go.Histogram(x = finished_orders_df["total process time"]))
fig.add_trace(go.Histogram(x = finished_orders_df["total process time"]))
fig.update_layout(barmode = 'stack')
fig.show()

labels = [ 'EEN', 'TWEE']
buttons = []
for i, label in enumerate(labels):
    visibility = [i==j for j in range(len(labels))]
    button = dict(
                 label =  label,
                 method = 'update',
                 args = [{'visible': visibility},
                     {'title': label}])
    buttons.append(button)

updatemenus = list([
    dict(active=-1,
         x=-0.15,
         buttons=buttons
    )
])

fig['layout']['title'] = 'Title'
fig['layout']['showlegend'] = True
fig['layout']['updatemenus'] = updatemenus
fig.show()
'''