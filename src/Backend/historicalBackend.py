from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime
from Backend import dataLoader


@callback(
    Output('job-offers-dashboard', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('provider-pickup', 'value')]
)
def update_dashboard(start_date, end_date,value):
    start_date = datetime.datetime.fromisoformat(start_date).date()
    end_date = datetime.datetime.fromisoformat(end_date).date()
    dashboard = make_subplots(rows=2, cols=2, subplot_titles=(
    'Total Job Offers Over Time', 'C++ Job Offers Over Time','Total Jobs Offer per level over time', 'Average Salary per level'))
    dataLoaderInstance = dataLoader.DataLoader()

    for provider in value:
        print(provider)
        combinerOffersCount = dataLoaderInstance.getOffersCount(provider, [start_date, end_date])

        dashboard.add_trace(
            go.Scatter(x=combinerOffersCount["Data"], y=combinerOffersCount["count"], mode='lines+markers',
                       name='Total Job Offers - noFluffjobs'), row=1, col=1)

        specifiedTechnologyCount = dataLoaderInstance.getOffersCountPerRequirement(provider, 'c++',[start_date, end_date])
        dashboard.add_trace(
            go.Scatter(x=specifiedTechnologyCount["Data"], y=specifiedTechnologyCount["count"], mode='lines+markers',
                       name='Total Jobs Offers in backend category'), row=1, col=2)

        for level in ["senior","mid", "junior", "Expert","Trainee"]:
            levelCount = dataLoaderInstance.getOffersCountPerLevel(provider,level,[start_date, end_date])
            dashboard.add_trace(
                go.Scatter(x=levelCount["Data"], y=levelCount["count"], mode='lines+markers',
                           name=f'{provider} Total Offers for {level}'), row=2, col=1)


    UOPSalaries=dataLoaderInstance.combine_dataframes(dataLoader.DataLoader().getProvidersLabels()[1])
    dataLoaderInstance.getOffersCountPerRequirement(dataLoader.DataLoader().getProvidersLabels()[1], ''"c++"'',[start_date, end_date])

    for level in UOPSalaries['Level'].unique():
        # Filtracja danych dla danego poziomu
        df_level = UOPSalaries[UOPSalaries['Level'] == level]

        # Dodawanie śladu dla danego poziomu
        dashboard.add_trace(go.Scatter(x=df_level['Date'], y=df_level['UOP'], mode='lines', name=level), row=2, col=2)


    dashboard.update_layout(height=900, showlegend=True)

    return dashboard
