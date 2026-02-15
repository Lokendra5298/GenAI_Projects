"""
Data loader for fetching YouTube transcripts
"""
from typing import List, Dict, Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class TranscriptChunk:
    """Represents a chunk of transcript with timestamp."""
    text: str
    start: float
    duration: float
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'text': self.text,
            'start': self.start,
            'duration': self.duration
        }


@dataclass
class VideoTranscript:
    """Complete video transcript with metadata."""
    video_id: str
    chunks: List[TranscriptChunk]
    full_text: str
    language: str
    total_duration: float
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'video_id': self.video_id,
            'chunks': [chunk.to_dict() for chunk in self.chunks],
            'full_text': self.full_text,
            'language': self.language,
            'total_duration': self.total_duration
        }


class YouTubeDataLoader:
    """Handles loading transcripts from YouTube videos."""
    
    def __init__(self, preferred_languages: Optional[List[str]] = None):
        """
        Initialize the data loader.
        
        Args:
            preferred_languages: List of preferred language codes (default: ['en'])
        """
        self.api = YouTubeTranscriptApi()
        self.preferred_languages = preferred_languages or ['en']
    
    def fetch_transcript(self, video_id: str) -> Optional[VideoTranscript]:
        """
        Fetch transcript for a YouTube video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            VideoTranscript object or None if unavailable
        """
        try:
            logger.info(f"Fetching transcript for video ID: {video_id}")
            
            # Fetch transcript
            transcript_list = self.api.list_transcripts(video_id)
            
            # Try to get transcript in preferred language
            transcript = None
            language_used = None
            
            # First, try manually created transcripts in preferred languages
            try:
                for lang in self.preferred_languages:
                    try:
                        transcript = transcript_list.find_manually_created_transcript([lang])
                        language_used = lang
                        logger.info(f"Found manually created transcript in {lang}")
                        break
                    except NoTranscriptFound:
                        continue
            except Exception as e:
                logger.debug(f"No manually created transcript found: {e}")
            
            # If no manual transcript, try auto-generated
            if transcript is None:
                try:
                    for lang in self.preferred_languages:
                        try:
                            transcript = transcript_list.find_generated_transcript([lang])
                            language_used = lang
                            logger.info(f"Found auto-generated transcript in {lang}")
                            break
                        except NoTranscriptFound:
                            continue
                except Exception as e:
                    logger.debug(f"No auto-generated transcript found: {e}")
            
            # If still no transcript, get any available
            if transcript is None:
                available = transcript_list._manually_created_transcripts
                if not available:
                    available = transcript_list._generated_transcripts
                
                if available:
                    transcript = list(available.values())[0]
                    language_used = transcript.language_code
                    logger.info(f"Using available transcript in {language_used}")
                else:
                    logger.error("No transcripts available for this video")
                    return None
            
            # Fetch the actual transcript data
            transcript_data = transcript.fetch()
            
            # Convert to TranscriptChunk objects
            chunks = []
            for item in transcript_data:
                chunks.append(TranscriptChunk(
                    text=item['text'].strip(),
                    start=item['start'],
                    duration=item['duration']
                ))
            
            # Create full text
            full_text = " ".join(chunk.text for chunk in chunks)
            
            # Calculate total duration
            if chunks:
                total_duration = chunks[-1].start + chunks[-1].duration
            else:
                total_duration = 0.0
            
            video_transcript = VideoTranscript(
                video_id=video_id,
                chunks=chunks,
                full_text=full_text,
                language=language_used or 'unknown',
                total_duration=total_duration
            )
            
            logger.info(f"Successfully loaded transcript: {len(chunks)} chunks, "
                       f"{len(full_text)} characters, {total_duration:.2f} seconds")
            
            return video_transcript
            
        except TranscriptsDisabled:
            logger.error(f"Transcripts are disabled for video {video_id}")
            return None
        except NoTranscriptFound:
            logger.error(f"No transcript found for video {video_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching transcript: {e}")
            return None
    
    def get_available_languages(self, video_id: str) -> List[str]:
        """
        Get list of available transcript languages for a video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            List of available language codes
        """
        try:
            transcript_list = self.api.list_transcripts(video_id)
            languages = []
            
            # Manual transcripts
            for transcript in transcript_list._manually_created_transcripts.values():
                languages.append(f"{transcript.language_code} (manual)")
            
            # Auto-generated transcripts
            for transcript in transcript_list._generated_transcripts.values():
                languages.append(f"{transcript.language_code} (auto)")
            
            return languages
            
        except Exception as e:
            logger.error(f"Error getting available languages: {e}")
            return []
    
    def fetch_with_timestamps(
        self, 
        video_id: str, 
        search_text: str
    ) -> List[Tuple[float, str]]:
        """
        Search for specific text in transcript and return timestamps.
        
        Args:
            video_id: YouTube video ID
            search_text: Text to search for
            
        Returns:
            List of (timestamp, text) tuples
        """
        transcript = self.fetch_transcript(video_id)
        if not transcript:
            return []
        
        results = []
        search_lower = search_text.lower()
        
        for chunk in transcript.chunks:
            if search_lower in chunk.text.lower():
                results.append((chunk.start, chunk.text))
        
        return results


