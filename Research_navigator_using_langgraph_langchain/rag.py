# rag.py
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import pandas as pd
from llm import get_embeddings
import os

VECTOR_STORE_PATH = "arxiv_faiss_index"

def build_vector_store(df: pd.DataFrame):
    embeddings = get_embeddings()
    docs = [Document(page_content=row['abstract'], metadata={"id": row['id']}) for _, row in df.iterrows()]
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(VECTOR_STORE_PATH)
    return vectorstore

def load_vector_store():
    if os.path.exists(VECTOR_STORE_PATH):
        return FAISS.load_local(VECTOR_STORE_PATH, get_embeddings(), allow_dangerous_deserialization=True)
    raise ValueError("Vector store not found. Build it first.")