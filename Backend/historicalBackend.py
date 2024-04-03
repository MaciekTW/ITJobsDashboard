from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime
from Backend import dataLoader


@callback(
    [Output('job-offers-dashboard-1', 'figure'),
     Output('job-offers-dashboard-2', 'figure'),
     Output('job-offers-dashboard-3', 'figure'),
     Output('job-offers-dashboard-4', 'figure'),
     Output('job-offers-dashboard-5', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('provider-pickup', 'value'),
     Input('tabs-operation-modes', 'value'),
     Input("switch-wow", "checked")]
)
def update_dashboard(start_date, end_date, value,tab,checked):
    start_date = datetime.datetime.fromisoformat(start_date).date()
    end_date = datetime.datetime.fromisoformat(end_date).date()
    dataLoaderInstance = dataLoader.DataLoader()
    figures = {}
    figures["fig1"] = figures.get("fig1", go.Figure())
    figures["fig2"] = figures.get("fig2", go.Figure())
    figures["fig3"] = figures.get("fig3", go.Figure())
    figures["fig4"] = figures.get("fig4", go.Figure())
    figures["fig5"] = figures.get("fig5", go.Figure())

    for provider in value:
        combinerOffersCount = dataLoaderInstance.getOffersCount(provider, [start_date, end_date])

        figures["fig1"].add_trace(
            go.Scatter(x=combinerOffersCount["Data"], y=combinerOffersCount["count"], mode='lines+markers',
                       name=f'{provider}'))
        figures["fig1"].update_layout(title='Total Job Offers - noFluffjobs', xaxis_title='Date', yaxis_title='Count',legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

        specifiedTechnologyCount = dataLoaderInstance.getOffersCountPerRequirement(provider, 'c++',[start_date, end_date])

        figures["fig2"] .add_trace(
            go.Scatter(x=specifiedTechnologyCount["Data"], y=specifiedTechnologyCount["count"], mode='lines+markers',
                       name=f'{provider}'))

        figures["fig2"] .update_layout(title='Total Jobs Offers with c++ requirement', xaxis_title='Date', yaxis_title='Count',legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

        for level in ["senior","mid", "junior", "Expert","Trainee"]:
            levelCount = dataLoaderInstance.getOffersCountPerLevel(provider,level,[start_date, end_date])
            figures["fig3"].add_trace(
                go.Scatter(x=levelCount["Data"], y=levelCount["count"], mode='lines+markers',
                           name=f'{provider} - {level} offers'))

        figures["fig3"].update_layout(title=f'Offers per seniority', xaxis_title='Date', yaxis_title='Count')

    UOPSalaries=dataLoaderInstance.combine_dataframes(dataLoader.DataLoader().getProvidersLabels()[1])

    for level in UOPSalaries['Level'].unique():
        df_level = UOPSalaries[UOPSalaries['Level'] == level]
        figures["fig4"].add_trace(go.Scatter(x=df_level['Date'], y=df_level['UOP'], mode='lines', name=level))

    figures["fig4"].update_layout(title="Median salary per seniority (UOP)", xaxis_title='Date', yaxis_title='Count',legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))


    if tab == 'noFluff':
        provider='noFluff'
        modeCount = dataLoaderInstance.getOffersCountPerOperationMode2(provider,True,[start_date, end_date])
        if checked:
            y=modeCount["Ratio"]
        else:
            y=modeCount["count"]

        figures["fig5"].add_trace(
            go.Scatter(x=modeCount["Data"], y=y, mode='lines+markers',
                       name=f'Remote offers'))

        modeCount = dataLoaderInstance.getOffersCountPerOperationMode2(provider,False,[start_date, end_date])
        if checked:
            y=modeCount["Ratio"]
        else:
            y=modeCount["count"]
        figures["fig5"].add_trace(
            go.Scatter(x=modeCount["Data"], y=y, mode='lines+markers',
                       name=f'Office offers'))
    else:
        provider='justjoinit'
        for mode in ["remote","hybrid", "office"]:
            modeCount = dataLoaderInstance.getOffersCountPerOperationMode(provider,mode,[start_date, end_date])
            if checked:
                y=modeCount["Ratio"]
            else:
                y=modeCount["count"]

            figures["fig5"].add_trace(
                go.Scatter(x=modeCount["Data"], y=y, mode='lines+markers',
                           name=f'{mode} offers'))


    figures["fig5"].update_layout(title="WoW over time", xaxis_title='Date', yaxis_title='Count',legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))



    return figures["fig1"], figures["fig2"], figures["fig3"], figures["fig4"], figures["fig5"]
