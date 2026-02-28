from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
azuresearch_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT")
#azuresearch_endpoint= os.getenv("AZURE_SEARCH_ENDPOINT")
#index_name=os.getenv("SEARCH_INDEX_NAME")
#AZURE_SEARCH_KEY=os.getenv("AZURE_SEARCH_KEY")
AZURE_OPENAI_KEY =os.getenv("AZURE_OPENAI_KEY")
api_version_value=os.getenv("VECTOR_SEARCH_API_VERSION") 
EMBEDDING_DEPLOYMENT=os.getenv("EMBEDDING_DEPLOYMENT")


emd_client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version=api_version_value,
    azure_endpoint=azuresearch_endpoint
)

def generate_embedding(text: str):
    print(f"inside the embeddings.py ----Generating embedding for text: {text}")
    response = emd_client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text
    )
    return response.data[0].embedding