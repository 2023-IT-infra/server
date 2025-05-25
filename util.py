import meilisearch
import json

client = meilisearch.Client('http://localhost:7700', 'aSampleMasterKey')

async def write_json_to_file(data: dict) -> None:
    with open('device_list.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data))

async def get_meilisearch(term: str) -> list[dict]:
    # Search for documents in the index
    index = client.index('devices').search(term)

    # Get the documents from the search result
    documents = index['hits']

    # Convert the documents to a list of dictionaries
    documents_list = []
    for document in documents:
        documents_list.append(document)

    return documents_list

def add_document_to_meilisearch(document: dict):
    # Create a new index
    index = client.index('devices')

    # Add a document to the index
    index.add_documents([document])