from langchain import  PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import os

# Configuración del modelo
llm = ChatGoogleGenerativeAI(model='gemini-pro',temperature=0)

# Plantillas de prompt
prompt_template = """
Eres un asistente muy útil. El usuario te hará preguntas, y debes responderlas con precisión y claridad.
Pregunta: {user_input}
Respuesta:
"""

# Crear la cadena de LLM
prompt = PromptTemplate(template=prompt_template, input_variables=["user_input"])
llm_chain = prompt | llm

def get_response(user_input):
    response = llm_chain.run({"user_input": user_input})
    return response
