# llm.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

API_KEY = os.getenv("GOOGLE_API_KEY")

def get_gemini_model():
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=API_KEY,
        temperature=0.7
    )

def get_embeddings():
    """
    Returns a local sentence-transformers embedding model.
    Downloads ~80 MB model on first run, then works offline.
    """
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}

    )
