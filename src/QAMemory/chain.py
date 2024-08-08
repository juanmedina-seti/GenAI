from langchain_core.prompts import  PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


from dotenv import load_dotenv

# Configuración del modelo
llm = ChatGoogleGenerativeAI(model="gemini-pro")


# Plantillas de prompt
def create_prompt(history, user_input):
    prompt_template = """
    Eres un asistente muy útil. Aquí está el historial de la conversación
  
    {history}
    Pregunta actual: {user_input}
    
    Respuesta:
    """
    return PromptTemplate(template=prompt_template, input_variables=["history", "user_input"])

class ChatMemory:
    def __init__(self):
        self.history = []

    def add_entry(self, user_input, response):
        self.history.append(f"Usuario: {user_input}")
        self.history.append(f"Asistente: {response}")

    def get_history(self):
        return "\n".join(self.history)

# Crear la cadena de LLM con memoria
memory = ChatMemory()

def get_response(user_input):
    prompt = create_prompt(memory.get_history(), user_input)
    llm_chain = prompt|llm
    
    response = llm_chain.invoke({"history": memory.get_history(), "user_input": user_input})
    print(response)
    memory.add_entry(user_input, response.content)
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