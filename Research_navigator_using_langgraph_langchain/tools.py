# tools.py
from langchain_core.tools import tool
from data_base import get_db
from rag import load_vector_store
import requests
from pypdf import PdfReader
from io import BytesIO
import json

@tool
def sql_filter(query: str) -> str:
    """Filters papers by category, author, or year using SQL."""
    db = get_db()
    # Simplified: assume query is a valid SQL WHERE clause
    sql = f"SELECT id, title FROM papers WHERE {query} LIMIT 10;"
    results = db.run(sql)
    return json.dumps(results)  # Return as stringified JSON

@tool
def vector_rag_search(query: str, top_k: int = 5) -> str:
    """Semantic search on paper abstracts."""
    vectorstore = load_vector_store()
    results = vectorstore.similarity_search(query, k=top_k)
    return json.dumps([{ "id": doc.metadata["id"], "abstract": doc.page_content } for doc in results])

@tool
def fetch_pdf_texts(ids: list[str], max_pdfs: int = 10) -> str:
    """Scrapes and extracts text from up to 10 ArXiv PDFs."""
    texts = []
    for id_ in ids[:max_pdfs]:
        url = f"https://arxiv.org/pdf/{id_}.pdf"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                pdf = PdfReader(BytesIO(response.content))
                text = "".join(page.extract_text() or "" for page in pdf.pages)
                texts.append(f"Paper {id_}: {text[:50000]}")  # Truncate
        except Exception:
            pass
    return "\n\n".join(texts)