from langchain_core.prompts import  ChatPromptTemplate
from langchain_groq import ChatGroq

from langchain_community.chat_message_histories import ChatMessageHistory


from dotenv import load_dotenv

# Configuración del modelo
llm = ChatGroq(model="mixtral-8x7b-32768")

#Clase para gestionar memoria

history = ChatMessageHistory()


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un asistente muy útil. Aquí está el historial de la conversación",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)

chain = prompt | llm

from langchain_core.runnables.history import RunnableWithMessageHistory


chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


def get_history() -> ChatMessageHistory:
    return history
    

def get_response(user_input):

    
    response =chain_with_message_history.invoke(
        {"input": user_input},
        {"configurable": {"session_id": "unused"}}
    )
    print(response)
    return response.content


def main():
    user_input = ""
    while True:
        user_input=input("Ingrese la pregunta (/q para finalizar)")
        if user_input.startswith("/q"):
            break
        response = get_response(user_input)
        print(response)


if __name__ == "__main__":
    main()