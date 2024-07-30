import streamlit as st
#from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from src.shared.get_embedding_function import get_embedding_function
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

import azure.identity
from langchain_community.vectorstores.azuresearch import AzureSearch

from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file

#chroma_path = os.environ.get("CHROMA_PATH")

vector_store_address = os.environ.get("AZURE_SEARCH_SERVICE")
vector_store_key = os.environ.get("AZURE_SEARCH_KEY")
embedding_model = os.environ.get("EMBEDDING_MODEL_QA")
PROMPT_TEMPLATE = """
Eres un analista de seguridad de la compañía llamada SETI, debes responder unas 
preguntas de seguridad a un cliente, anteriormente se han respondido las siguientes
preguntas similares así:

{context}

---

Ahora basado en las pregunta anteriores responde esta: {question}
"""


llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0)
model = llm
    
embedding_function = get_embedding_function(embedding_model)
#db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

index_name: str = "idx_security_survey"
db: AzureSearch = AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=vector_store_key,
        index_name=index_name,
        embedding_function=get_embedding_function(embedding_model),
        #token_provider = token_provider
    )

st.title("Analista de Seguridad SETI")

query_text = st.text_area("Ingrese la pregunta ")
if(st.button("Enviar pregunta")):
    
        results = db.similarity_search(query_text, k=2,)
        context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
        #sources = "\n\n---\n\n".join([f"{doc.metadata['filename']}:{doc.metadata['line_number']}:" for doc, _score in results])
        st.header("Preguntas similares") 
        for  doc in results:
            st.write(doc.page_content)
            st.write(f"Archivo:{doc.metadata['filename']}|linea:{doc.metadata['line_number']}")
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        response_text = model.invoke(prompt)
        st.header("Respuesta a partir del contexto")
        st.write(response_text.content)
