from elasticsearch import Elasticsearch, helpers


# Create a Elasticsearch Client
def create_client():
    client = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http", 'use_ssl': False}],
                           http_auth=('elastic', 'abcdefg')
                           )
    return client

# Create an Index (Table)
def create_index(client, index_name):
    # Create an index is similar to create a table in SQL, or collection in MongoDB
    return client.indices.create(index=index_name)

# Index a Document
def index_document(client, index_name, doc_id, document):
    # Index a document is similar to insert a row in SQL, or insert a document in MongoDB
    return client.index(index=index_name, id=doc_id, body=document)


def bulk_index_documents(client, index_name, documents_list):
    """
    Bulk indexes a list of documents.

    Parameters:
    - client: The Elasticsearch client object
    - index_name: The name of the index where the documents will be stored
    - documents_list: A list of dictionaries, each containing all the relevant fields for a document

    Returns:
    - The response from the Elasticsearch bulk API
    """
    actions = [
        {
            "_index": index_name,
            "_id": doc.get("id", None),  # Use the 'id' field in the dict as the document ID, if present
            "_source": doc
        }
        for doc in documents_list
    ]

    return helpers.bulk(client, actions)

# Get a Document
def get_document(client, index_name, doc_id):
    # Get a document is similar to select a row in SQL, or find a document in MongoDB
    return client.get(index=index_name, id=doc_id)

# Search Documents
def search_documents(client, index_name, query):
    # This search function using scoring function "BM25" by default
    # Search documents is similar to select rows in SQL, or find documents in MongoDB
    # query is a dictionary, for example: {"match": {"foo": "foo"}}
    # see details: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
    return client.search(index=index_name, body={"query": query})

# Update a Document
def update_document(client, index_name, doc_id, updated_fields):
    # Update a document is similar to update a row in SQL, or update a document in MongoDB
    # updated_fields is a dictionary, for example: {"new_field": "new_value"}

    return client.update(index=index_name, id=doc_id, body={"doc": updated_fields})

# Delete a Document
def delete_document(client, index_name, doc_id):
    # Delete a document is similar to delete a row in SQL, or delete a document in MongoDB
    # Example: delete_document(client, "my_index", "my_document_id")
    return client.delete(index=index_name, id=doc_id)

# Delete an Index
def delete_index(client, index_name):
    # Delete an index is similar to delete a table in SQL, or delete a collection in MongoDB
    # Example: delete_index(client, "my_index")
    return client.indices.delete(index=index_name)

# Initialize Elasticsearch Client

# Example Usage
if __name__ == "__main__":
    client = create_client()
    # Create an index
    print(create_index(client, "my_index"))

    # Index a document
    print(index_document(client, "my_index", "my_document_id", {"foo": "foo", "bar": "bar"}))

    # Get a document
    print(get_document(client, "my_index", "my_document_id"))

    # Search documents
    print(search_documents(client, "my_index", {"match": {"foo": "foo"}}))

    # Update a document
    print(update_document(client, "my_index", "my_document_id", {"new_field": "new_value"}))

    # Delete a document
    print(delete_document(client, "my_index", "my_document_id"))

    # Delete an index
    print(delete_index(client, "my_index"))