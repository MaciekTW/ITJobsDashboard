from dash import Dash, dcc, html, Input, Output, callback
from Backend import mainBackend, dataLoader
from Frontend import mainView
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.layout = mainView.mainDiv
app.title="IT Market Dashboard"

if __name__ == '__main__':
    app.run(debug=True)
