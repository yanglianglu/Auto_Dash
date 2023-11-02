def getDocuments(query):
    fake_documents = {
        'total': 5,
        'results': [
            {
                'title': f'{query}',
                'url': f'https://www {query}.com/',
                'description': f'About {query} About {query} + ... More ways to shop: Find an {query} Store or other retailer near you. Or call 1-800-MY {query}.'
            },
            {
                'title': f'{query} Inc.',
                'url': f'https://en.wikipedia.org/wiki {query}_Inc.',
                'description': f'{query} Inc. is an American multinational technology company headquartered in Cupertino, California. As of March 2023, {query} is the worlds biggest company by ...'
            },
            {
                'title': f'AAPL: {query} Inc - Stock Price, Quote and News',
                'url': f'https://www.cnbc.com/quotes/AAPL',
                'description': f'Get {query} Inc(AAPL: NASDAQ) real-time stock quotes, news, price and financial information from CNBC.'
            }
        ]
    }
    return fake_documents
