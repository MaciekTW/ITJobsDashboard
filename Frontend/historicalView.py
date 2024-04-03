from dash import Dash, dcc, html, Input, Output, callback
from Constans import styles
import datetime
from Backend import historicalBackend
import dash_mantine_components as dmc

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
        ], style={'display': 'flex', 'align-items': 'center', 'backgroundColor': '#312E37', 'padding': '12px',
                  'border-radius': '10px'}),

        html.Div(
            [
                dcc.Graph(id='job-offers-dashboard-1', style={'width': '33%', 'margin': '10px'}),
                dcc.Graph(id='job-offers-dashboard-2', style={'width': '33%', 'margin': '10px'}),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='job-offers-dashboard-5', style={'width': '90%', 'height': '100%'}),
                                html.Div(
                                    [
                                        dmc.Switch(
                                            id="switch-wow",
                                            size="lg",
                                            onLabel="Relative",
                                            offLabel="Absolute",
                                            style={'transform': 'rotate(90deg)'},
                                        )
                                    ], style={'width': '10%', 'backgroundColor': 'white','display': 'flex', 'align-items': 'center'}
                                )
                            ], style={'display': 'flex'}
                        ),
                        dcc.Tabs(id="tabs-operation-modes", value='tab-1-example-graph', children=[
                            dcc.Tab(label='noFluff', value='noFluff'),
                            dcc.Tab(label='justjoinit', value='justjoinit'),
                        ])
                    ], style={'width': '33%', 'margin': '10px'}
                ),
            ], style={'display': 'flex', 'height': '100%'}),
        html.Div(
            [
                dcc.Graph(id='job-offers-dashboard-3', style={'width': '50%', 'margin': '10px'}),
                dcc.Graph(id='job-offers-dashboard-4', style={'width': '50%', 'margin': '10px'}),
            ], style={'display': 'flex'}
        )
    ], style={'backgroundColor': '#797674', 'padding': '12px', 'border-radius': '10px'}),
])
