import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
import pandas as pd

from court_plotly import court_shapes

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(
    id = 'main',
    children=[
        html.Div(
            id = 'info-select',
            children = [
                html.Div(
                    id = 'info-select-sub',
                    children = [
                        html.P(
                            children='POSSESSION OPTIMIZER',
                            style = {
                                'letter-spacing': 2.1,
                                'font-weight': 700,
                                'font-size': '170%',
                            }
                        ),
                        dcc.Dropdown(
                            id='game-select-dropdown',
                            options=[
                                {'label': 'Cle vs Bos 1', 'value': 'Cle_bos_1'},
                                {'label': 'Cle vs Bos 2', 'value': 'Cle_bos_2'},
                                {'label': 'Cle vs Bos 3', 'value': 'Cle_bos_3'},
                            ],
                            placeholder='Select Game',
                            value='Null Game',
                            searchable=False,
                        ),
                        dcc.Dropdown(
                            id='possession-select-dropdown',
                            options=[
                                {'label': '{}'.format(i), 'value': i} for i in range(100)
                            ],
                            placeholder='Select Possession',
                            value='Null',
                            searchable=False,
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id = 'interface',
            children = [
                html.Div(
                    id = 'interface-top',
                    children = [
                        dcc.Graph(
                            id='main-graph',
                        )
                    ]
                ),
                html.Div(
                    id = 'interface-bottom',
                    children = [
                        dcc.Graph(
                            id='main-graph-2',
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output('main-graph','figure'),
    [Input('game-select-dropdown', 'value')]
)
def update_main_graph(value):
    # initializaion: only draw the court
    if (value == "Null Game"):
        return {
            'layout' : go.Layout(
                    xaxis=dict(showgrid=False,
                               range=[-300,300]),
                    yaxis=dict(showgrid=False,
                               range=[422.5,-47.5]),
                    # draw the court
                    shapes = court_shapes
                )
        }

    main_df = pd.read_csv("Data_supplement/Shot_zones_reg_season/bos_shot_1617.csv")


    return {
        'data' : [go.Scatter(
                    x = main_df['LOC_X'],
                    y = main_df['LOC_Y'],
                    mode='markers'
                )],
        'layout' : go.Layout(
            xaxis=dict(showgrid=False,
                        range=[-300,300]),
            yaxis=dict(showgrid=False,
                        range=[422.5,-47.5]),
            # draw the court
            shapes = court_shapes
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)