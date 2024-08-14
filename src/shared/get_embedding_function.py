from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings


    # Los embeddings que no hacen parte de langchain.community (deplicate)
    # o en librería Lanchain_* creada por el fabricante 
    # implementan la interfaz que necesita langchain 
    
import os


# create EF with custom endpoint


def get_embedding_function(model="sentence-transformers/all-mpnet-base-v2"):

    # Ollama
   # embeddings = OllamaEmbeddings(model="nomic-embed-text",       )

    # HuggingFace descarga al librería local
    # embeddings = HuggingFaceEmbeddings(model=model)

    # Hub ejecuta en servidores de hugging face
    embeddings = HuggingFaceEndpointEmbeddings(
        model=model,
        task="feature-extraction",

    )

    # embeddings= GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    return embeddings


def get_embedding_function_for_chunks():
   # embeddings = OllamaEmbeddings(model="nomic-embed-text",       )
    model = "sentence-transformers/all-mpnet-base-v2"

    # HuggingFace
    # embeddings = HuggingFaceEmbeddings( model = model)

    embeddings = HuggingFaceEndpointEmbeddings(
        model=model,
        task="feature-extraction",

    )
   
    return embeddings