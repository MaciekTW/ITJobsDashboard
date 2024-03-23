from dash import Dash, dcc, html, Input, Output, callback
from Constans import styles

mainDiv =  html.Div(children=[
    html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Historic Data', value='historic-data', style=styles.tab_style, selected_style=styles.tab_selected_style),
            dcc.Tab(label='Today Data', value='today-data', style=styles.tab_style, selected_style=styles.tab_selected_style),
            dcc.Tab(label='Offer specific', value='offer-specific', style=styles.tab_style, selected_style=styles.tab_selected_style)
        ], style=styles.tabs_styles),
        html.Div(id='tabs-content-inline')
    ])
])

