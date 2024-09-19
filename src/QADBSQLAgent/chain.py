
from langchain_groq  import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit




#from langchain.agents import create_structured_chat_agent
import pandas as pd


from dotenv import load_dotenv

load_dotenv()

db =SQLDatabase.from_uri("sqlite:///data/sqlite/cierre.db")






prefix = """

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

prompt_template = PromptTemplate.from_template(prefix)
 




system_message = prompt_template.format(dialect="SQLite", top_k=5)

agent_executor = create_react_agent(
    llm, toolkit.get_tools(), state_modifier=system_message,debug=False
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

        inputs = {"messages": [("user", user_input)]}

        response = agent_executor.invoke(inputs)
        response[-1].pretty_print()


if __name__ == "__main__":
    main()