
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
La columna DURACION tiene el total de segundos de ejecución, se puede sumar para saber el tiempo total
La preguntas de duración respndela en horas, minutos y segundos.
El proceso inicia con la tarea identificada por DESCRIPCION_TAREA='Inhabilita accesos al menu', 
el INICIO de esta tarea es inicio del proceso de cierre.
El fin del proceso de cierre se da al finalizar la tarea con CODIGO_TAREA=OCIE1000.
Si la tarea identificadas con DESCRIPCION_TAREA='Habilita accesos al menu'
finaliza después de las 08:00:00 del dia siguiente a la fecha de cierre no se pueden abrir oficinas a tiempo
Para saber la duracion de todo el proceso suma los segundos de todas las tareas para la FECHA_CIERRE
Para saber la duracion sin pausas suma todas las tareas con CODIGO_TAREA != PAUSA
La respuesta debe ser completa pero ejecutiva en español para que la reciban los altos ejecutivos de la compañía
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
    inputs = {"messages": [("user", user_input)]}
    response = agent_executor.stream(inputs)
    for s in response:
        for key in s.keys():
            message=s[key]['messages'][-1]
    
    if isinstance(message,tuple):
        return(message[1])
    else:
        return message.content
           

def main():
    user_input = ""
    while True:
        user_input=input("Ingrese la pregunta (/q para finalizar): \n")
        if user_input.startswith("/q"):
            break

        inputs = {"messages": [("user", user_input)]}

        response = agent_executor.stream(inputs)
        for s in response:
            for key in s.keys():
                message=s[key]['messages'][-1]
                if isinstance(message,tuple):
                    print(message)
                else:
                    message.pretty_print()
           


"""
        if isinstance(message, str):
            print(message)
        elif isinstance(message, ChatMessage):
            message.pretty_print()
        else:
            print(f"ERROR: Unknown type - {type(message)}")
"""



if __name__ == "__main__":
    main()