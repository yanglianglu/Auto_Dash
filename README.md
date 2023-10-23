AutoDash/
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- docker-compose.yml (optional)

|-- data/
|   |-- raw/
|   |-- processed/
|   |-- embeddings/

|-- notebooks/
|   |-- EDA.ipynb
|   |-- model_prototyping.ipynb
|   |-- etc.ipynb

|-- src/
|   |-- __init__.py
|   |-- main.py
|   |-- utils/
|       |-- __init__.py
|       |-- database_utils.py
|       |-- network_graph.py
|       |-- query_expansion.py
|   |-- search/
|       |-- __init__.py
|       |-- scrape_documents.py
|   |-- preprocessing/
|       |-- __init__.py
|       |-- text_preprocessing.py
|   |-- models/
|       |-- __init__.py
|       |-- topic_model.py
|       |-- sentiment_model.py
|       |-- summarization_model.py
|       |-- embeddings.py
|   |-- dashboard/
|       |-- __init__.py
|       |-- dashboard.py

```

### Explanation

1. **.gitignore**: To exclude files that shouldn't be tracked, such as temporary files or secrets.

2. **README.md**: For project description, setup guide, etc.

3. **requirements.txt**: Required Python packages.

5. **docker-compose.yml**: For containerization and package setup if you intend to use these technologies.

6. **data/**: To store raw and processed data.
   - **raw/**: Original, immutable data dump.
   - **processed/**: Cleaned data that feeds into models.
   - **embeddings/**: Any pre-trained or generated embeddings.

7. **notebooks/**: Jupyter notebooks for EDA and model prototyping.

8. **src/**: All the source code.
   - **main.py**: Main script to run tasks.
   - **utils/**: Utility functions like database utilities.
   - **search/**: Functions related to scraping and search engine API calls.
   - **preprocessing/**: Text preprocessing functions.
   - **models/**: Machine learning and NLP models.
   - **dashboard/**: Code to create and manage the dashboard.

## dependencies
1. Python 3.11
2. Elasticsearch 7.15.0



## Setup
1. Run docker-compose up -d to start the elasticsearch container
   - elasticsearch is available at http://localhost:9200
   - kibana is available at http://localhost:5601
   - username: elastic, password: abcdefg
   - we usually don't interact with elasticsearch directly, but it's useful for visual inspection of the data
