from dash import Dash, dcc, html, Input, Output, callback
from Constans import styles
import datetime
from Backend import historicalBackend

historicalDiv = html.Div([
    html.H1("Job Offers Analysis Dashboard"),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=datetime.datetime(2023, 1, 1),
        end_date=datetime.datetime(2023, 12, 31),
        display_format='DD-MM-YYYY'
    ),
    dcc.Graph(id='job-offers-dashboard'),
])