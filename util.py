import json
import os

import meilisearch
from fastapi.encoders import jsonable_encoder

MEILI_URL = os.getenv("MEILI_URL")
MEILI_MASTER_KEY = os.getenv("MEILI_MASTER_KEY")

client = meilisearch.Client(MEILI_URL, MEILI_MASTER_KEY)

async def write_json_to_file(data: dict) -> None:
    with open('device_list.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(jsonable_encoder(data)))


def _encode_document(document: dict) -> dict:
    """Return a version of the document safe for JSON serialization."""
    return jsonable_encoder(document)

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
    """Add a single document to the devices index."""
    index = client.index('devices')
    index.add_documents([_encode_document(document)])


def update_document_in_meilisearch(document: dict):
    """Update a document in the devices index."""
    index = client.index('devices')
    index.add_documents([_encode_document(document)])


def delete_document_from_meilisearch(document_id: int):
    """Delete a document from the devices index."""
    index = client.index('devices')
    index.delete_document(str(document_id))


def index_bulk_devices(documents: list[dict]):
    """Add multiple documents to the devices index."""
    index = client.index('devices')
    index.add_documents([_encode_document(d) for d in documents])

