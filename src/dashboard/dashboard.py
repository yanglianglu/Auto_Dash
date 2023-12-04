# to run: python .\dashboard.py
import json
import dash
from dash import dcc, html, dash_table, ctx
from dash.dependencies import Input, Output, State, ALL
from wordcloud import WordCloud
import io
from base64 import b64encode

import dashboard.data_api as data_api
from search.scrape_documents import processDocumentUrl

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
        html.Div(children=[], className='sentimentresults section',
                 id='sentiment'),
        html.Div(children=[], className='summaryresults section',
                 id='summary-list'),
        html.Div(children=[], className='searchresults section',
                 id='document-list'),
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

    first = True
    first_scraped = None
    for result in documents['results']:
        if first:
            print(f'scraping URL: {result["url"]}')
            result['scraped'] = processDocumentUrl(result['url'])
            first_scraped = result['scraped']
            print(f'scraped doc: {result["scraped"]}')
            result['summary'] = data_api.getSummarization(result)
            if data_api.MOCK_DATA:
                first = False
        else:
            # during testing, avoid sending too may requests
            result['scraped'] = first_scraped
            result['summary'] = 'Skipped in testing mode'

    results.append(html.H2('Documents Found'))
    for result in documents['results']:
        results.append(html.Div(children=[
            html.H2(result['title']),
            html.A(result['url'], href=result['url']),
            html.P(result['description']),
            html.H3('Summarizer model output: '),
            html.P(result['summary']),
        ], className='searchresult'))

    sentiment = data_api.getSentiment(documents)
    sentiment_text = ''
    if sentiment < 0.33:
        sentiment_text = 'Negative'
    elif sentiment < 0.66:
        sentiment_text = 'Neutral'
    else:
        sentiment_text = 'Positive'
    sentimentresults = [
        html.H2('Overall Sentiment'),
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Div(className="st slice-item") for i in range(5)
                ], className="slice-colors"),
                html.Div(className="needle", style={
                         'rotate': f'{int(180*sentiment)}deg'}),
                html.Div(sentiment_text, className='gauge-center'),
            ], className='gauge')
        ], className='wrapper')
    ]

    summary = data_api.getTopics(documents)
    summaryresults = []
    # print(summary)
    # for word in summary:
    #     summaryresults.append(html.Div(children=[
    #         html.Div(word['term']),
    #         html.Div(word['weight'])
    #     ]))
    wordcloud = WordCloud(width=625, height=300, background_color='white')
    wordcloud.fit_words({word['term']: word['weight'] for word in summary})
    img = wordcloud.to_image()
    image_io = io.BytesIO()
    img.save(image_io, 'PNG')
    summaryresults.append(html.H2('Topics'))
    summaryresults.append(html.Img(
        src='data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')))

    return [results, query, summaryresults, sentimentresults]


if __name__ == '__main__':
    app.run_server(debug=True)
