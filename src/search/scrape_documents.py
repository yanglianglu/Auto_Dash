import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

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

    res = []
    for result in filteredResults[:n]:
        a = result.find_element(By.TAG_NAME, "a")
        res.append(a.get_attribute('href'))
    
    driver.quit()
    return res

def processDocumentUrl(driver, url):
    print("Processing " + url)
    cur = 0
    while cur < numOfRetries:
        driver.get(url)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//h1[@data-test-locator='headline']"))
            )
            break
        except:
            cur += 1
            print("Could not load " + url + ", retrying")

    if cur == numOfRetries:
        print("Could not load " + url + ", skiping")
        return
    
    title = driver.find_element(By.XPATH, "//h1[@data-test-locator='headline']").text

    if driver.find_elements(By.XPATH, "//div[contains(@class, 'caas-readmore')]//*[text()='Continue reading']"):
        body = driver.find_element(By.CLASS_NAME, "caas-body")
        text = body.find_elements(By.TAG_NAME, 'p')
        print("External link")
        return {
            'base_url': url,
            'title': title,
            'body': "\n".join([p.text for p in text]),
            'urls': []
        }

    readMoreButtons = driver.find_elements(By.XPATH, "//div[contains(@class, 'caas-readmore')]//button")
    if readMoreButtons:
        expandButton = readMoreButtons[0]
        expandButton.click()
        time.sleep(1)

    body = driver.find_element(By.CLASS_NAME, "caas-body")
    text = body.find_elements(By.TAG_NAME, 'p')
    
    return {
        'base_url': url,
        'title': title,
        'body': "\n".join([p.text for p in text]),
        'urls': []
    }


# Given a list of urls, process the urls and return a list of documents
# [
#     {
#       'base_url': 'https://finance.yahoo.com/m/05189731-ff16-33e1-b077-dfead8ad1cb9/paypal-s-new-boss.html',
#       'title': "PayPal's New Boss",
#       'body': "When PayPal Holdings reports third quarter earnings on Nov. 1, it'll give new Chief Executive Alex Chriss his first chance to lay out his turnaround strategy."
#       'urls': []
#     },
#     {
#        ...
#     },
#     ...
# ]
# 
# 
# Note that this method cannot process the urls recursively
def processUrls(urls):
    try:
        driver = initBrowser()
    except:
        print("There was an issue initializing browser window")
        return []
    
    res = []
    for url in urls:
        doc = processDocumentUrl(driver, url)
        if doc:
            res.append(doc)

    return res



# urls = getDocumentsUrls("Apple", 10)
# f = open("urls.txt", "w")
# for url in urls:
#     f.write(url + "\n")

# f.close()


# f = open("urls.txt", "r")
# urls = f.read().rstrip().split("\n")
# docs = processUrls(urls)

# print(docs[0]['body'])


