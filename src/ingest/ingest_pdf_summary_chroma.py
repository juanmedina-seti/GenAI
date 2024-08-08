import argparse
import shutil
from langchain_community.vectorstores import Chroma
from langchain.schema.document import Document
#from get_embedding_function import get_embedding_function
from src.shared.get_embedding_function import get_embedding_function
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import PyPDFLoader

#from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate





from dotenv import load_dotenv
import os
import glob

load_dotenv()  # Load the .env file

chroma_path = os.environ.get("VECTORDB_DBA")
dba_pdfs_path = os.environ.get("DBA_PDF_PATH")

def format_docs(pages: list[Document]):
    return "\n\n".join(doc.page_content for doc in pages)



# Configuración del modelo
llm = ChatGroq(model="mixtral-8x7b-32768")
prompt = PromptTemplate.from_template("resume el siguiente documento teniendo en cuenta su objetivo, motor de base de datos utilizado: {doc}")
#chain_summary =   { "doc":format_docs }    |prompt | llm 
chain_summary =  prompt | llm 

def main():

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    docs_summaries = load_documents()
    add_to_chroma(docs_summaries)


def load_documents():
    summaries : list[Document] =[]
    for pdf_file in glob.glob(dba_pdfs_path+"/*.pdf") :
        document_loader : PyPDFLoader = PyPDFLoader(pdf_file)
        pages= document_loader.load()
        summary= summarize_documents(pages)
        summaries.append(summary)
    
    return summaries


def summarize_documents(pages: list[Document]):

    #text = [p.page_content for p in pages]
    #text= str.join(text,"/n")
    text= format_docs(pages[0:19])
    print(f"text length = {len(text)}")

    summary = chain_summary.invoke ({"doc":text})
    print(summary)
    document=Document(page_content = summary.content,metadata=pages[0].metadata)

                
    return document


def add_to_chroma(docs: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=chroma_path, embedding_function=get_embedding_function()
    )
 
    db.add_documents(docs)






def clear_database():
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)


if __name__ == "__main__":
    main()
