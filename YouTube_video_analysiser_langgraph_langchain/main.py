"""
Main module that integrates all components of the YouTube Analysis System
"""
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path

from data_loader import YouTubeDataLoader, VideoTranscript
from vectorstore import VectorStoreManager
from llm import LLMManager, PromptManager
from rag import RAGSystem
from tools import create_tools
from agent import create_agent, VideoAnalysisAgent
from database import VideoDatabase
from utils import extract_video_id, setup_environment

logger = logging.getLogger(__name__)


class YouTubeAnalysisSystem:
    """Main system integrating all components."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        db_path: str = "youtube_analysis.db",
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "gemini-2.0-flash-exp",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize the YouTube Analysis System.
        
        Args:
            api_key: Google API key
            db_path: Path to SQLite database
            embedding_model: Name of embedding model
            llm_model: Name of LLM model
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        logger.info("Initializing YouTube Analysis System")
        
        # Initialize components
        self.data_loader = YouTubeDataLoader()
        self.vector_store_manager = VectorStoreManager(
            embedding_model=embedding_model,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.llm_manager = LLMManager(
            api_key=api_key,
            model_name=llm_model,
            temperature=0.3
        )
        self.database = VideoDatabase(db_path)
        
        # These will be initialized when a video is loaded
        self.current_video_id = None
        self.current_transcript = None
        self.rag_system = None
        self.agent = None
        self.tools = None
        
        logger.info("System initialized successfully")
    
    def load_video(self, video_url_or_id: str) -> Dict[str, Any]:
        """
        Load and process a YouTube video.
        
        Args:
            video_url_or_id: YouTube URL or video ID
            
        Returns:
            Dictionary with load status and metadata
        """
        try:
            # Extract video ID
            video_id = extract_video_id(video_url_or_id)
            if not video_id:
                return {
                    'success': False,
                    'error': 'Invalid YouTube URL or video ID'
                }
            
            logger.info(f"Loading video: {video_id}")
            
            # Load transcript
            transcript = self.data_loader.fetch_transcript(video_id)
            
            if not transcript:
                return {
                    'success': False,
                    'error': 'Could not fetch transcript for this video'
                }
            
            # Create vector store
            logger.info("Creating vector store from transcript")
            self.vector_store_manager.create_vector_store(
                text=transcript.full_text,
                metadata={
                    'video_id': video_id,
                    'language': transcript.language
                }
            )
            
            # Initialize RAG system
            self.rag_system = RAGSystem(
                self.vector_store_manager,
                self.llm_manager
            )
            
            # Create tools
            self.tools = create_tools(
                self.vector_store_manager,
                self.llm_manager,
                transcript
            )
            
            # Create agent
            self.agent = create_agent(
                self.llm_manager,
                self.tools,
                agent_type="general"
            )
            
            # Store in database
            self.database.add_video(
                video_id=video_id,
                language=transcript.language,
                duration=transcript.total_duration,
                transcript_length=len(transcript.full_text)
            )
            
            # Update state
            self.current_video_id = video_id
            self.current_transcript = transcript
            
            logger.info(f"Video loaded successfully: {video_id}")
            
            return {
                'success': True,
                'video_id': video_id,
                'language': transcript.language,
                'duration': transcript.total_duration,
                'transcript_length': len(transcript.full_text),
                'num_chunks': len(self.vector_store_manager.documents),
                'full_text': transcript.full_text
            }
            
        except Exception as e:
            logger.error(f"Error loading video: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def query(
        self,
        question: str,
        use_agent: bool = True,
        k: int = 4
    ) -> Dict[str, Any]:
        """
        Query the system about the loaded video.
        
        Args:
            question: User question
            use_agent: Whether to use the agent (vs direct RAG)
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer and metadata
        """
        if not self.current_video_id:
            return {
                'answer': 'No video loaded. Please load a video first.',
                'sources': []
            }
        
        try:
            if use_agent and self.agent:
                # Use agent for more intelligent processing
                logger.info(f"Processing query with agent: {question}")
                result = self.agent.run(
                    query=question,
                    video_id=self.current_video_id
                )
                
                # Save to database
                self.database.add_query(
                    video_id=self.current_video_id,
                    query_text=question,
                    query_type="agent_qa",
                    answer=result['answer']
                )
                
                return result
            else:
                # Use direct RAG
                logger.info(f"Processing query with RAG: {question}")
                result = self.rag_system.query(question, k=k)
                
                # Save to database
                self.database.add_query(
                    video_id=self.current_video_id,
                    query_text=question,
                    query_type="rag_qa",
                    answer=result['answer']
                )
                
                return result
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'answer': f'Error: {str(e)}',
                'sources': []
            }
    
    def summarize(self, summary_type: str = "comprehensive") -> str:
        """
        Generate a summary of the video.
        
        Args:
            summary_type: Type of summary
            
        Returns:
            Summary text
        """
        if not self.current_video_id:
            return "No video loaded. Please load a video first."
        
        try:
            logger.info(f"Generating {summary_type} summary")
            summary = self.rag_system.summarize(summary_type=summary_type)
            
            # Save to database
            self.database.add_summary(
                video_id=self.current_video_id,
                summary_text=summary,
                summary_type=summary_type
            )
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"Error: {str(e)}"
    
    def extract_key_points(self, num_points: int = 5) -> str:
        """
        Extract key points from the video.
        
        Args:
            num_points: Number of key points to extract
            
        Returns:
            Key points text
        """
        if not self.agent:
            return "No video loaded. Please load a video first."
        
        try:
            logger.info(f"Extracting {num_points} key points")
            result = self.agent.run(
                query=f"Extract the {num_points} most important key points from this video.",
                video_id=self.current_video_id
            )
            return result['answer']
            
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return f"Error: {str(e)}"
    
    def extract_topics(self, num_topics: int = 5) -> List[str]:
        """
        Extract main topics from the video.
        
        Args:
            num_topics: Number of topics to extract
            
        Returns:
            List of topics
        """
        if not self.rag_system:
            return []
        
        try:
            logger.info(f"Extracting {num_topics} topics")
            return self.rag_system.extract_topics(num_topics=num_topics)
            
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return []
    
    def analyze_topic(self, topic: str) -> str:
        """
        Analyze how a topic is discussed in the video.
        
        Args:
            topic: Topic to analyze
            
        Returns:
            Analysis text
        """
        if not self.agent:
            return "No video loaded. Please load a video first."
        
        try:
            logger.info(f"Analyzing topic: {topic}")
            result = self.agent.run(
                query=f"Analyze how '{topic}' is discussed in this video. Provide details about what is said, examples given, and conclusions drawn.",
                video_id=self.current_video_id
            )
            return result['answer']
            
        except Exception as e:
            logger.error(f"Error analyzing topic: {e}")
            return f"Error: {str(e)}"
    
    def compare_topics(self, topic1: str, topic2: str) -> str:
        """
        Compare two topics from the video.
        
        Args:
            topic1: First topic
            topic2: Second topic
            
        Returns:
            Comparison text
        """
        if not self.agent:
            return "No video loaded. Please load a video first."
        
        try:
            logger.info(f"Comparing topics: {topic1} vs {topic2}")
            result = self.agent.run(
                query=f"Compare and contrast how '{topic1}' and '{topic2}' are discussed in this video.",
                video_id=self.current_video_id
            )
            return result['answer']
            
        except Exception as e:
            logger.error(f"Error comparing topics: {e}")
            return f"Error: {str(e)}"
    
    def search_transcript(self, search_text: str) -> List[tuple]:
        """
        Search for text in the transcript with timestamps.
        
        Args:
            search_text: Text to search for
            
        Returns:
            List of (timestamp, text) tuples
        """
        if not self.current_transcript:
            return []
        
        try:
            results = []
            search_lower = search_text.lower()
            
            for chunk in self.current_transcript.chunks:
                if search_lower in chunk.text.lower():
                    results.append((chunk.start, chunk.text))
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching transcript: {e}")
            return []
    
    def get_video_history(self) -> Dict[str, Any]:
        """
        Get history for the current video.
        
        Returns:
            Dictionary with video history
        """
        if not self.current_video_id:
            return {}
        
        return self.database.get_video_history(self.current_video_id)
    
    def get_recent_videos(self, limit: int = 10) -> List[Dict]:
        """
        Get recently analyzed videos.
        
        Args:
            limit: Maximum number of videos
            
        Returns:
            List of video dictionaries
        """
        return self.database.get_recent_videos(limit)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get system statistics.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'video_loaded': self.current_video_id is not None,
            'current_video_id': self.current_video_id
        }
        
        if self.rag_system:
            stats.update(self.rag_system.get_stats())
        
        return stats
    
    def cleanup(self):
        """Cleanup resources."""
        if self.database:
            self.database.close()
        logger.info("System cleanup complete")


def main():
    """Main function for CLI testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="YouTube Video Analysis System")
    parser.add_argument("video_id", help="YouTube video ID or URL")
    parser.add_argument("--api-key", help="Google API key")
    parser.add_argument("--query", help="Question to ask about the video")
    parser.add_argument("--summarize", action="store_true", help="Generate summary")
    
    args = parser.parse_args()
    
    # Initialize system
    system = YouTubeAnalysisSystem(api_key=args.api_key)
    
    # Load video
    print(f"Loading video: {args.video_id}")
    result = system.load_video(args.video_id)
    
    if not result['success']:
        print(f"Error: {result['error']}")
        return
    
    print(f"Video loaded successfully!")
    print(f"Duration: {result['duration']:.2f} seconds")
    print(f"Language: {result['language']}")
    print(f"Chunks: {result['num_chunks']}")
    
    # Process query or summary
    if args.query:
        print(f"\nQuery: {args.query}")
        response = system.query(args.query)
        print(f"\nAnswer: {response['answer']}")
    
    if args.summarize:
        print("\nGenerating summary...")
        summary = system.summarize("comprehensive")
        print(f"\nSummary:\n{summary}")
    
    # Cleanup
    system.cleanup()


if __name__ == "__main__":
    main()
