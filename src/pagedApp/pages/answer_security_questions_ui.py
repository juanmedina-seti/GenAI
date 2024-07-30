import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from src.shared.get_embedding_function import get_embedding_function
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file

chroma_path = os.environ.get("CHROMA_PATH")
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
    
embedding_function = get_embedding_function()
db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

st.title("Analista de Seguridad SETI")

query_text = st.text_area("Ingrese la pregunta ")
if(st.button("Enviar pregunta")):
    
        results = db.similarity_search_with_score(query_text, k=2)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = "\n\n---\n\n".join([f"{doc.metadata['filename']}:{doc.metadata['line_number']}:" for doc, _score in results])
        st.header("Preguntas similares") 
        for  doc, score in results:
            st.write(doc.page_content)
            st.write(f"Similitud (0-1): {score}|Archivo:{doc.metadata['filename']}|linea:{doc.metadata['line_number']}")
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        response_text = model.invoke(prompt)
        st.header("Respuesta a partir del contexto")
        st.write(response_text.content)
