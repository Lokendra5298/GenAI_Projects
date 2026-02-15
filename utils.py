"""
Utility functions for the YouTube Video Analysis System
"""
import re
import os
from typing import Optional, Dict, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_video_id(url_or_id: str) -> Optional[str]:
    """
    Extract YouTube video ID from URL or return the ID if already provided.
    
    Args:
        url_or_id: YouTube URL or video ID
        
    Returns:
        Video ID or None if invalid
    """
    # If it's already a video ID (11 characters, alphanumeric and - _)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    # Pattern for various YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    return None


def validate_api_key(api_key: str) -> bool:
    """
    Validate if API key is not empty and not a placeholder.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False
    
    # Check for common placeholder values
    placeholders = ['your_api_key', 'api_key_here', 'google_api_key', 'xxx', '']
    return api_key.lower() not in placeholders and len(api_key) > 10


def format_timestamp(seconds: float) -> str:
    """
    Convert seconds to HH:MM:SS format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length and add ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def create_session_id() -> str:
    """
    Create a unique session ID based on timestamp.
    
    Returns:
        Session ID string
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    return filename[:200]


def count_tokens(text: str) -> int:
    """
    Approximate token count (rough estimation: 1 token ≈ 4 characters).
    
    Args:
        text: Text to count tokens for
        
    Returns:
        Approximate token count
    """
    return len(text) // 4


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"


def setup_environment() -> Dict[str, Any]:
    """
    Setup environment and load configuration.
    
    Returns:
        Configuration dictionary
    """
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    config = {
        'google_api_key': os.getenv('GOOGLE_API_KEY', ''),
        'chunk_size': int(os.getenv('CHUNK_SIZE', '1000')),
        'chunk_overlap': int(os.getenv('CHUNK_OVERLAP', '200')),
        'embedding_model': os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2'),
        'llm_model': os.getenv('LLM_MODEL', 'gemini-2.0-flash-exp'),
        'temperature': float(os.getenv('TEMPERATURE', '0.3')),
    }
    
    return config


class ProgressTracker:
    """Simple progress tracking for operations."""
    
    def __init__(self):
        self.steps = []
        self.current_step = 0
    
    def add_step(self, description: str):
        """Add a step to track."""
        self.steps.append({
            'description': description,
            'status': 'pending',
            'timestamp': None
        })
    
    def complete_step(self, step_index: Optional[int] = None):
        """Mark a step as complete."""
        if step_index is None:
            step_index = self.current_step
        
        if step_index < len(self.steps):
            self.steps[step_index]['status'] = 'complete'
            self.steps[step_index]['timestamp'] = datetime.now()
            self.current_step = step_index + 1
    
    def get_progress(self) -> float:
        """Get progress percentage."""
        if not self.steps:
            return 0.0
        completed = sum(1 for step in self.steps if step['status'] == 'complete')
        return (completed / len(self.steps)) * 100
    
    def get_current_step(self) -> Optional[str]:
        """Get current step description."""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]['description']
        return None


def create_error_message(error: Exception, context: str = "") -> str:
    """
    Create a user-friendly error message.
    
    Args:
        error: Exception object
        context: Additional context about where error occurred
        
    Returns:
        Formatted error message
    """
    error_type = type(error).__name__
    error_msg = str(error)
    
    if context:
        return f"Error in {context}: {error_type} - {error_msg}"
    return f"{error_type}: {error_msg}"


if __name__ == "__main__":
    # Test functions
    test_urls = [
        "https://www.youtube.com/watch?v=Gfr50f6ZBvo",
        "https://youtu.be/Gfr50f6ZBvo",
        "Gfr50f6ZBvo"
    ]
    
    print("Testing video ID extraction:")
    for url in test_urls:
        video_id = extract_video_id(url)
        print(f"  {url} -> {video_id}")
    
    print("\nTesting timestamp formatting:")
    print(f"  90 seconds -> {format_timestamp(90)}")
    print(f"  3665 seconds -> {format_timestamp(3665)}")
    
    print("\nTesting duration formatting:")
    print(f"  45 seconds -> {format_duration(45)}")
    print(f"  125 seconds -> {format_duration(125)}")
    print(f"  7385 seconds -> {format_duration(7385)}")
