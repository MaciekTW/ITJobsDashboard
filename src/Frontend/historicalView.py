from dash import Dash, dcc, html, Input, Output, callback
from Constans import styles
import datetime
from Backend import historicalBackend

historicalDiv = html.Div([
    html.H1("Job Offers Analysis Dashboard"),
    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=datetime.datetime(2023, 1, 1),
            end_date=datetime.date.today(),
            display_format='DD-MM-YYYY',
            style={'padding': '4px', 'margin-left': '6px', 'border-radius': '10px'}
        ),
        dcc.Dropdown(['JustJoinIT', 'NoFluffJobs'], ['JustJoinIT', 'NoFluffJobs'], multi=True, id='provider-pickup',
                     style={'padding': '4px', 'margin-left': '6px', 'border-radius': '10px'}),
    ], style={'display': 'flex', 'backgroundColor': '#4C47CE', 'padding': '12px', 'margin': '10px',
              'border-radius': '10px'}),
    dcc.Graph(id='job-offers-dashboard'),
])
