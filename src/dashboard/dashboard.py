# to run: python .\dashboard.py
import json
import dash
from dash import dcc, html, dash_table, ctx
from dash.dependencies import Input, Output, State, ALL
import dashboard.data_api as data_api

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(children=[
        html.Div(children=[
            html.Img(
                src=dash.get_asset_url('logo.png'), style={'height': '100px'})
        ], className='logo'),
        html.Div(children=[
            dcc.Input(id='query-input', type='text', value='',
                      placeholder='', className='searchbar'),
        ], className='bar'),
        html.Div(children=[
            html.Button('Search', id='search-btn',
                        n_clicks=0, className='button'),
        ], className='buttons')
    ], id='search-page'),

    html.Div([
        html.Div(children=[
            html.Img(
                src=dash.get_asset_url('logo.png'), style={'height': '50px'}),
            html.Div(children=[
                dcc.Input(id='query-input2', type='text', value='',
                          placeholder='', className='searchbar'),
            ], className='bar', style={'margin': '0 20px'}),
            html.Button('Search', id='search-btn2',
                        n_clicks=0, className='button'),
        ], className='topbar'),
        html.Div(children=[], className='searchresults', id='document-list'),
        html.Div(children=[], className='summaryresults', id='summary-list'),
        html.Div(children=[], className='sentimentresults', id='sentiment'),
    ], id='results-page', style={'display': 'none'}),
])


@app.callback(
    [Output('search-page', 'style'), Output('results-page', 'style')],
    Input('search-btn', 'n_clicks'),
    State('query-input', 'value'),
)
def update_pages(n_clicks, query):
    print('update_pages', n_clicks)
    if n_clicks == 0:
        return [{'display': 'block'}, {'display': 'none'}]
    else:
        return [{'display': 'none'}, {'display': 'block'}]


@app.callback(
    [Output('document-list', 'children'),
     Output('query-input2', 'value'),
     Output('summary-list', 'children'),
     Output('sentiment', 'children')],
    [Input('search-btn', 'n_clicks'), Input('search-btn2', 'n_clicks')],
    [State('query-input', 'value'), State('query-input2', 'value')],
)
def update_results(n_clicks, n_clicks2, query, query2):
    print('update_results', ctx.triggered_id,
          n_clicks, n_clicks2, query, query2)
    if ctx.triggered_id is None:
        return [[], '', [], []]
    if ctx.triggered_id == 'search-btn':
        query = query
    elif ctx.triggered_id == 'search-btn2':
        query = query2

    print(f'getDocuments {query}')
    documents = data_api.getDocuments(query)
    print(f'documents {documents}')

    results = []

    for result in documents['results']:
        results.append(html.Div(children=[
            html.H2(result['title']),
            html.A(result['url'], href=result['url']),
            html.P(result['description'])
        ], className='searchresult'))

    summary = data_api.getSummarization(query)
    summaryresults = []
    print(summary)
    for word in summary:
        summaryresults.append(html.Div(children=[
            html.Div(word['term']),
            html.Div(word['weight'])
        ]))

    sentiment = data_api.getSentiment(query)
    sentimentresults = [
        html.Div('Sentiment: '),
        html.Div(sentiment)
    ]

    return [results, query, summaryresults, sentimentresults]


if __name__ == '__main__':
    app.run_server(debug=True)