class TranscriptProcessor:
    """Process and clean transcript data."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean transcript text.
        
        Args:
            text: Raw transcript text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove common transcription artifacts
        artifacts = ['[Music]', '[Applause]', '[Laughter]', '(music)', '(applause)']
        for artifact in artifacts:
            text = text.replace(artifact, '')
        
        return text.strip()
    
    @staticmethod
    def extract_key_phrases(text: str, max_phrases: int = 10) -> List[str]:
        """
        Extract potential key phrases from text (simple extraction).
        
        Args:
            text: Input text
            max_phrases: Maximum number of phrases to extract
            
        Returns:
            List of key phrases
        """
        # Simple sentence splitting
        sentences = text.split('.')
        
        # Get sentences of reasonable length
        phrases = []
        for sentence in sentences:
            sentence = sentence.strip()
            word_count = len(sentence.split())
            if 5 <= word_count <= 20:  # Reasonable phrase length
                phrases.append(sentence)
        
        return phrases[:max_phrases]
    
    @staticmethod
    def split_into_segments(
        transcript: VideoTranscript, 
        segment_duration: float = 300.0
    ) -> List[Dict]:
        """
        Split transcript into time-based segments.
        
        Args:
            transcript: VideoTranscript object
            segment_duration: Duration of each segment in seconds (default: 5 minutes)
            
        Returns:
            List of segment dictionaries
        """
        segments = []
        current_segment = {
            'start_time': 0.0,
            'end_time': segment_duration,
            'text': '',
            'chunks': []
        }
        
        for chunk in transcript.chunks:
            if chunk.start >= current_segment['end_time']:
                # Save current segment
                if current_segment['text']:
                    segments.append(current_segment)
                
                # Start new segment
                current_segment = {
                    'start_time': current_segment['end_time'],
                    'end_time': current_segment['end_time'] + segment_duration,
                    'text': '',
                    'chunks': []
                }
            
            current_segment['text'] += ' ' + chunk.text
            current_segment['chunks'].append(chunk)
        
        # Add last segment
        if current_segment['text']:
            segments.append(current_segment)
        
        return segments


if __name__ == "__main__":
    # Test the data loader
    loader = YouTubeDataLoader()
    
    # Test with a sample video ID
    test_video_id = "Gfr50f6ZBvo"
    
    print(f"Testing with video ID: {test_video_id}")
    print("\nAvailable languages:")
    languages = loader.get_available_languages(test_video_id)
    for lang in languages:
        print(f"  - {lang}")
    
    print("\nFetching transcript...")
    transcript = loader.fetch_transcript(test_video_id)
    
    if transcript:
        print(f"\nTranscript loaded successfully:")
        print(f"  Video ID: {transcript.video_id}")
        print(f"  Language: {transcript.language}")
        print(f"  Chunks: {len(transcript.chunks)}")
        print(f"  Total duration: {transcript.total_duration:.2f} seconds")
        print(f"  Text length: {len(transcript.full_text)} characters")
        print(f"\nFirst 200 characters:")
        print(f"  {transcript.full_text[:200]}...")
    else:
        print("Failed to load transcript")
