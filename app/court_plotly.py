"""
This file contains the plotly shapes necessary to draw the court.

Referenced this website for drawing court shapes:
https://moderndata.plot.ly/nba-shots-analysis-using-plotly-shapes/

Referenced this website for drawing an arc: (plotly doesn't support svg arc)
https://community.plot.ly/t/plotly-shape-questions/7164/2
"""

import plotly.graph_objects as go
import numpy as np

def my_circle(center, radius, n_points=360):
    t=np.linspace(0, 1, n_points)
    x=center[0]+radius*np.cos(2*np.pi*t)
    y=center[1]+radius*np.sin(2*np.pi*t)
    return x, y

# 3 point line arc is 23.75 feet away from basket
# the arc stretches from 22 degrees to 158 degrees
x,y=my_circle((0,0), 237.5)
three_point_path ='M '+str(x[22])+','+str(y[22])
for k in range(23, 159):
     three_point_path +=' L '+str(x[k])+','+str(y[k])

court_shapes = [
    #hoop
    go.layout.Shape(
                        type="circle",
                        xref="x",
                        yref="y",
                        x0=-7.5,
                        y0=-7.5,
                        x1=7.5,
                        y1=7.5,
                        line=dict(
                            color="Black",
                            width=2
                        )
                    ),
    #backboard
    go.layout.Shape(
                        type="rect",
                        x0=-30,
                        y0=-7.5,
                        x1=30,
                        y1=-6.5,
                        line=dict(
                            color="Black",
                            width=2
                        )
                    ),
    #paint outer box
    go.layout.Shape(
                        type="rect",
                        x0=-80,
                        y0=-47.5,
                        x1=80,
                        y1=142.5,
                        line=dict(
                            color="Black",
                            width=2
                        )
                    ),
    #paint inner box
    go.layout.Shape(
                        type="rect",
                        x0=-60,
                        y0=-47.5,
                        x1=60,
                        y1=142.5,
                        line=dict(
                            color="Black",
                            width=2
                        )
                    ),
    # center circles
    go.layout.Shape(
                        type='circle',
                        xref='x',
                        yref='y',
                        x0='60',
                        y0='482.5',
                        x1='-60',
                        y1='362.5',
                        line=dict(
                            color='Black',
                            width=2
                        )
                    ),
    go.layout.Shape(
                        type='circle',
                        xref='x',
                        yref='y',
                        x0='20',
                        y0='442.5',
                        x1='-20',
                        y1='402.5',
                        line=dict(
                            color='Black',
                            width=2
                        )

    ),
    #free throw circle
    go.layout.Shape(
                        type='circle',
                        xref='x',
                        yref='y',
                        x0='60',
                        y0='200',
                        x1='-60',
                        y1='80',
                        line=dict(
                            color='Black',
                            width=2
                        )
    ),
    #3 point line
    go.layout.Shape(
                        type='line',
                        xref='x',
                        yref='y',
                        x0='-220',
                        y0='-47.5',
                        x1='-220',
                        y1='92.5',
                        line=dict(
                            color='Black',
                            width=2
                        )
    ),
    go.layout.Shape(
                        type='line',
                        xref='x',
                        yref='y',
                        x0='220',
                        y0='-47.5',
                        x1='220',
                        y1='92.5',
                        line=dict(
                            color='Black',
                            width=2
                        )
    ),
    # go.layout.Shape(
    #                     type='path',
    #                     xref='x',
    #                     yref='y',
    #                     path='M -220 92.5 C -70 300, 70 300, 220 92.5',
    #                     line=dict(
    #                         color='Black',
    #                         width=2
    #                     )
    # ),
    go.layout.Shape(
                        type='path',
                        xref='x',
                        yref='y',
                        path= three_point_path,
                        line=dict(
                            color='Black',
                            width=2
                        )
    )
]