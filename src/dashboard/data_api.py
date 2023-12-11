import time
import pandas as pd
from collections import Counter

from src.search.scrape_documents import getDocumentsUrls, processDocumentUrl
import src.models.sentiment_model as sentiment_model
import src.models.summarization_model as summarization_model
import src.models.topic_model as tm


MOCK_DATA = False

MOCK_DOCUMENTS = {
    'total': 10,
    'results': [{'title': 'Zoom quietly makes its way to Apple TV',
                 'url': 'https://finance.yahoo.com/news/zoom-quietly-makes-way-apple-235953397.html',
                 'description': 'The video conferencing app Zoom has quietly arrived on Apple TV 4K, allowing users to conduct meetings via their television and an iPhone or iPad.'},
                {'title': 'Even After Black Friday, These 7 Costco Electronics Are Still Great Holiday Deals',
                 'url': 'https://finance.yahoo.com/news/even-black-friday-7-costco-200012460.html',
                 'description': "This December, Costco members will find steep discounts on electronics for everyone on their holiday wish list. Many sales start at $30 off the item's original online price with savings upward of $250..."},
                {'title': 'JP Morgan’s Top 15 Stock Picks for 2023 and Now',
                 'url': 'https://finance.yahoo.com/news/jp-morgan-top-15-stock-190553259.html',
                 'description': 'In this piece, we will take a look at JP Morgan’s top 15 stock picks for 2023 and most recent stock picks. If you want to skip our introduction to the world’s biggest bank in terms of assets, its latest performance, and other details, then check out JP Morgan’s Top 5 Stock Picks for 2023. […]'},
                {'title': 'How to master the camera app on iPhone 15 Pro & 15 Pro Max',
                 'url': 'https://finance.yahoo.com/news/master-camera-app-iphone-15-174500644.html',
                 'description': "The new iPhone 15 Pro and iPhone 15 Pro Max have the most impressive cameras Apple has created to date. Here's how you can get the most out of them to make your photos and videos look stunning."},
                {'title': 'How to manage notifications in iOS 17 and iPadOS 17',
                 'url': 'https://finance.yahoo.com/news/manage-notifications-ios-17-ipados-154913624.html',
                 'description': 'While the biggest changes to notifications happened in iOS 15 and iPadOS 15, there are still some important tips to know for managing them within iOS 17 and iPadOS 17.'},
                {'title': 'Apple releases urgent iOS update due to security exploits',
                 'url': 'https://finance.yahoo.com/news/apple-releases-urgent-ios-due-152453756.html',
                 'description': 'Apple released an update to its operating system this week, seeking to patch rumored security gaps in its landmark iOS 17.1.1 release earlier this year.'},
                {'title': 'Digital Payments Are Having a Jolly Holiday',
                 'url': 'https://finance.yahoo.com/m/5c0763d9-3367-3c08-896c-ba2af5b5e747/digital-payments-are-having-a.html',
                 'description': 'E-commerce sales also help boost the platforms that stores and sellers use for digital payments and shopping. Shopify said its merchants saw a 24% boost in Black Friday-Cyber Monday weekend sales over last year.'},
                {'title': "iPhone 15 Portrait Mode in focus for 'Album Cover' ad spot",
                 'url': 'https://finance.yahoo.com/news/iphone-15-portrait-mode-focus-124649017.html',
                 'description': "Apple's new ad for the iPhone 15 highlights the ability to take Portrait Mode shots with the camera, via a band politely fighting over an album cover photo."},
                {'title': 'A Bull Market Is Coming: 2 "Magnificent Seven" Stocks to Buy Right Now and Hold Forever',
                 'url': 'https://finance.yahoo.com/m/7015b70a-a44d-3b9b-b9f4-3357a9a328e1/a-bull-market-is-coming-2.html',
                 'description': 'These two companies could be the best-performing Magnificent Seven stocks through the next bull market and beyond.'},
                {
                    'title': 'Surprise! Warren Buffett Has Bet Over $176 Billion in 3 Artificial Intelligence (AI) Growth Stocks',
                    'url': 'https://finance.yahoo.com/m/f324d96b-9cfe-32ef-962e-61e5c1f9dc4c/surprise-warren-buffett-has.html',
                    'description': "Buffett has consistently said he has difficulty fathoming complex technology, but he's accumulated a fortune in AI stocks."}]
}


def getDocuments(query):
    if not MOCK_DATA:
        return getDocumentsUrls(query, 10)
    # in mock data, still simulate the waiting time
    time.sleep(1)
    return MOCK_DOCUMENTS


summarizer = summarization_model.init_model()


def getSummarization(result):
    if result["scraped"] is None:
        return 'Failed to scrape'
    # return 'summary'
    summary = summarization_model.inference(
        summarizer, result["scraped"]['body'])
    print(f'summary: {summary}')
    return summary


def getTopics(documents):
    docs = []
    for result in documents['results']:
        if result["scraped"] is None:
            continue
        docs.append(result["scraped"]['body'])
    ldam, common_corpus, texts = tm.fit_topic_model(docs)
    topics = ldam.show_topics(4, formatted=False)
    return [{'topic_id': i, 'word_weight': [{'term': k[0], 'weight': k[1]} for k in pairs]} for i, pairs in topics]

    # cnt = Counter()
    # total = 0
    # for result in documents['results']:
    #    if result["scraped"] is None:
    #        continue
    #    for keyword in result["scraped"]['keywords']:
    #        cnt[keyword] += 1
    #        total += 1
    # return [{'term': key, 'weight': value / total}
    #        for key, value in cnt.items()]


    # import random
    # words = []
    # for i in range(5):
    #     words.append({'term': f'{query}{i+1}', 'weight': random.random()})
    # return words


sentiment = sentiment_model.LogisticRegressionModel() if not MOCK_DATA else None


def getSentiment(documents):
    if MOCK_DATA:
        import random
        return random.random()

    results = []
    df_data = []
    for doc in documents['results']:
        df_data.append(doc['summary'])

    df = pd.DataFrame(df_data, columns=["Text"])
    results = sentiment.predict(df)
    print(f'getSentiment {results} {results[0]}')

    if results[0] == 'neutral':
        return 0.5
    elif results[0] == 'positive':
        return 1.0
    elif results[0] == 'negative':
        return 0.0
    else:
        print('unknown sentiment')
        return 0.5

    import random
    return random.random()
