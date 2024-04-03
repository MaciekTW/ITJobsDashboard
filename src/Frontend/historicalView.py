from dash import Dash, dcc, html, Input, Output, callback
from Constans import styles
import datetime
from Backend import historicalBackend

historicalDiv = html.Div([
    html.Div([
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=datetime.datetime(2023, 1, 1),
                end_date=datetime.date.today(),
                display_format='DD-MM-YYYY',
                style={'padding': '4px', 'margin-left': '6px', 'border-radius': '10px'}
            ),
            dcc.Dropdown(['justjoinit', 'noFluff'], ['justjoinit', 'noFluff'], multi=True, id='provider-pickup',
                         style={'padding': '4px', 'margin-left': '6px', 'border-radius': '10px'}),
        ], style={'display': 'flex', 'backgroundColor': '#312E37', 'padding': '12px', 'border-radius': '10px'}),

        html.Div([
            dcc.Graph(id='job-offers-dashboard-1', style={'width': '33%', 'padding': '6px', 'margin': '10px'}),
            dcc.Graph(id='job-offers-dashboard-2', style={'width': '33%', 'padding': '6px', 'margin': '10px'}),
            html.Div([
                dcc.Graph(id='job-offers-dashboard-5'),
                dcc.Tabs(id="tabs-operation-modes", value='tab-1-example-graph', children=[
                    dcc.Tab(label='noFluff', value='noFluff'),
                    dcc.Tab(label='justjoinit', value='justjoinit'),
                ])
            ], style={'width': '33%', 'padding': '6px', 'margin': '10px'}),
        ], style={'display': 'flex'}),
        html.Div([
            dcc.Graph(id='job-offers-dashboard-3', style={'width': '50%', 'padding': '6px', 'margin': '10px'}),
            dcc.Graph(id='job-offers-dashboard-4', style={'width': '50%', 'padding': '6px', 'margin': '10px'}),
        ], style={'display': 'flex'})
    ], style={'backgroundColor': '#797674', 'padding': '12px', 'border-radius': '10px'}),
])
