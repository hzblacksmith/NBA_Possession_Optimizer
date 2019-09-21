import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from textwrap import dedent as d
import json

import ast

import plotly.graph_objects as go
import pandas as pd

from court_plotly import court_shapes
from helper import *

from player_lookup import ss_id_to_names, nba_id_to_names

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


test_df = pd.read_csv("../ecf_1_shot.csv")


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
                                {'label': 'Cle vs Bos 4', 'value': 'Cle_bos_4'},
                                {'label': 'Cle vs Bos 5', 'value': 'Cle_bos_5'},
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
                            style = {
                                'width': '100%'
                            }
                        )
                    ]
                ),
                html.Div(
                    id = 'interface-bottom',
                    children = [
                        html.Div(
                            id = 'actual_player',
                            children = [
                                html.Img(id = 'actual_player_img',
                                        style = {
                                            'width': '80px',
                                            'height': '80px'
                                        }),
                                html.Div(
                                    id = 'actual_player_name',
                                ),
                                dcc.Graph(
                                    id = 'actual_player_graph'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
    



@app.callback(
    Output('main-graph','figure'),
    [Input('game-select-dropdown', 'value'),
     Input('possession-select-dropdown', 'value')]
)
def update_main_graph(game_value, possession_value):

    # initializaion: only draw the court
    if (game_value == "Null Game" or possession_value == "Null"):
        return {
            'layout' : go.Layout(
                    # draw the court
                    shapes = court_shapes,
                    xaxis=dict(showgrid=False,
                               range=[-300,300],
                               showline=False,
                               zeroline=False,
                               showticklabels=False),
                    yaxis=dict(showgrid=False,
                               range=[422.5,-47.5],
                               showline=False,
                               zeroline=False,
                               showticklabels=False),
                    margin=go.layout.Margin(
                        l=0,
                        r=0,
                        b=0,
                        t=0,
                    ),
                )
        }
    
    main_df = test_df[test_df['possession_index'] == int(possession_value)]

    player_routes = get_player_routes(main_df)
    # main_df = pd.read_csv("Data_supplement/Shot_zones_reg_season/bos_shot_1617.csv")

    return {
        'data' : [go.Scatter(
                    x = player_routes[player_id]['X'],
                    y = player_routes[player_id]['Y'],
                    customdata = [player_id] * len(player_routes[player_id]['X']),
                    mode='lines'
                ) for player_id in player_routes],
        'layout' : go.Layout(
            # draw the court
            shapes = court_shapes,
            xaxis=dict(showgrid=False,
                        range=[-300,300],
                        showline=False,
                        zeroline=False,
                        showticklabels=False),
            yaxis=dict(showgrid=False,
                        range=[422.5,-47.5],
                        showline=False,
                        zeroline=False,
                        showticklabels=False),
            margin=go.layout.Margin(
                l=0,
                r=0,
                b=0,
                t=0,
            ),
            
        )
    }

@app.callback(
    [Output('actual_player_img', 'src'),
     Output('actual_player_name', 'children')],
    [Input('main-graph', 'hoverData')])
def display_hover_data(hoverData):
    if hoverData is None:
        raise PreventUpdate
    player_ss_id = hoverData['points'][0]['customdata']
    try:
        player_name = ss_id_to_names[player_ss_id]
    except:
        player_name = "Unknown"
    print(player_name)
    if player_name == "Unknown":
        return (app.get_asset_url('Pictures/question.png'),
                "Unknown Player"
                )
    else:
        return (app.get_asset_url('Pictures/{}.png'.format(player_name)),
                "{}".format(player_name)
                )

if __name__ == '__main__':
    app.run_server(debug=True)