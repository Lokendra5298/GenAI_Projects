"""
Vector store module for semantic search and retrieval
"""
from typing import List, Dict, Optional, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import pickle
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Manages vector embeddings and similarity search."""
    
    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize vector store manager.
        
        Args:
            embedding_model: Name of the HuggingFace embedding model
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.embedding_model_name = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize embeddings
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        self.vector_store = None
        self.documents = []
    
    def create_vector_store(
        self, 
        text: str, 
        metadata: Optional[Dict] = None
    ) -> FAISS:
        """
        Create a vector store from text.
        
        Args:
            text: Input text to embed
            metadata: Optional metadata to attach to documents
            
        Returns:
            FAISS vector store
        """
        try:
            logger.info("Creating vector store from text")
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            logger.info(f"Split text into {len(chunks)} chunks")
            
            # Create documents with metadata
            self.documents = []
            for i, chunk in enumerate(chunks):
                doc_metadata = metadata.copy() if metadata else {}
                doc_metadata.update({
                    'chunk_id': i,
                    'chunk_size': len(chunk)
                })
                
                doc = Document(
                    page_content=chunk,
                    metadata=doc_metadata
                )
                self.documents.append(doc)
            
            # Create vector store
            self.vector_store = FAISS.from_documents(
                self.documents,
                self.embeddings
            )
            
            logger.info(f"Vector store created with {len(self.documents)} documents")
            return self.vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def create_from_chunks(
        self, 
        chunks: List[str], 
        metadatas: Optional[List[Dict]] = None
    ) -> FAISS:
        """
        Create vector store from pre-split chunks.
        
        Args:
            chunks: List of text chunks
            metadatas: Optional list of metadata dictionaries
            
        Returns:
            FAISS vector store
        """
        try:
            logger.info(f"Creating vector store from {len(chunks)} chunks")
            
            # Create documents
            self.documents = []
            for i, chunk in enumerate(chunks):
                metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
                metadata['chunk_id'] = i
                
                doc = Document(
                    page_content=chunk,
                    metadata=metadata
                )
                self.documents.append(doc)
            
            # Create vector store
            self.vector_store = FAISS.from_documents(
                self.documents,
                self.embeddings
            )
            
            logger.info(f"Vector store created with {len(self.documents)} documents")
            return self.vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        score_threshold: Optional[float] = None
    ) -> List[Document]:
        """
        Perform similarity search.
        
        Args:
            query: Query text
            k: Number of results to return
            score_threshold: Minimum similarity score (0-1)
            
        Returns:
            List of most similar documents
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return []
        
        try:
            if score_threshold is not None:
                # Search with score filtering
                results = self.vector_store.similarity_search_with_score(query, k=k*2)
                filtered_results = [
                    doc for doc, score in results 
                    if score >= score_threshold
                ][:k]
                return filtered_results
            else:
                # Regular search
                results = self.vector_store.similarity_search(query, k=k)
                return results
                
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def similarity_search_with_scores(
        self, 
        query: str, 
        k: int = 4
    ) -> List[Tuple[Document, float]]:
        """
        Perform similarity search and return scores.
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search with scores: {e}")
            return []
    
    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5
    ) -> List[Document]:
        """
        Perform MMR search for diverse results.
        
        Args:
            query: Query text
            k: Number of results to return
            fetch_k: Number of candidates to fetch
            lambda_mult: Diversity parameter (0=max diversity, 1=max relevance)
            
        Returns:
            List of diverse relevant documents
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return []
        
        try:
            results = self.vector_store.max_marginal_relevance_search(
                query, 
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult
            )
            return results
            
        except Exception as e:
            logger.error(f"Error in MMR search: {e}")
            return []
    
    def get_retriever(
        self,
        search_type: str = "similarity",
        search_kwargs: Optional[Dict] = None
    ):
        """
        Get a retriever interface for the vector store.
        
        Args:
            search_type: Type of search ('similarity', 'mmr', 'similarity_score_threshold')
            search_kwargs: Additional search parameters
            
        Returns:
            Retriever object
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return None
        
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        
        return self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
    
    def save_vector_store(self, path: str):
        """
        Save vector store to disk.
        
        Args:
            path: Directory path to save to
        """
        if not self.vector_store:
            logger.error("No vector store to save")
            return
        
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            self.vector_store.save_local(path)
            
            # Save metadata
            metadata = {
                'embedding_model': self.embedding_model_name,
                'chunk_size': self.chunk_size,
                'chunk_overlap': self.chunk_overlap,
                'num_documents': len(self.documents)
            }
            
            with open(Path(path) / "metadata.pkl", "wb") as f:
                pickle.dump(metadata, f)
            
            logger.info(f"Vector store saved to {path}")
            
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
    
    def load_vector_store(self, path: str) -> bool:
        """
        Load vector store from disk.
        
        Args:
            path: Directory path to load from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load FAISS index
            self.vector_store = FAISS.load_local(
                path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            # Load metadata
            metadata_path = Path(path) / "metadata.pkl"
            if metadata_path.exists():
                with open(metadata_path, "rb") as f:
                    metadata = pickle.load(f)
                    logger.info(f"Loaded vector store: {metadata}")
            
            logger.info(f"Vector store loaded from {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return False
    
    def add_documents(self, documents: List[Document]):
        """
        Add more documents to existing vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return
        
        try:
            self.vector_store.add_documents(documents)
            self.documents.extend(documents)
            logger.info(f"Added {len(documents)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
    
    def delete_by_metadata(self, metadata_filter: Dict):
        """
        Delete documents matching metadata filter.
        
        Args:
            metadata_filter: Metadata to match for deletion
        """
        # Note: FAISS doesn't support native deletion
        # This would require recreating the index without matching docs
        logger.warning("Document deletion requires recreating the index")
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with statistics
        """
        if not self.vector_store:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'num_documents': len(self.documents),
            'embedding_model': self.embedding_model_name,
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'total_chunks': len(self.documents),
            'avg_chunk_size': sum(len(doc.page_content) for doc in self.documents) / len(self.documents) if self.documents else 0
        }


class HybridRetriever:
    """Combines semantic and keyword search."""
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        """
        Initialize hybrid retriever.
        
        Args:
            vector_store_manager: VectorStoreManager instance
        """
        self.vsm = vector_store_manager
    
    def retrieve(
        self, 
        query: str, 
        k: int = 4,
        semantic_weight: float = 0.7
    ) -> List[Document]:
        """
        Hybrid retrieval combining semantic and keyword search.
        
        Args:
            query: Query text
            k: Number of results
            semantic_weight: Weight for semantic search (0-1)
            
        Returns:
            List of retrieved documents
        """
        # Get semantic results
        semantic_results = self.vsm.similarity_search_with_scores(query, k=k*2)
        
        # Simple keyword matching
        query_lower = query.lower()
        keyword_scores = {}
        
        for doc in self.vsm.documents:
            score = 0
            doc_lower = doc.page_content.lower()
            
            # Count query term occurrences
            for term in query_lower.split():
                if len(term) > 3:  # Skip short words
                    score += doc_lower.count(term)
            
            if score > 0:
                keyword_scores[doc] = score
        
        # Combine scores
        combined_scores = {}
        
        # Add semantic scores
        for doc, score in semantic_results:
            combined_scores[doc] = semantic_weight * (1 - score)  # Convert distance to similarity
        
        # Add keyword scores
        max_keyword_score = max(keyword_scores.values()) if keyword_scores else 1
        for doc, score in keyword_scores.items():
            normalized_score = score / max_keyword_score
            if doc in combined_scores:
                combined_scores[doc] += (1 - semantic_weight) * normalized_score
            else:
                combined_scores[doc] = (1 - semantic_weight) * normalized_score
        
        # Sort and return top k
        sorted_docs = sorted(
            combined_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [doc for doc, score in sorted_docs[:k]]


if __name__ == "__main__":
    # Test vector store
    print("Testing Vector Store Manager...")
    
    vsm = VectorStoreManager()
    
    # Sample text
    sample_text = """
    Artificial intelligence is transforming the world. Machine learning algorithms
    can now recognize patterns in data with incredible accuracy. Deep learning,
    a subset of machine learning, uses neural networks with multiple layers.
    Natural language processing allows computers to understand human language.
    Computer vision enables machines to interpret visual information.
    """
    
    # Create vector store
    vsm.create_vector_store(sample_text, metadata={'source': 'test'})
    
    # Test search
    query = "What is deep learning?"
    results = vsm.similarity_search(query, k=2)
    
    print(f"\nQuery: {query}")
    print(f"Found {len(results)} results:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.page_content[:100]}...")
    
    # Test stats
    stats = vsm.get_stats()
    print(f"\nVector Store Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
