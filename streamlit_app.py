"""
Streamlit UI for YouTube Video Analysis System
"""
import streamlit as st
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import YouTubeAnalysisSystem
from utils import extract_video_id, format_timestamp, format_duration
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state."""
    if 'system' not in st.session_state:
        st.session_state.system = None
    if 'video_loaded' not in st.session_state:
        st.session_state.video_loaded = False
    if 'current_video_id' not in st.session_state:
        st.session_state.current_video_id = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'transcript_data' not in st.session_state:
        st.session_state.transcript_data = None


def initialize_system(api_key: str):
    """Initialize the YouTube analysis system."""
    if st.session_state.system is None:
        with st.spinner("Initializing system..."):
            try:
                st.session_state.system = YouTubeAnalysisSystem(api_key=api_key)
                return True
            except Exception as e:
                st.error(f"Error initializing system: {e}")
                return False
    return True


def load_video(video_url_or_id: str):
    """Load a YouTube video."""
    video_id = extract_video_id(video_url_or_id)
    
    if not video_id:
        st.error("Invalid YouTube URL or video ID")
        return False
    
    with st.spinner(f"Loading video {video_id}..."):
        try:
            result = st.session_state.system.load_video(video_id)
            
            if result['success']:
                st.session_state.video_loaded = True
                st.session_state.current_video_id = video_id
                st.session_state.transcript_data = result
                st.session_state.chat_history = []
                
                st.success(f"✅ Video loaded successfully!")
                return True
            else:
                st.error(f"Failed to load video: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            st.error(f"Error loading video: {e}")
            logger.error(f"Error loading video: {e}")
            return False


def sidebar():
    """Render sidebar."""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Google API Key",
            type="password",
            help="Enter your Google API key for Gemini"
        )
        
        if api_key:
            if initialize_system(api_key):
                st.success("✅ System initialized")
        else:
            st.warning("⚠️ Please enter your API key")
            st.info("Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)")
        
        st.markdown("---")
        
        # Video input
        st.markdown("### 🎥 Load Video")
        video_input = st.text_input(
            "YouTube URL or Video ID",
            placeholder="https://youtube.com/watch?v=..."
        )
        
        if st.button("Load Video", disabled=not api_key):
            if video_input:
                load_video(video_input)
            else:
                st.warning("Please enter a video URL or ID")
        
        # Video info
        if st.session_state.video_loaded:
            st.markdown("---")
            st.markdown("### 📊 Video Info")
            data = st.session_state.transcript_data
            
            st.markdown(f"**Video ID:** `{st.session_state.current_video_id}`")
            st.markdown(f"**Language:** {data.get('language', 'N/A')}")
            st.markdown(f"**Duration:** {format_duration(data.get('duration', 0))}")
            st.markdown(f"**Transcript length:** {data.get('transcript_length', 0):,} chars")
            st.markdown(f"**Chunks:** {data.get('num_chunks', 0)}")
        
        st.markdown("---")
        
        # Settings
        with st.expander("🔧 Advanced Settings"):
            st.markdown("**Agent Type:**")
            agent_type = st.selectbox(
                "Select agent",
                ["general", "summarizer", "qa", "analyzer"],
                label_visibility="collapsed"
            )
            
            st.markdown("**Retrieval Settings:**")
            k_docs = st.slider("Number of sources", 1, 10, 4)
            
            st.markdown("**LLM Settings:**")
            temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
        
        # History
        if st.session_state.chat_history:
            st.markdown("---")
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()


def main_content():
    """Render main content area."""
    st.markdown('<div class="main-header">🎥 YouTube Video Analyzer with AI Agents</div>', unsafe_allow_html=True)
    
    if not st.session_state.system:
        st.markdown("""
        <div class="info-box">
            <h3>Welcome to YouTube Video Analyzer!</h3>
            <p>This advanced system uses LangGraph agents to analyze YouTube videos.</p>
            <p><strong>Getting started:</strong></p>
            <ol>
                <li>Enter your Google API key in the sidebar</li>
                <li>Load a YouTube video by URL or ID</li>
                <li>Ask questions or request analysis</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if not st.session_state.video_loaded:
        st.markdown("""
        <div class="warning-box">
            <strong>No video loaded.</strong> Please load a YouTube video using the sidebar.
        </div>
        """, unsafe_allow_html=True)
        
        # Example videos
        st.markdown("### 🎬 Try these example videos:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("AI Overview"):
                load_video("Gfr50f6ZBvo")
        
        with col2:
            if st.button("Machine Learning"):
                load_video("ukzFI9rgwfU")
        
        with col3:
            if st.button("Python Tutorial"):
                load_video("kqtD5dpn9C8")
        
        return
    
    # Tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📝 Summaries", "🔍 Analysis", "📊 Transcript"])
    
    with tab1:
        chat_interface()
    
    with tab2:
        summary_interface()
    
    with tab3:
        analysis_interface()
    
    with tab4:
        transcript_interface()


def chat_interface():
    """Chat interface with the video."""
    st.markdown("### 💬 Chat with the Video")
    st.markdown("Ask questions about the video content using our AI agent.")
    
    # Display chat history
    for i, msg in enumerate(st.session_state.chat_history):
        if msg['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg['content'])
    
    # Chat input
    user_query = st.chat_input("Ask a question about the video...")
    
    if user_query:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_query
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.system.query(user_query)
                    answer = result['answer']
                    st.markdown(answer)
                    
                    # Add to history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': answer
                    })
                    
                    # Show sources
                    if result.get('sources'):
                        with st.expander("📚 View Sources"):
                            for i, source in enumerate(result['sources'][:3], 1):
                                st.markdown(f"**Source {i}:**")
                                st.text(source.page_content[:200] + "...")
                                st.markdown("---")
                    
                except Exception as e:
                    st.error(f"Error: {e}")


