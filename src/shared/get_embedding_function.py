from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceHubEmbeddings
#from langchain_google_genai import GoogleGenerativeAIEmbeddings

import os


# create EF with custom endpoint


def get_embedding_function(model="sentence-transformers/all-mpnet-base-v2"):

    # Ollama
   # embeddings = OllamaEmbeddings(model="nomic-embed-text",       )

    # HuggingFace descarga al librería local
    # embeddings = HuggingFaceEmbeddings(model=model)

    # Hub ejecuta en servidores de hugging face
    embeddings = HuggingFaceHubEmbeddings(
        model=model,
        task="feature-extraction",

    )
    # Los embeddings que no hacen parte de langchain.community no
    # implementant la interfaz que necesita langchain 
    # embeddings= GoogleGenerativeAIEmbeddings(model="models/embedding-001",api_key=google_api_key)

    return embeddings


def get_embedding_function_for_chunks():
   # embeddings = OllamaEmbeddings(model="nomic-embed-text",       )
    model = "sentence-transformers/all-mpnet-base-v2"

    # HuggingFace
    # embeddings = HuggingFaceEmbeddings( model = model)

    embeddings = HuggingFaceHubEmbeddings(
        model=model,
        task="feature-extraction",

    )
   
    return embeddings