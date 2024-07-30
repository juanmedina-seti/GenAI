from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain

# Configuración del modelo
openai_api_key = "tu_clave_de_api_aqui"
llm = OpenAI(api_key=openai_api_key)

# Plantillas de prompt
def create_prompt(history, user_input):
    prompt_template = """
    Eres un asistente muy útil. Aquí está el historial de la conversación:
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
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    response = llm_chain.run({"history": memory.get_history(), "user_input": user_input})
    memory.add_entry(user_input, response)
    return response
