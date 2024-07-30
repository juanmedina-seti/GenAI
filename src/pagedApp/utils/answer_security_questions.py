import os
from langchain_community.vectorstores.chroma import Chroma
from src.shared.get_embedding_function import get_embedding_function
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.llm import LLMChain

from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file

chroma_path = os.environ.get("CHROMA_PATH")
PROMPT_TEMPLATE = """
Eres un analista de seguridad de la compañía llamada SETI, debes responder unas 
preguntas de seguridad a un cliente, anteriormente se han respondido las siguientes
preguntas similares así:

{context}

---

Ahora basado en las pregunta anteriores responde esta: {question}
"""


def previous_answers(query_text:str) -> list[any]:
    db = Chroma(persist_directory=chroma_path, embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(query_text, k=2)
    
    return [doc.page_content for doc, _score in results]

def new_answer(query_text:str, results: list[any]) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    chain = LLMChain(llm=llm, 
                     prompt=PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"]))
    context_text = "\n\n---\n\n".join( results)
    response_text=chain.invoke(input={"context":context_text, "question": query_text})
    return response_text["text"]

def main():
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    chain = LLMChain(llm=llm, 
                     prompt=PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"]))
        
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

    while True:
        query_text=input("Ingrese la pregunta (q para salir):")
        if query_text == "q":
            break
        results = db.similarity_search_with_score(query_text, k=2)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = "\n\n---\n\n".join([f"{doc.metadata["filename"]}:{doc.metadata["line_number"]}:" for doc, _score in results])
        print("\n\n##################################")
        print("###### Preguntas similares #######")
        print("##################################")
        print(context_text)
        print("###### Fuentes #######")
        print(sources)
        print("##################################")
        


        while True:
            redactar= input("\nQuiere redactar una nueva respuesta (s/n):")
            if redactar == "s":
                #prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
                response_text=chain.invoke(input={"context":context_text, "question": query_text})
                
                print("\n\n##################################")
                print("###### Nueva Respuesta #######")
                print(response_text["text"])   
                break
            elif redactar == "n":
                break


if __name__ == "__main__":
    main()