from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceHubEmbeddings

import os


# create EF with custom endpoint


def get_embedding_function(model="sentence-transformers/all-mpnet-base-v2"):

    # Ollama
   # embeddings = OllamaEmbeddings(model="nomic-embed-text",       )

    # HuggingFace
    # embeddings = HuggingFaceEmbeddings()

    
    embeddings = HuggingFaceHubEmbeddings(
        model=model,
        task="feature-extraction",

    )
    # Google
    # google_api_key = os.environ["GOOGLE_API_KEY"]
    # embeddings= GoogleGenerativeAIEmbeddings(model="models/embedding-001",api_key=google_api_key)

    return embeddings


def get_embedding_function_for_chunks():
   # embeddings = OllamaEmbeddings(model="nomic-embed-text",       )

    # HuggingFace
    # embeddings = HuggingFaceEmbeddings()

    model = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceHubEmbeddings(
        model=model,
        task="feature-extraction",

    )
    # Google
    # google_api_key = os.environ["GOOGLE_API_KEY"]
    # embeddings= GoogleGenerativeAIEmbeddings(model="models/embedding-001",api_key=google_api_key)

    return embeddings