from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300, length_function=len)
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./project_work/chroma_db", embedding_function=embedding_model)

def load_documents(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            print(f"Unsupported file type: {filename}")
            continue
        Documents = splits(loader.load(),filename)
        print(f'no of documents = {len(Documents)}')
        vectorstore.add_documents(Documents)

        return True
    
    

def splits(Documents,file_name):
    splits= text_splitter.split_documents(Documents)
    for split in splits:
        split.metadata['file_name'] = file_name

    return splits

def load_db():
    global vectorstore 
    vectorstore = Chroma(persist_directory="./project_work/chroma_db", embedding_function=embedding_model)

