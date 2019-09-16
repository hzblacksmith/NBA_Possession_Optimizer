import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
import pandas as pd

from court_plotly import court_shapes

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


shotchart = pd.read_csv("Data_supplement/Shot_zones/bos_shot_1617.csv")

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}



app.layout = html.Div(
    style={'backgroundColor': colors['background'],
            'marginLeft': 20, 'marginRight': 20, 'marginTop': 20, 'marginBottom': 20,
            'border-radius': 10
          },
    children=[
        html.H1(
            children='Possession Optimizer for Coaches',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.Graph(
            id='main-graph',
            style = {
                'width': '50%'
            },
            figure = go.Figure(
                data = go.Scatter(
                    x = shotchart['LOC_X'],
                    y = shotchart['LOC_Y'],
                    mode='markers'
                ),
                layout=go.Layout(
                    xaxis=dict(showgrid=False,
                               range=[-300,300]),
                    yaxis=dict(showgrid=False,
                               range=[422.5,-47.5]),
                    # draw the court
                    shapes = court_shapes
                )
            )
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)