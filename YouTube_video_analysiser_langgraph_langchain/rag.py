"""
Retrieval-Augmented Generation (RAG) system for YouTube video analysis
"""
from typing import List, Dict, Optional, Any
from langchain.docstore.document import Document
import logging

logger = logging.getLogger(__name__)


class RAGSystem:
    """Complete RAG system for video analysis."""
    
    def __init__(self, vector_store_manager, llm_manager):
        """
        Initialize RAG system.
        
        Args:
            vector_store_manager: VectorStoreManager instance
            llm_manager: LLMManager instance
        """
        self.vsm = vector_store_manager
        self.llm = llm_manager
        self.retriever = None
        
        if self.vsm.vector_store:
            self.retriever = self.vsm.get_retriever()
    
    def query(
        self, 
        question: str, 
        k: int = 4,
        search_type: str = "similarity"
    ) -> Dict[str, Any]:
        """
        Query the RAG system.
        
        Args:
            question: User question
            k: Number of documents to retrieve
            search_type: Type of search ('similarity', 'mmr')
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        if not self.retriever:
            return {
                'answer': "RAG system not initialized. Please load a video first.",
                'sources': [],
                'confidence': 0.0
            }
        
        try:
            # Retrieve relevant documents
            if search_type == "mmr":
                docs = self.vsm.max_marginal_relevance_search(question, k=k)
            else:
                docs = self.vsm.similarity_search(question, k=k)
            
            if not docs:
                return {
                    'answer': "No relevant information found in the transcript.",
                    'sources': [],
                    'confidence': 0.0
                }
            
            # Format context from retrieved documents
            context = self._format_context(docs)
            
            # Generate answer
            answer = self.llm.generate_with_context(
                query=question,
                context=context,
                system_message="You are an expert assistant analyzing YouTube video transcripts. Provide accurate, detailed answers based on the given context."
            )
            
            # Calculate confidence (simple heuristic based on number of sources)
            confidence = min(len(docs) / k, 1.0)
            
            return {
                'answer': answer,
                'sources': docs,
                'context': context,
                'confidence': confidence,
                'num_sources': len(docs)
            }
            
        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            return {
                'answer': f"Error processing query: {str(e)}",
                'sources': [],
                'confidence': 0.0
            }
    
    def summarize(
        self,
        summary_type: str = "comprehensive",
        max_length: Optional[int] = None
    ) -> str:
        """
        Generate a summary of the video.
        
        Args:
            summary_type: Type of summary ('brief', 'comprehensive', 'bullet_points')
            max_length: Maximum length of summary
            
        Returns:
            Summary text
        """
        try:
            # Get representative chunks
            all_docs = self.vsm.documents
            
            if not all_docs:
                return "No content available to summarize."
            
            # Sample documents for summary (to stay within token limits)
            if len(all_docs) > 10:
                # Take beginning, middle, and end
                sample_docs = (
                    all_docs[:4] +
                    all_docs[len(all_docs)//2-2:len(all_docs)//2+2] +
                    all_docs[-4:]
                )
            else:
                sample_docs = all_docs
            
            context = self._format_context(sample_docs)
            
            # Generate summary based on type
            if summary_type == "brief":
                prompt = f"""Provide a brief 2-3 paragraph summary of this video:

{context}

Summary:"""
            
            elif summary_type == "bullet_points":
                prompt = f"""Create a bullet-point summary of this video's main points:

{context}

Provide 7-10 key points in bullet format."""
            
            else:  # comprehensive
                prompt = f"""Provide a comprehensive summary of this video, covering:
1. Main topic and purpose
2. Key points and arguments
3. Important details and examples
4. Conclusions or takeaways

Video content:
{context}

Summary:"""
            
            summary = self.llm.generate(prompt)
            
            # Truncate if needed
            if max_length and len(summary) > max_length:
                summary = summary[:max_length] + "..."
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"Error generating summary: {str(e)}"
    
    def _format_context(self, documents: List[Document]) -> str:
        """
        Format documents into context string.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Formatted context string
        """
        if not documents:
            return ""
        
        return "\n\n---\n\n".join([doc.page_content for doc in documents])
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG system.
        
        Returns:
            Dictionary with statistics
        """
        stats = self.vsm.get_stats()
        stats['retriever_available'] = self.retriever is not None
        return stats
