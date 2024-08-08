#program with all the information to read an excel file, create embedding with gemini and populate a Chroma vector database with documents and metadata from each row of the excel
import shutil
from icecream import ic
import pandas as pd
import azure.identity
#from langchain.vectorstores.chroma import Chroma
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain.schema.document import Document
#from get_embedding_function import get_embedding_function
from src.shared.get_embedding_function import get_embedding_function


from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file
vector_store_address = os.environ.get("AZURE_SEARCH_SERVICE")
vector_store_key = os.environ.get("AZURE_SEARCH_KEY")
embedding_model = os.environ.get("EMBEDDING_MODEL_QA")
#chroma_path = os.environ.get("CHROMA_PATH")

excel_file_path = os.environ.get("EXCEL_FILE_PATH")

# Connect to the Chroma database")

PROMPT_TEMPLATE = """
Eres un analista de seguridad de la compañía llamada SETI, debes responder unas 
preguntas de seguridad a un cliente, anteriormente se han respondido las siguientes
preguntas similares así:

{context}

---

Ahora basado en las pregunta anteriores responde esta: {question}
"""



def main():
    # Create (or update) the data store.
    #clear_database()
    documents, ids = get_excel_data()

    add_to_vectorstore(documents, ids)



# Connect to the Chroma database

def get_excel_data():
# Read the excel file
    df = pd.read_excel(excel_file_path)
    ic(df.head())
    documents=[]
    ids=[]
# Iterate over each row of the excel file
    for index, row in df.iterrows():

        # Create a document with the text from the excel row
        ic(f"{index}:{str(row["Pregunta"])}|||{str(row["Detalle"])}")
        
        # Create metadata with the information from the excel row


        # Add the document and metadata to the database
        #not pd.isna(row["Pregunta"]) and 
        if           len(str(row["Pregunta"]) )> 30:
            documents.append(Document(page_content=str(f"Pregunta: {str(row['Pregunta'])} ||| Respuesta: {str(row['Detalle'])}"),
                            metadata={"filename": excel_file_path, "line_number": index,"categoria":row["Categoria"],"tema":row["Tema"],"cliente":row["Cliente"],"fecha":str(row["Fecha"] )}
                           ))
            ids.append(str(index+1))
    return documents, ids
        


def add_to_vectorstore(documents, ids):
    # Load the existing database.

   
    index_name: str = "idx_security_survey"
    vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=vector_store_key,
        index_name=index_name,
        embedding_function=get_embedding_function(embedding_model),
        #token_provider = token_provider
    )

    # Load the documents in batches of 100
    for i in       range(0, len(documents), 30):
        print(f"{i} docs de {len(documents)}")
        vector_store.add_documents(
            documents=documents[i : i + 30],
            ids=ids[i : i + 30]
           # metadatas=metadatas[i : i + 100],  # type: ignore
        )

   # new_count = len(vector_store.get(include=[]))

    #print(f"Added {new_count - count} documents")
    





if __name__ == "__main__":
    main()
