from azure.search.documents.models import VectorizedQuery
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os

azuresearch_endpoint= os.getenv("AZURE_SEARCH_ENDPOINT")
index_name=os.getenv("SEARCH_INDEX_NAME")
AZURE_SEARCH_KEY=os.getenv("AZURE_SEARCH_KEY")

search_client = SearchClient(
    endpoint=azuresearch_endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)


def upload_review_document(document):
    search_client.upload_documents(documents=[document])

def search_similar_reviews(embedding, top_k=3):
    vector_query = VectorizedQuery(
        vector=embedding,
        k_nearest_neighbors=top_k,
        fields="embedding"  # MUST match your index vector field name
    )

    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query]
    )

    return list(results)