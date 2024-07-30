from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain

# Configuración del modelo
openai_api_key = "tu_clave_de_api_aqui"
llm = OpenAI(api_key=openai_api_key)

# Plantillas de prompt
prompt_template = """
Eres un asistente muy útil. El usuario te hará preguntas, y debes responderlas con precisión y claridad.
Pregunta: {user_input}
Respuesta:
"""

# Crear la cadena de LLM
prompt = PromptTemplate(template=prompt_template, input_variables=["user_input"])
llm_chain = LLMChain(llm=llm, prompt=prompt)

def get_response(user_input):
    response = llm_chain.run({"user_input": user_input})
    return response
