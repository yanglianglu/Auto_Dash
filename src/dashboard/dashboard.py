# to run: python .\dashboard.py
import json
import dash
from dash import dcc, html, dash_table, ctx
from dash.dependencies import Input, Output, State, ALL

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AutoDash"),
    html.Div(children=[
        html.Div("Please input your search query: "),
        dcc.Input(id='query-input', type='text', value='',
                  placeholder='Enter search query', style={'width': '500px'}),
        html.Button('Search', id='search-btn', n_clicks=0),
    ]),

    html.Div([
        html.H1("Results"),
        html.Ul(id='document-list'),
    ], id='results-page', style={'display': 'none'}),
])


def getDocuments(query):
    fake_documents = [
        "Document 1",
        "Document 2",
        "Document 3",
        "Document 4",
    ]
    return fake_documents


@app.callback(
    Output('results-page', 'style'),
    Input('search-btn', 'n_clicks'),
)
def update_pages(n_clicks):
    if n_clicks is None:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback(
    Output('document-list', 'children'),
    Input('search-btn', 'n_clicks'),
    State('query-input', 'value'),
)
def update_results(n_clicks, query):
    if n_clicks is None:
        return []

    documents = getDocuments(query)

    if query:
        results = [html.Li(doc) for doc in documents]
    else:
        results = []

    return results


if __name__ == '__main__':
    app.run_server(debug=True)
