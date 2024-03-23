from dash import Dash, dcc, html, Input, Output, callback
from Backend import mainBackend, dataLoader
from Frontend import mainView


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.layout = mainView.mainDiv

if __name__ == '__main__':
    app.run(debug=True)
