# AutoDash ReadMe

## Video Demo https://www.youtube.com/watch?v=OZF0yScFogU&t=15s

## Overview
AutoDash is a comprehensive tool for scraping financial news articles from Yahoo Finance and conducting sentiment analysis on the collected data. It is designed to automatically retrieve news articles, process the content, and store the structured data in an Elasticsearch database for further analysis and visualization.

## Features

- **Web Scraping**: Automated retrieval of financial news articles from Yahoo Finance using Selenium WebDriver with headless Chrome.
- **Content Extraction**: Processing individual news articles to extract structured information, including the title, publication time, content, and related URLs using BeautifulSoup.
- **Sentiment Analysis**: A logistic regression model trained on financial text data to predict sentiment, with the ability to serialize the trained model for future use.
- **Elasticsearch Integration**: Storing and retrieving scraped and processed data using Elasticsearch, enabling robust data search and retrieval capabilities.
- **Data Visualization**: The extracted data and analysis results can be visualized using a Dash-based web dashboard (code not included in the snippet).

## Installation

1. **Clone the repository**:
   ```sh
   https://github.com/yanglianglu/Auto_Dash/tree/main
   ```

2. **Install dependencies**:
   - Ensure Python 3.9+ is installed on your system.
   - Install required Python packages:
     ```sh
     pip install -r requirements.txt
     ```

3. **Set up Elasticsearch**:
   - Open Docker Desktop and run docker-compose up -d
   - Preprocess the data and store it in Elasticsearch:
     ```sh
     python src/search/scrape_documents.py
     ```
   - Wait for few minutes for the data to be preprocessed and stored in Elasticsearch.
4. **Run the Application**:
   - Use the `mineData()` function to start scraping articles and populating the database.
   - Run the following command to start the web dashboard:
     ```sh
     python main.py
     ```
