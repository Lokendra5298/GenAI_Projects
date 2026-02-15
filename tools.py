"""
Tools for LangGraph agents to analyze YouTube videos
"""
from typing import List, Dict, Optional, Any, Annotated
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


# Tool input schemas
class SearchTranscriptInput(BaseModel):
    """Input for searching transcript."""
    query: str = Field(description="The search query to find in the transcript")
    k: int = Field(default=4, description="Number of results to return")


class AnalyzeTopicInput(BaseModel):
    """Input for topic analysis."""
    topic: str = Field(description="The topic to analyze")
    aspect: Optional[str] = Field(default=None, description="Specific aspect to focus on")


class SummarizeSegmentInput(BaseModel):
    """Input for summarizing a segment."""
    start_time: Optional[float] = Field(default=None, description="Start time in seconds")
    end_time: Optional[float] = Field(default=None, description="End time in seconds")
    summary_type: str = Field(default="brief", description="Type of summary: brief, detailed, or bullet_points")


class QuestionAnswerInput(BaseModel):
    """Input for question answering."""
    question: str = Field(description="The question to answer")


class ExtractKeyPointsInput(BaseModel):
    """Input for extracting key points."""
    num_points: int = Field(default=5, description="Number of key points to extract")


class YouTubeTools:
    """Collection of tools for YouTube video analysis."""
    
    def __init__(self, vector_store_manager, llm_manager, transcript_data):
        """
        Initialize YouTube tools.
        
        Args:
            vector_store_manager: VectorStoreManager instance
            llm_manager: LLMManager instance
            transcript_data: VideoTranscript object
        """
        self.vsm = vector_store_manager
        self.llm = llm_manager
        self.transcript = transcript_data
        
        # Create retriever
        self.retriever = self.vsm.get_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
    
    @tool
    def search_transcript(query: str, k: int = 4) -> str:
        """
        Search the video transcript for relevant content.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            Relevant transcript segments
        """
        # This will be bound to instance method
        pass
    
    def _search_transcript_impl(self, query: str, k: int = 4) -> str:
        """Implementation of transcript search."""
        try:
            results = self.vsm.similarity_search(query, k=k)
            
            if not results:
                return "No relevant content found in the transcript."
            
            output = f"Found {len(results)} relevant segments:\n\n"
            for i, doc in enumerate(results, 1):
                output += f"Segment {i}:\n{doc.page_content}\n\n"
            
            return output
            
        except Exception as e:
            logger.error(f"Error searching transcript: {e}")
            return f"Error searching transcript: {str(e)}"
    
    def _analyze_topic_impl(self, topic: str, aspect: Optional[str] = None) -> str:
        """Implementation of topic analysis."""
        try:
            # Search for topic in transcript
            results = self.vsm.similarity_search(topic, k=5)
            
            if not results:
                return f"The topic '{topic}' is not discussed in this video."
            
            context = "\n\n".join([doc.page_content for doc in results])
            
            # Construct query
            if aspect:
                query = f"Analyze how {topic} is discussed in the video, specifically focusing on {aspect}."
            else:
                query = f"Analyze how {topic} is discussed in the video."
            
            # Generate analysis
            prompt = f"""Based on the following transcript segments:

{context}

{query}

Provide a detailed analysis including:
1. Whether and how the topic is covered
2. Key points made about the topic
3. Examples or evidence provided
4. Conclusions or implications discussed"""
            
            response = self.llm.generate(prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error analyzing topic: {e}")
            return f"Error analyzing topic: {str(e)}"
    
    def _answer_question_impl(self, question: str) -> str:
        """Implementation of question answering."""
        try:
            # Retrieve relevant context
            results = self.vsm.similarity_search(question, k=4)
            
            if not results:
                return "I don't have enough information in the transcript to answer this question."
            
            context = "\n\n".join([doc.page_content for doc in results])
            
            # Generate answer using RAG
            answer = self.llm.generate_with_context(
                query=question,
                context=context,
                system_message="You are a helpful assistant analyzing a YouTube video. Answer questions based only on the provided transcript context."
            )
            
            return answer
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return f"Error: {str(e)}"
    
    def _extract_key_points_impl(self, num_points: int = 5) -> str:
        """Implementation of key points extraction."""
        try:
            # Use full transcript or a representative sample
            text = self.transcript.full_text
            
            # Limit text length if too long
            max_length = 8000
            if len(text) > max_length:
                # Take beginning, middle, and end
                part_size = max_length // 3
                text = (
                    text[:part_size] + 
                    text[len(text)//2 - part_size//2:len(text)//2 + part_size//2] +
                    text[-part_size:]
                )
            
            prompt = f"""Analyze this video transcript and extract the {num_points} most important key points:

{text}

Provide exactly {num_points} key points in a numbered list. Each point should be:
- Clear and concise (1-2 sentences)
- Capture a main idea or important insight
- Be distinct from other points

Key Points:"""
            
            response = self.llm.generate(prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return f"Error: {str(e)}"
    
    def _summarize_segment_impl(
        self, 
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        summary_type: str = "brief"
    ) -> str:
        """Implementation of segment summarization."""
        try:
            # Extract segment
            if start_time is None and end_time is None:
                # Summarize entire video
                text = self.transcript.full_text
                segment_desc = "entire video"
            else:
                # Filter chunks by time
                segment_chunks = []
                for chunk in self.transcript.chunks:
                    chunk_end = chunk.start + chunk.duration
                    
                    if start_time is not None and chunk_end < start_time:
                        continue
                    if end_time is not None and chunk.start > end_time:
                        continue
                    
                    segment_chunks.append(chunk.text)
                
                if not segment_chunks:
                    return "No content found in the specified time range."
                
                text = " ".join(segment_chunks)
                segment_desc = f"segment from {start_time}s to {end_time}s"
            
            # Generate summary based on type
            if summary_type == "brief":
                prompt = f"Provide a brief 2-3 sentence summary of this {segment_desc}:\n\n{text}"
            elif summary_type == "detailed":
                prompt = f"Provide a detailed summary of this {segment_desc}, covering all main points:\n\n{text}"
            else:  # bullet_points
                prompt = f"Summarize this {segment_desc} as a bulleted list of key points:\n\n{text}"
            
            response = self.llm.generate(prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error summarizing segment: {e}")
            return f"Error: {str(e)}"
    
    def _find_timestamps_impl(self, search_text: str) -> str:
        """Implementation of finding timestamps."""
        try:
            results = []
            search_lower = search_text.lower()
            
            for chunk in self.transcript.chunks:
                if search_lower in chunk.text.lower():
                    # Format timestamp
                    minutes = int(chunk.start // 60)
                    seconds = int(chunk.start % 60)
                    timestamp = f"{minutes:02d}:{seconds:02d}"
                    
                    results.append({
                        'timestamp': timestamp,
                        'time_seconds': chunk.start,
                        'text': chunk.text
                    })
            
            if not results:
                return f"'{search_text}' was not found in the transcript."
            
            output = f"Found {len(results)} occurrence(s) of '{search_text}':\n\n"
            for i, result in enumerate(results, 1):
                output += f"{i}. [{result['timestamp']}] {result['text'][:100]}...\n"
            
            return output
            
        except Exception as e:
            logger.error(f"Error finding timestamps: {e}")
            return f"Error: {str(e)}"
    
    def _compare_topics_impl(self, topic1: str, topic2: str) -> str:
        """Implementation of topic comparison."""
        try:
            # Search for both topics
            results1 = self.vsm.similarity_search(topic1, k=3)
            results2 = self.vsm.similarity_search(topic2, k=3)
            
            context1 = "\n".join([doc.page_content for doc in results1]) if results1 else "Not discussed"
            context2 = "\n".join([doc.page_content for doc in results2]) if results2 else "Not discussed"
            
            prompt = f"""Compare and contrast how these two topics are discussed in the video:

Topic 1: {topic1}
Context: {context1}

Topic 2: {topic2}
Context: {context2}

Provide a comparison covering:
1. How each topic is presented
2. Similarities in their treatment
3. Differences in their discussion
4. Relationships between the topics (if any)"""
            
            response = self.llm.generate(prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error comparing topics: {e}")
            return f"Error: {str(e)}"
    
    def get_tool_list(self) -> List:
        """Get list of all available tools as LangChain tools."""
        
        @tool
        def search_transcript(query: str, k: int = 4) -> str:
            """Search the video transcript for content related to a query."""
            return self._search_transcript_impl(query, k)
        
        @tool
        def analyze_topic(topic: str, aspect: Optional[str] = None) -> str:
            """Analyze how a specific topic is discussed in the video."""
            return self._analyze_topic_impl(topic, aspect)
        
        @tool
        def answer_question(question: str) -> str:
            """Answer a question based on the video transcript."""
            return self._answer_question_impl(question)
        
        @tool
        def extract_key_points(num_points: int = 5) -> str:
            """Extract the main key points from the video."""
            return self._extract_key_points_impl(num_points)
        
        @tool
        def summarize_segment(
            start_time: Optional[float] = None,
            end_time: Optional[float] = None,
            summary_type: str = "brief"
        ) -> str:
            """Summarize a time segment of the video (or entire video if times not specified)."""
            return self._summarize_segment_impl(start_time, end_time, summary_type)
        
        @tool
        def find_timestamps(search_text: str) -> str:
            """Find timestamps where specific text or topic is mentioned."""
            return self._find_timestamps_impl(search_text)
        
        @tool
        def compare_topics(topic1: str, topic2: str) -> str:
            """Compare and contrast two topics discussed in the video."""
            return self._compare_topics_impl(topic1, topic2)
        
        return [
            search_transcript,
            analyze_topic,
            answer_question,
            extract_key_points,
            summarize_segment,
            find_timestamps,
            compare_topics
        ]


# Standalone tool functions for direct use
def create_tools(vector_store_manager, llm_manager, transcript_data) -> List:
    """
    Create and return a list of tools for YouTube analysis.
    
    Args:
        vector_store_manager: VectorStoreManager instance
        llm_manager: LLMManager instance
        transcript_data: VideoTranscript object
        
    Returns:
        List of LangChain tools
    """
    tools = YouTubeTools(vector_store_manager, llm_manager, transcript_data)
    return tools.get_tool_list()


if __name__ == "__main__":
    print("YouTube Tools module")
    print("This module provides tools for LangGraph agents to analyze YouTube videos")
    print("\nAvailable tools:")
    print("  - search_transcript: Search for content in the transcript")
    print("  - analyze_topic: Analyze how a topic is discussed")
    print("  - answer_question: Answer questions about the video")
    print("  - extract_key_points: Extract main points from the video")
    print("  - summarize_segment: Summarize a time segment")
    print("  - find_timestamps: Find when topics are mentioned")
    print("  - compare_topics: Compare two topics")
