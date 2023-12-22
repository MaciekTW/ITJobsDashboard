from dash import Dash, dcc, html, Input, Output, callback
from Frontend import historicalView

@callback(Output('tabs-content-inline', 'children'),
          Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'historic-data':
        return historicalView.historicalDiv
    elif tab == 'today-data':
        return html.Div([
            html.H3('Today Data')
        ])
    elif tab == 'offer-specific':
        return html.Div([
            html.H3('Offer specific')
        ])
    else:
        return historicalView.historicalDiv