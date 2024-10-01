from datetime import date
from langchain_groq  import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
from sqlalchemy import text



from dotenv import load_dotenv

load_dotenv()


engine = create_engine("sqlite:///data/sqlite/cierre.db")


def obtener_datos_por_proceso_de_cierre() ->str:
    """Retorna los datos del proceso de cierre para todas las fechas disponibles específica en formato json
        con los siguientes campos:
               FECHA_CIERRE: fecha del cierre
               DURACION_TOTAL: duración de todo el proceso de cierre de cada fecha
               DURACION_SIN_PAUSAS: duración de las tareas de cierre sin contar las pausas
               INICIO_CIERRE: Fecha y hora de inicio del cierre
               FIN_CIERRE: Fecha y hora de fin de todo del cierre
               HORA_HABILITAR_MENU: Fecha y hora en que finalizó la tarea de habilitar menú lo que permite abrir oficinas
        Args:
            fecha_cierre: fecha de cierre, Opcional. 
    """
    query= """select FECHA_CIERRE, TIME(SUM( DURACION), 'unixepoch') as DURACION_TOTAL_CIERRE,  TIME(SUM(IIF(CODIGO_TAREA=='PAUSA',0,DURACION)),'unixepoch') AS DURACION_CIERRE_SIN_PAUSAS,
            DATETIME( min(INICIO)) as INICIO_CIERRE, DATETIME( max(FIN)) as FIN_CIERRE, DATETIME(MAX(IIF(DESCRIPCION_TAREA='Habilita accesos al menu',FIN,0))) AS FECHA_HABILITAR_MENU
            from Cierre 
            WHERE FECHA_CIERRE IS NOT NULL
            group by FECHA_CIERRE """
    
    context= "["
    with engine.connect() as connection:
        result = connection.execute(text(query))
        for row in result:
            context += f'{{"FECHA_CIERRE":"{row[0]},"DURACION_TOTAL":"{row[1]}", "DURACION_SIN_PAUSAS":"{row[2]}", "INICIO_CIERRE":"{row[3]}", "FIN_CIERRE":"{row[4]}", HORA_HABILITAR_MENU="{row[5]}"}}, '
    context += "]"
    return context


def obtener_datos_tareas_y_pausas_por_fecha(fecha_cierre:date) ->str:
    """Retorna los detalles de tareas y pausas del cierre para una fecha específica
        los datos disponibles enen formato json son:
               FECHA_CIERRE: fecha del cierre
               DURACION: duración de la tarea en ejecución
               INICIO: Fecha y hora de inicio de la tarea
               FIN: Fecha y hora de fin de la tarea
               CODIGO_TAREA: Identificador de la tarea
               DESCRIPCION_TAREA: Descripción que complementa el código de la tarea
        Args:
            fecha_cierre: fecha de cierre 
    """
    query= """select FECHA_CIERRE, TIME( DURACION, 'unixepoch') as DURACION, CODIGO_TAREA, DESCRIPCION_TAREA,
                DATETIME(INICIO) as INICIO, DATETIME( FIN) as FIN
                from Cierre 
                WHERE FECHA_CIERRE = """
    query += "'" + fecha_cierre.strftime("%Y-%m-%d") + "'"
        
    context= "["
    with engine.connect() as connection:
        result = connection.execute(text(query))
        for row in result:
            context += f'{{"FECHA_CIERRE":"{row[0]},"DURACION":"{row[1]}", "CODIGO_TAREA":"{row[2]}", "DESCRIPCION_TAREA":"{row[3]}", "INICIO":"{row[4]}", FIN="{row[5]}"}}, '
    context += "]"
    return context



# Configuración del modelo
#llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
#grop_model = "gemma-7b-it"
grop_model ="llama3-groq-70b-8192-tool-use-preview"
llm = ChatGroq(model=grop_model, temperature=0,verbose=True)

tools=[obtener_datos_por_proceso_de_cierre, obtener_datos_tareas_y_pausas_por_fecha]

chat_history=""





system_message = """"Eres un asistente muy útil. Por favor entraga solamente la respuesta a la pregunta de manera concreta.
               con las herramientas disponibles puedes consultar las últimas fechas de cierre con datos registrados
            """

agent_executor = create_react_agent(
    llm, tools=tools, state_modifier=system_message,debug=False
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