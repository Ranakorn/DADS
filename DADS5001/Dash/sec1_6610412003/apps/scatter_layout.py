# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from app import app

df = pd.read_csv('https://github.com/chris1610/pbpython/blob/master/data/cereal_data.csv?raw=True')

fig1 = px.scatter(df,
                x='sugars',
                y='rating',
                hover_name='name',
                title='Cereal ratings vs. sugars')

layout = html.Div(children=[

        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph1',
            figure=fig1
        ),

        dcc.Dropdown(['sugars', 'sodium', 'fiber'], 'sugars', id='dropdown1')
    
    ], style={'padding': 10, 'flex': 1})

@app.callback(
    Output('example-graph1', 'figure'),
    Input('dropdown1', 'value'))
def update_fig1(x):
    
    fig1 = px.scatter(df,
                x=x,
                y="rating",
                hover_name='name',
                title= "Rating" + ' VS '+x)
    #fig1.update_layout(transition_duration=500)

    return fig1
