"""
Database module for storing video analysis history and results
"""
import sqlite3
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class VideoDatabase:
    """SQLite database for storing video analysis data."""
    
    def __init__(self, db_path: str = "youtube_analysis.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._initialize_db()
    
    def _initialize_db(self):
        """Create database tables if they don't exist."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            # Videos table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT UNIQUE NOT NULL,
                    title TEXT,
                    language TEXT,
                    duration REAL,
                    transcript_length INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Queries table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    query_text TEXT NOT NULL,
                    query_type TEXT,
                    answer TEXT,
                    sources TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(video_id)
                )
            """)
            
            # Summaries table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    summary_type TEXT,
                    summary_text TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(video_id)
                )
            """)
            
            # Analysis sessions table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    video_id TEXT NOT NULL,
                    session_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(video_id)
                )
            """)
            
            self.conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def add_video(
        self, 
        video_id: str, 
        title: Optional[str] = None,
        language: Optional[str] = None,
        duration: Optional[float] = None,
        transcript_length: Optional[int] = None
    ) -> bool:
        """
        Add or update video record.
        
        Args:
            video_id: YouTube video ID
            title: Video title
            language: Transcript language
            duration: Video duration in seconds
            transcript_length: Length of transcript text
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cursor.execute("""
                INSERT INTO videos (video_id, title, language, duration, transcript_length)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(video_id) DO UPDATE SET
                    title = COALESCE(?, title),
                    language = COALESCE(?, language),
                    duration = COALESCE(?, duration),
                    transcript_length = COALESCE(?, transcript_length),
                    last_accessed = CURRENT_TIMESTAMP
            """, (video_id, title, language, duration, transcript_length,
                  title, language, duration, transcript_length))
            
            self.conn.commit()
            logger.info(f"Added/updated video: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding video: {e}")
            return False
    
    def add_query(
        self, 
        video_id: str, 
        query_text: str,
        query_type: str = "general",
        answer: Optional[str] = None,
        sources: Optional[List[str]] = None
    ) -> bool:
        """
        Add a query and its response.
        
        Args:
            video_id: YouTube video ID
            query_text: The query text
            query_type: Type of query (e.g., 'qa', 'summary', 'analysis')
            answer: The answer/response
            sources: List of source references
            
        Returns:
            True if successful, False otherwise
        """
        try:
            sources_json = json.dumps(sources) if sources else None
            
            self.cursor.execute("""
                INSERT INTO queries (video_id, query_text, query_type, answer, sources)
                VALUES (?, ?, ?, ?, ?)
            """, (video_id, query_text, query_type, answer, sources_json))
            
            self.conn.commit()
            logger.info(f"Added query for video: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding query: {e}")
            return False
    
    def add_summary(
        self, 
        video_id: str, 
        summary_text: str,
        summary_type: str = "general",
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Add a summary for a video.
        
        Args:
            video_id: YouTube video ID
            summary_text: The summary text
            summary_type: Type of summary (e.g., 'brief', 'detailed', 'key_points')
            metadata: Additional metadata as dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            metadata_json = json.dumps(metadata) if metadata else None
            
            self.cursor.execute("""
                INSERT INTO summaries (video_id, summary_type, summary_text, metadata)
                VALUES (?, ?, ?, ?)
            """, (video_id, summary_type, summary_text, metadata_json))
            
            self.conn.commit()
            logger.info(f"Added {summary_type} summary for video: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding summary: {e}")
            return False
    
    def get_video_history(self, video_id: str) -> Dict[str, Any]:
        """
        Get complete history for a video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary with video info, queries, and summaries
        """
        try:
            # Get video info
            self.cursor.execute("""
                SELECT * FROM videos WHERE video_id = ?
            """, (video_id,))
            video_row = self.cursor.fetchone()
            
            if not video_row:
                return {}
            
            video_info = {
                'video_id': video_row[1],
                'title': video_row[2],
                'language': video_row[3],
                'duration': video_row[4],
                'transcript_length': video_row[5],
                'created_at': video_row[6],
                'last_accessed': video_row[7]
            }
            
            # Get queries
            self.cursor.execute("""
                SELECT query_text, query_type, answer, sources, created_at
                FROM queries
                WHERE video_id = ?
                ORDER BY created_at DESC
            """, (video_id,))
            
            queries = []
            for row in self.cursor.fetchall():
                queries.append({
                    'query_text': row[0],
                    'query_type': row[1],
                    'answer': row[2],
                    'sources': json.loads(row[3]) if row[3] else [],
                    'created_at': row[4]
                })
            
            # Get summaries
            self.cursor.execute("""
                SELECT summary_type, summary_text, metadata, created_at
                FROM summaries
                WHERE video_id = ?
                ORDER BY created_at DESC
            """, (video_id,))
            
            summaries = []
            for row in self.cursor.fetchall():
                summaries.append({
                    'summary_type': row[0],
                    'summary_text': row[1],
                    'metadata': json.loads(row[2]) if row[2] else {},
                    'created_at': row[3]
                })
            
            return {
                'video': video_info,
                'queries': queries,
                'summaries': summaries
            }
            
        except Exception as e:
            logger.error(f"Error getting video history: {e}")
            return {}
    
    def get_recent_videos(self, limit: int = 10) -> List[Dict]:
        """
        Get recently accessed videos.
        
        Args:
            limit: Maximum number of videos to return
            
        Returns:
            List of video dictionaries
        """
        try:
            self.cursor.execute("""
                SELECT video_id, title, language, duration, last_accessed
                FROM videos
                ORDER BY last_accessed DESC
                LIMIT ?
            """, (limit,))
            
            videos = []
            for row in self.cursor.fetchall():
                videos.append({
                    'video_id': row[0],
                    'title': row[1],
                    'language': row[2],
                    'duration': row[3],
                    'last_accessed': row[4]
                })
            
            return videos
            
        except Exception as e:
            logger.error(f"Error getting recent videos: {e}")
            return []
    
    def create_session(self, session_id: str, video_id: str, session_data: Dict) -> bool:
        """
        Create a new analysis session.
        
        Args:
            session_id: Unique session identifier
            video_id: YouTube video ID
            session_data: Session data as dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session_json = json.dumps(session_data)
            
            self.cursor.execute("""
                INSERT INTO sessions (session_id, video_id, session_data)
                VALUES (?, ?, ?)
            """, (session_id, video_id, session_json))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return False
    
    def update_session(self, session_id: str, session_data: Dict) -> bool:
        """
        Update an existing session.
        
        Args:
            session_id: Unique session identifier
            session_data: Updated session data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session_json = json.dumps(session_data)
            
            self.cursor.execute("""
                UPDATE sessions
                SET session_data = ?, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = ?
            """, (session_json, session_id))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get session data.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Session data dictionary or None
        """
        try:
            self.cursor.execute("""
                SELECT video_id, session_data, created_at, updated_at
                FROM sessions
                WHERE session_id = ?
            """, (session_id,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'video_id': row[0],
                    'session_data': json.loads(row[1]),
                    'created_at': row[2],
                    'updated_at': row[3]
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            return None
    
    def delete_video(self, video_id: str) -> bool:
        """
        Delete a video and all associated data.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete related records first
            self.cursor.execute("DELETE FROM queries WHERE video_id = ?", (video_id,))
            self.cursor.execute("DELETE FROM summaries WHERE video_id = ?", (video_id,))
            self.cursor.execute("DELETE FROM sessions WHERE video_id = ?", (video_id,))
            self.cursor.execute("DELETE FROM videos WHERE video_id = ?", (video_id,))
            
            self.conn.commit()
            logger.info(f"Deleted video and related data: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting video: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    # Test the database
    db = VideoDatabase("test_youtube.db")
    
    # Test adding a video
    print("Testing database operations...")
    db.add_video(
        video_id="test123",
        title="Test Video",
        language="en",
        duration=300.0,
        transcript_length=5000
    )
    
    # Test adding a query
    db.add_query(
        video_id="test123",
        query_text="What is this video about?",
        query_type="qa",
        answer="This is a test video.",
        sources=["chunk_1", "chunk_2"]
    )
    
    # Test getting history
    history = db.get_video_history("test123")
    print("\nVideo history:")
    print(json.dumps(history, indent=2))
    
    # Test getting recent videos
    recent = db.get_recent_videos(5)
    print("\nRecent videos:")
    for video in recent:
        print(f"  - {video['video_id']}: {video['title']}")
    
    db.close()
    print("\nDatabase test complete!")
