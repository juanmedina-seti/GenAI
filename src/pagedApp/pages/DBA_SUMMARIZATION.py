import streamlit as st
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from dotenv import load_dotenv
import sys
import os

load_dotenv()  # Load the .env file
sys.path.append(".")


from src.shared.get_embedding_function import get_embedding_function

chroma_path = os.environ.get("VECTORDB_KB")
PROMPT_TEMPLATE = """
Eres un analista administrador de bases de datos con experiencia de 10 año,
tienes alto conocimiento en aseguramiento de motores de bases de datos, basado en
tu conocimiento y en algunas guías de SETI :

{context}

---

Responde esta pregunta: {question}
"""
metadata_field_info = [
    AttributeInfo(
        name="motor",
        description="Especifica el motor de base de datos ['oracle', 'mysql', 'mongodb', 'sqlserver', 'postgresql' ]",
        type="string",
    ),]

llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0)
model = llm
    
embedding_function = get_embedding_function()
db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

st.title("DBA Knowledge Base")

query_text = st.text_area("Ingrese la consulta ")
if(st.button("Enviar")):
        results = db.similarity_search(query_text, k=2)
        #results = retriever.invoke(query_text)
        

        st.header("Documentos relacionados") 
        
        for  doc in results:
            st.write(doc.page_content)
            st.write(f'{doc.metadata["source"]}')

