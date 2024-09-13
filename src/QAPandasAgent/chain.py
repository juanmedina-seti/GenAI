
from langchain_groq  import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

#from langchain.agents import create_structured_chat_agent
import pandas as pd


from dotenv import load_dotenv

load_dotenv()


#dataframe
df = pd.read_csv("data/csv/cierre.csv",delimiter=";")

df['HPBPROC'] = df['HPBPROC'].str.strip() #quita espacios en blanco el nombre de proceso
df['HPBDESC'] = df['HPBDESC'].str.strip() #quita espacios en blanco el descripción de proceso

prefix = """
Eres un asistente muy útil. El usuario te hará preguntas, y debes responderlas con precisión y claridad.
el dataframe tiene datos de la duración (en la columna duracion) de todos las tareas de cierre. 
Los campos con las fecha y horas de inicio y fin son: HPBFINI que es la fecha de inicio, HPBHINI que es la hora de inicio, HPBFFIN fecha de fin y HPBHFIN hora de fin. 
El cierre de cada dia inicia en la misma fecha y finaliza en la mañana del dia siguiente.  
La duración proceso de cierre inicia con la tarea identificada por HPBDESC='Inhabilita accesos al menu' 
hasta la fecha de finalización de la tarea identificada por HPBPROC=OCIE1000.
Si no finaliza antes de las 8:00:00 del dia siguiente no puede abrir oficinas.
La respuesta debe ser completa pero ejecutiva para que la reciban los altos ejecutivos de la compañía
"""

#Notas
"""
HPBPROC = PCADENA no siempre tiene los mismos código HPBSEC por eso se filtra por descripción
Se debió quitar espacios en blanco al finalizar los tipo texto
el PBDESC  confundía al motor, se cambió por HPBDESC  y mejoró
Es necesario decir que de una respuesta ejecutivo o muestra todas las operaciones matemáticas

Para que arme bien el query debi subir a un modelo más completo 70B

Los filtros por fecha le generan error
"""
posfix=""
# Configuración del modelo
#llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
#grop_model = "gemma-7b-it"
grop_model ="llama3-groq-70b-8192-tool-use-preview"
llm = ChatGroq(model=grop_model, temperature=0)
agent_executor = create_pandas_dataframe_agent(
    llm,
    df,
    prefix= prefix,
    verbose=True,
    agent_type= 'tool-calling',
    allow_dangerous_code=True
    )








def get_response(user_input):
    response = agent_executor.invoke(user_input)
    return response.output

def main():
    user_input = ""
    while True:
        user_input=input("Ingrese la pregunta (/q para finalizar): \n")
        if user_input.startswith("/q"):
            break
        response = agent_executor.invoke(user_input)
        print(str(response["output"]))


if __name__ == "__main__":
    main()