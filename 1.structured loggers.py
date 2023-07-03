import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CREDENTIALS_FILE = 'path/to/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)
    return service

def search_documents(query):
    service = authenticate()

    try:
        results = service.files().list(
            q=f"name contains '{query}' and mimeType='application/vnd.google-apps.document'",
            fields="files(id, name)",
            pageSize=10
        ).execute()
        documents = results.get('files', [])
        return documents
    except Exception as e:
        logger.error("An error occurred while searching for documents: %s", e)

def get_document_content(document_id):
    service = authenticate()

    try:
        request = service.files().export_media(fileId=document_id, mimeType='text/plain')
        content = request.execute()
        return content.decode('utf-8')
    except Exception as e:
        logger.error("An error occurred while retrieving document content: %s", e)

def process_query(query):
    documents = search_documents(query)
    if documents:
        logger.info("Found %d documents matching the query '%s'", len(documents), query)
        for document in documents:
            logger.info("Document ID: %s, Name: %s", document['id'], document['name'])
            content = get_document_content(document['id'])
        
    else:
        logger.info("No documents found matching the query '%s'", query)

if __name__ == '__main__':
    query = "natural language query"  
    process_query(query)
