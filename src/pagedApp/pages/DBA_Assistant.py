import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from src.shared.get_embedding_function import get_embedding_function
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file

chroma_path = os.environ.get("VECTORDB_DBA")
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

st.title("DBA Assistant")

query_text = st.text_area("Ingrese la pregunta ")
if(st.button("Enviar pregunta")):
        retriever = SelfQueryRetriever.from_llm(
            llm,
            db,
            "document_content_description",
            metadata_field_info,
        )
        #results = db.similarity_search_with_score(query_text, k=5)
        results = retriever.invoke(query_text)
        context_text = "\n\n---\n\n".join([doc.page_content for doc in results])

        sources = "\n\n---\n\n".join([f"{doc.metadata['source']}" for doc in results])
        st.header("Preguntas similares") 
        for  doc in results:
            st.write(doc.page_content)
            st.write(f'{doc.metadata["motor"]}:{doc.metadata["source"]}')
  
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        response_text = model.invoke(prompt)
        st.header("Respuesta a partir del contexto")
        st.write(response_text.content)
