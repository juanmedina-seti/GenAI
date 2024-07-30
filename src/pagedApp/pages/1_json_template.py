import streamlit as st
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file


PROMPT_TEMPLATE = """
Esta es la descripción de un proceso de negocio. Identifica las tareas en el proceso y quién las ejectura (rol)

{proceso}
Luego organiza las tareas y roles en una lista con formato json como en el siguiente ejemplo:

  "tareas": [
    {{
      "nombre": "Nombre de la Tarea",
      "rol": "Rol que Ejecuta la Tarea",
    }},
    {{
      "nombre": "Nombre de la Tarea 2",
      "rol": "Rol que Ejecuta la Tarea 2",
    }}
  


Por favor, devuelve la descripción del proceso de negocio en el formato JSON anterior.

"""


llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=.8)
model = llm
    
st.title("Digramador de procesos de negocio")

query_text = st.text_area("Escribe la descripción del proceso de negocio ")
if(st.button("Convertir a json")):
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(proceso=query_text)
    response_text = model.invoke(prompt)
    st.header("Resultado")
    st.write(str(response_text.content))