def summary_interface():
    """Summary generation interface."""
    st.markdown("### 📝 Generate Summaries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        summary_type = st.selectbox(
            "Summary Type",
            ["brief", "comprehensive", "bullet_points"]
        )
    
    with col2:
        if st.button("Generate Summary", type="primary"):
            with st.spinner("Generating summary..."):
                try:
                    summary = st.session_state.system.summarize(summary_type)
                    
                    st.markdown("#### Summary")
                    st.markdown(summary)
                    
                    # Save to history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': f"**{summary_type.title()} Summary:**\n\n{summary}"
                    })
                    
                except Exception as e:
                    st.error(f"Error generating summary: {e}")
    
    # Quick actions
    st.markdown("#### Quick Summary Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Key Points"):
            with st.spinner("Extracting key points..."):
                summary = st.session_state.system.extract_key_points()
                st.markdown(summary)
    
    with col2:
        if st.button("Main Topics"):
            with st.spinner("Analyzing topics..."):
                topics = st.session_state.system.extract_topics()
                st.markdown("**Main Topics:**")
                for topic in topics:
                    st.markdown(f"- {topic}")
    
    with col3:
        if st.button("Timeline"):
            st.info("Timeline generation coming soon!")


def analysis_interface():
    """Advanced analysis interface."""
    st.markdown("### 🔍 Advanced Analysis")
    
    # Topic analysis
    st.markdown("#### Analyze a Topic")
    topic = st.text_input("Enter a topic to analyze:")
    
    if st.button("Analyze Topic") and topic:
        with st.spinner(f"Analyzing '{topic}'..."):
            try:
                result = st.session_state.system.analyze_topic(topic)
                st.markdown("#### Analysis Results")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    
    # Compare topics
    st.markdown("#### Compare Two Topics")
    col1, col2 = st.columns(2)
    
    with col1:
        topic1 = st.text_input("First topic:")
    
    with col2:
        topic2 = st.text_input("Second topic:")
    
    if st.button("Compare Topics") and topic1 and topic2:
        with st.spinner(f"Comparing '{topic1}' and '{topic2}'..."):
            try:
                result = st.session_state.system.compare_topics(topic1, topic2)
                st.markdown("#### Comparison")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")


def transcript_interface():
    """Transcript viewer interface."""
    st.markdown("### 📊 Transcript Viewer")
    
    if st.session_state.transcript_data:
        # Search in transcript
        search_term = st.text_input("Search in transcript:")
        
        if search_term:
            with st.spinner("Searching..."):
                try:
                    results = st.session_state.system.search_transcript(search_term)
                    
                    if results:
                        st.success(f"Found {len(results)} results")
                        for i, (timestamp, text) in enumerate(results, 1):
                            with st.expander(f"Result {i} - {format_timestamp(timestamp)}"):
                                st.text(text)
                    else:
                        st.warning("No results found")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
        
        # Display full transcript
        if st.checkbox("Show full transcript"):
            transcript = st.session_state.transcript_data.get('full_text', '')
            st.text_area(
                "Full Transcript",
                transcript,
                height=400,
                label_visibility="collapsed"
            )


def main():
    """Main application function."""
    initialize_session_state()
    sidebar()
    main_content()


if __name__ == "__main__":
    main()
