"""Vector Store for Qualitative Financial Text"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from typing import List


class FinancialVectorStore:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize or load existing vector store"""
        try:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        except:
            self.vectorstore = Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
    
    def add_documents(self, documents: List[Document]):
        """Add documents to vector store"""
        if documents:
            self.vectorstore.add_documents(documents)
    
    def add_texts(self, texts: List[str], metadatas: List[dict] = None):
        """Add raw texts with metadata"""
        self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Search for similar documents"""
        return self.vectorstore.similarity_search(query, k=k)
    
    def search_with_score(self, query: str, k: int = 3):
        """Search with relevance scores"""
        return self.vectorstore.similarity_search_with_score(query, k=k)
