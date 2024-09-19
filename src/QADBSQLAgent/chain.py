
from langchain_groq  import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit




#from langchain.agents import create_structured_chat_agent
import pandas as pd


from dotenv import load_dotenv

load_dotenv()

db =SQLDatabase.from_uri("sqlite:///data/sqlite/cierre.db")






prefix = """

Eres un agente diseñado para interactuar con una base de datos SQL.
Dada una pregunta de entrada, debes analizar que datos requieres para responder y cree la consulta de {dialect} sintácticamente correcta para ejecutar, luego mire los resultados de la consulta y devuelva la respuesta.
A menos que el usuario especifique una cantidad específica de ejemplos que desea obtener, limite siempre su consulta a un máximo de {top_k} resultados.

Puede ordenar los resultados por una columna relevante para devolver los ejemplos más interesantes de la base de datos.
Nunca consulte todas las columnas de una tabla específica, solo solicite las columnas relevantes según la pregunta.
Tienes acceso a herramientas para interactuar con la base de datos.

Utilice únicamente las siguientes herramientas. Utilice únicamente la información devuelta por las siguientes herramientas para construir su respuesta final.
DEBE verificar su consulta antes de ejecutarla. Si recibe un error al ejecutar una consulta, vuelva a escribir la consulta y vuelva a intentarlo.
NO realice ninguna declaración DML (INSERT, UPDATE, DELETE, DROP, etc.) en la base de datos.
Para comenzar SIEMPRE debes mirar las tablas de la base de datos para ver qué puedes consultar.

NO te saltes este paso.
La tabla con la que interactuas es cierre. La cual contiene registros de las tareas realizadas para el proceso de cierre
La FECHA_CIERRE indica la fecha del día sobre el que se ejecuta el proceso de cierre. TODAS las tareas con la misma FECHA_CIERRE son parte del mismo cierre
Cada tarea está identificada por el CODIGO_TAREA y DESCRIPCION_TAREA. 
Cada tarea tiene INICIO y FIN que contienen la fecha y hora de inicio y fin de la ejecución
DURACION es la duración de le ejecución en segundos
El proceso inicia con la tarea identificada por HPBDESC='Inhabilita accesos al menu', 
el INICIO de esta tarea es inicio del proceso de cierre.
El fin del proceso de cierre se da al finalizar la tarea con CODIGO_TAREA=OCIE1000.
Si esta proceso Finaliza despues de la 08:00:00 es un afectación que no permite abrir oficinas.
La respuesta debe ser completa pero ejecutiva para que la reciban los altos ejecutivos de la compañía
"""



# Configuración del modelo
#llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
#grop_model = "gemma-7b-it"
grop_model ="llama3-groq-70b-8192-tool-use-preview"
llm = ChatGroq(model=grop_model, temperature=0,verbose=True)


toolkit = SQLDatabaseToolkit(db=db, llm=llm)
chat_history=""

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            prefix
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
    
)




system_message = prompt_template.format_prompt(dialect="SQLite", top_k=5)
agent_executor = create_react_agent(
    llm, toolkit.get_tools(), state_modifier=system_message,debug=True
)


def get_response(user_input):
    response = agent_executor.invoke({"input":user_input})
    return response.output

def main():
    user_input = ""
    while True:
        user_input=input("Ingrese la pregunta (/q para finalizar): \n")
        if user_input.startswith("/q"):
            break
        response = agent_executor.invoke({"input":user_input})
        print(str(response))


if __name__ == "__main__":
    main()