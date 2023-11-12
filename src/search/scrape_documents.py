import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


from bs4 import BeautifulSoup 
import requests


import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import utils.database_utils as db

numOfRetries = 3

def initBrowser():
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver


# Given a keyword, get the first n number of documents from yahoo finance
# Documents are returned as a list of url string
# [
#     'https://finance.yahoo.com/news/retail-investors-can-now-bet-on-music-royalties-we-want-people-to-have-access-150221575.html',
#     'https://finance.yahoo.com/news/foxconn-faces-tax-audit-land-024521324.html',
#     'https://finance.yahoo.com/news/iphone-assembler-hon-hai-dives-010601477.html',
#     'https://finance.yahoo.com/m/05189731-ff16-33e1-b077-dfead8ad1cb9/paypal-s-new-boss.html',
# ]
def getDocumentsUrls(keyword, n):  
    """
    :param string keyword: keyword to search
    :param int n: number of docs to return

    """

    url = "https://finance.yahoo.com/"
    cur = 0

    while cur < numOfRetries:
        try:
            driver = initBrowser()
        except:
            print("There was an issue initializing browser window")
            continue
        driver.get(url)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "header-search-form"))
            )
            break
        except:
            cur += 1
            print("Could not load " + url + ", retrying")
            driver.close()

    if cur == numOfRetries:
        print("Could not load " + url + ", exiting")
        driver.quit()
        return []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "header-search-form"))
        )
    except:
        print("Could not load yahoo finace")
        driver.quit()
        return []

    searchBar = driver.find_element(By.XPATH, "//form[contains(@action, '/quote')]")
    searchBarInput = searchBar.find_element(By.TAG_NAME, "input")
    searchBarInput.send_keys(keyword)
    searchBarButton = searchBar.find_element(By.ID, "header-desktop-search-button")
    searchBarButton.click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'mrt-node-quoteNewsStream')]"))
        )
    except:
        print("Could not load results")
        driver.quit()
        return []
    
    resultsDiv = driver.find_element(By.XPATH, "//div[contains(@id, 'mrt-node-quoteNewsStream')]")
    results = resultsDiv.find_elements(By.TAG_NAME, "li")
    filteredResults = []
    for result in results:
        try:
            result.find_element(By.XPATH, ".//a[text()='Ad']")
        except:
            filteredResults.append(result)

    prev  = 0
    while len(filteredResults) < n:
        print("{} urls found".format(len(filteredResults)))
        if (prev == len(filteredResults)):
            print("Maximum number of documents found related to " + keyword)
            break
        prev = len(filteredResults)
        driver.execute_script("arguments[0].scrollIntoView();",results[-1])
        time.sleep(1)

        results = resultsDiv.find_elements(By.TAG_NAME, "li")
        filteredResults = []
        for result in results:
            try:
                result.find_element(By.XPATH, ".//a[text()='Ad']")
            except:
                filteredResults.append(result)

    print("{} urls found".format(len(filteredResults)))

    res = []
    for result in filteredResults[:n]:
        a = result.find_element(By.TAG_NAME, "a")
        res.append(a.get_attribute('href'))
    
    driver.quit()
    return res

def processDocumentUrl(url):
    print("Processing " + url)
    r = requests.get(url)
    if r.status_code != 200:
        print('Cannot open url')
        return
    soup = BeautifulSoup(r.content, 'html5lib')
    try:

        head = soup.find('head')
        title = head.find('title').text
        origUrl = head.find('meta', {'property': 'og:url'})['content']
        isExternal = url != origUrl
        keywords = head.find('meta', {'name': 'news_keywords'})['content'].split(',')

        article = soup.find('article')

        pubTime = article.find('time')['datetime']

        urls = article.findAll('a')
        urls = [a['href'] for a in urls if a.has_attr('href')]

        paragraphs = article.findAll('p')
        body = [p.text for p in paragraphs]

        return {
            'base_url': url,
            'is_external': isExternal,
            'title': title,
            'published_time': pubTime,
            'keywords': keywords,
            'body': "\n".join(body),
            'urls': urls
        }
    
    except:
        return

# Given a list of urls, process the urls and return a list of documents
# [
#     {
#       'base_url': 'https://finance.yahoo.com/m/05189731-ff16-33e1-b077-dfead8ad1cb9/paypal-s-new-boss.html',
#       'title': "PayPal's New Boss",
#       'published_time': '2023-11-03T21:17:17.000Z' datetime in ISO format
#       'body': "When PayPal Holdings reports third quarter earnings on Nov. 1, it'll give new Chief Executive Alex Chriss his first chance to lay out his turnaround strategy."
#       'keywords': [],
#       'urls': []
#     },
#     {
#        ...
#     },
#     ...
# ]
def processUrls(urls):
    res = []
    for url in urls:
        doc = processDocumentUrl(url)
        if doc:
            res.append(doc)
    return res

def mineNewsUrls():
    url = 'https://finance.yahoo.com/'
    cur = 0

    while cur < numOfRetries:
        try:
            driver = initBrowser()
        except:
            print("There was an issue initializing browser window")
            continue
        driver.get(url)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "header-search-form"))
            )
            break
        except:
            cur += 1
            print("Could not load " + url + ", retrying")
            driver.close()

    if cur == numOfRetries:
        print("Could not load " + url + ", exiting")
        driver.quit()
        return []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'mrt-node-slingstoneStream')]"))
        )
    except:
        print("Could not load results")
        driver.quit()
        return []
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    last_height = driver.execute_script("return document.getElementById('slingstoneStream-0-Stream').scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollBy(0, document.getElementById('slingstoneStream-0-Stream').scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.getElementById('slingstoneStream-0-Stream').scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height

    resultsDiv = driver.find_element(By.XPATH, "//div[contains(@id, 'mrt-node-slingstoneStream')]")
    results = resultsDiv.find_elements(By.TAG_NAME, "li")
    filteredResults = []
    for result in results:
        try:
            result.find_element(By.XPATH, ".//a[text()='Ad']")
        except:
            filteredResults.append(result)

    print("{} urls found".format(len(filteredResults)))

    res = []
    for result in filteredResults:
        a = result.find_element(By.TAG_NAME, "a")
        res.append(a.get_attribute('href'))
    
    driver.quit()
    return res

def mineData():
    client = db.create_client()
    
    if not client.indices.exists(index="documents"):
        db.create_index(client, "documents")

    visited = set()
    urls = mineNewsUrls()
    count = 0
    while urls:
        url = urls.pop(0)
        if url not in visited and 'https://finance.yahoo.com' in url:
            doc = processDocumentUrl(url)
            if doc:
                count = count + 1
                try:
                    db.get_document(client, "documents", url)
                except:
                    db.index_document(client, "documents", url, doc)
                    print('Document inserted into elasticsearch')
                urls.extend(doc['urls'])
            visited.add(url)

# Example Usage
if __name__ == "__main__":
    mineData()