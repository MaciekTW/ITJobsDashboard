from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime
from Backend import dataLoader


@callback(
    Output('job-offers-dashboard', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_dashboard(start_date, end_date):
    start_date = datetime.datetime.fromisoformat(start_date).date()
    end_date = datetime.datetime.fromisoformat(end_date).date()

    dashboard = make_subplots(rows=3, cols=1, subplot_titles=(
    'Total Job Offers Over Time', 'C++ Job Offers Over Time', 'Average Salary per level'))
    dataLoaderInstance = dataLoader.DataLoader()


    for provider in dataLoader.DataLoader().getProvidersLabels():
        combinerOffersCount = dataLoaderInstance.getOffersCount(provider, [start_date, end_date])

        dashboard.add_trace(
            go.Scatter(x=combinerOffersCount["Data"], y=combinerOffersCount["count"], mode='lines+markers',
                       name='Total Job Offers - noFluffjobs'), row=1, col=1)

        specifiedTechnologyCount = dataLoaderInstance.getOffersCountPerRequirement(provider, 'c++',[start_date, end_date])
        print(len(specifiedTechnologyCount))
        dashboard.add_trace(
            go.Scatter(x=specifiedTechnologyCount["Data"], y=specifiedTechnologyCount["count"], mode='lines+markers',
                       name='Total Jobs Offers in backend category'), row=2, col=1)


    UOPSalaries=dataLoaderInstance.combine_dataframes(dataLoader.DataLoader().getProvidersLabels()[1])
    dataLoaderInstance.getOffersCountPerRequirement(dataLoader.DataLoader().getProvidersLabels()[1], ''"c++"'',[start_date, end_date])

    for level in UOPSalaries['Level'].unique():
        # Filtracja danych dla danego poziomu
        df_level = UOPSalaries[UOPSalaries['Level'] == level]

        # Dodawanie śladu dla danego poziomu
        dashboard.add_trace(go.Scatter(x=df_level['Date'], y=df_level['UOP'], mode='lines', name=level), row=3, col=1)


    # if 'CJO' in selected_series:
    #     if noFluff_data:
    #         dates, _, cpp_offers_list, _, _, _, _ = zip(*noFluff_data)
    #         dashboard.add_trace(go.Scatter(x=dates, y=cpp_offers_list, mode='lines+markers', name='C++ Job Offers - noFluffjobs'), row=2, col=1)
    #     if JustJoinIT_data:
    #         dates, _, cpp_offers_list, _, _, _, _ = zip(*JustJoinIT_data)
    #         dashboard.add_trace(go.Scatter(x=dates, y=cpp_offers_list, mode='lines+markers', name='C++ Job Offers - JustJoinIT'), row=2, col=1)
    #
    # if 'RJO' in selected_series:
    #     if noFluff_data:
    #         dates, _, _, _, _, _,rust_offers = zip(*noFluff_data)
    #         dashboard.add_trace(go.Scatter(x=dates, y=rust_offers, mode='lines+markers', name='Rust Job Offers'), row=3, col=1)
    #     if JustJoinIT_data:
    #         dates, _, _, _, _, _,rust_offers = zip(*JustJoinIT_data)
    #         dashboard.add_trace(go.Scatter(x=dates, y=rust_offers, mode='lines+markers', name='Rust Job Offers'), row=3, col=1)

    dashboard.update_layout(height=900, width=1000, showlegend=True)

    return dashboard
