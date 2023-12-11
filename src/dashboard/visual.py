import dash
from dash import Dash, dcc, html, Input, Output, callback, no_update
from dash.dependencies import Input, Output, State, ALL
from src.search.scrape_documents import processDocumentUrl
from src.dashboard.data_api import getDocuments
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Img(src=dash.get_asset_url('logo.png'), style={'height': '100px'})
        ], className='logo'),

        html.Div(children=[
            dcc.Input(id='query-input', type='text', value='', placeholder='Enter your query', className='searchbar')
        ], className='bar'),

        html.Div(children=[
            html.Button('Search', id='search-btn', n_clicks=0)
        ])
    ], id='search-page'),

    html.Div(children=[
], id='container')
])







@callback(
    Output('container', 'children'),
    Input('search-btn', 'n_clicks'),
    State('query-input', 'value'))
def update_output(n_clicks, value):
    if n_clicks == 0:
        return 'Search Results'
    else:
        print('update_output', n_clicks, value)
        urls = getDocuments(value)
        print(urls)
    return urls




