import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import dash_auth

nsdq = pd.read_csv('dataset/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)


options = []
for tic in nsdq.index:
    my_dict = {}
    my_dict['label'] = nsdq.loc[tic]['Name'] +' '+ tic      #apple company aapl
    my_dict['value'] = tic
    options.append(my_dict)


app = dash.Dash()

USERNAME_PASSWORD_PAIRS = {'shyam': 'prasath'}
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server


app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Enter the stock symbol:', style={'paddingRight': '30px'}),
        dcc.Dropdown(
            id='my-ticker-symbol',
            options = options,
            value=['TSLA'],
            multi=True)
        ],style= {'display': 'inline-block', 'verticalAlign': 'top'}),

    html.Div([
        html.H3('select a start and end date:'),
        dcc.DatePickerRange(id = 'my-date-picker',
                            min_date_allowed= datetime(2015,1,1),
                            max_date_allowed= datetime.today(),
                            start_date= datetime(2018,1,1),            # default
                            end_date = datetime.today(),              # default
                            )
        ], style= {'display': 'inline-block'}),

    html.Div([
        html.Button(id = 'submit-button',
                    n_clicks= 0,
                    children= 'Submit', style= {'fontSize': 24, 'marginLeft': '30px'})
    ], style= {'display': 'inline-block'}),
        dcc.Graph(
            id='my-graph'),
        dcc.Graph(
            id='my-graph_vol')
])

@app.callback(Output('my-graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('my-ticker-symbol', 'value'),
               State('my-date-picker', 'start_date'),
               State('my-date-picker', 'end_date'),
               ])
def update_graph(n_clicks,stock_ticker,start_date,end_date):
    start_date = start_date
    end_date = end_date

    traces = []
    for tic in stock_ticker:
        df = web.get_data_yahoo(tic, start_date, end_date)
        traces.append({'x': df.index, 'y': df['Adj Close'], 'name' : tic})

    fig = {
        'data': traces,
        'layout': {'title': 'stock_ticker Adj Close'}
    }
    return fig


@app.callback(Output('my-graph_vol', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('my-ticker-symbol', 'value'),
               State('my-date-picker', 'start_date'),
               State('my-date-picker', 'end_date'),
               ])
def update_graph_1(n_clicks,stock_ticker,start_date,end_date):
    start_date = start_date
    end_date = end_date

    traces_1 = []
    for tic in stock_ticker:
        df = web.get_data_yahoo(tic, start_date, end_date)
        traces_1.append({'x': df.index, 'y': df['Volume'], 'name' : tic})

    fig = {
        'data': traces_1,
        'layout': {'title': 'stock_ticker_Volume'}
    }
    return fig


if __name__ == '__main__':
    app.run_server()
