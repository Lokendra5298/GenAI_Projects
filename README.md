# 🎥 Advanced YouTube Video Analysis System

An intelligent YouTube video analysis system powered by LangGraph agents, LangChain, and Google Gemini. This system can analyze YouTube videos, answer questions, generate summaries, and perform deep content analysis using advanced AI agents.

## ✨ Features

### Core Capabilities
- **Intelligent Q&A**: Ask questions about video content with context-aware responses
- **Multiple Summary Types**: Brief, comprehensive, and bullet-point summaries
- **Topic Analysis**: Deep analysis of specific topics discussed in videos
- **Comparative Analysis**: Compare and contrast different concepts from the video
- **Transcript Search**: Find specific content with timestamps
- **Key Points Extraction**: Automatically extract main takeaways
- **Conversation Memory**: Multi-turn conversations with context retention

### Advanced Features
- **LangGraph Agents**: Multiple specialized agents for different tasks
  - General-purpose analysis agent
  - Summarization specialist
  - Q&A specialist
  - Deep analysis expert
- **RAG (Retrieval-Augmented Generation)**: Accurate answers grounded in transcript
- **Vector Search**: Semantic search using FAISS and sentence transformers
- **Database Storage**: SQLite database for history and analytics
- **Streamlit UI**: Beautiful, user-friendly web interface

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                         │
├─────────────────────────────────────────────────────────────┤
│                    Main System (main.py)                    │
├──────────────┬──────────────┬──────────────┬───────────────┤
│ Data Loader  │ Vector Store │  LLM Manager │   Database    │
│ (YouTube)    │   (FAISS)    │   (Gemini)   │  (SQLite)     │
└──────────────┴──────────────┴──────────────┴───────────────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
         ┌──────────────┴──────────────┐
         │                             │
    ┌────▼────┐                  ┌────▼────┐
    │   RAG   │                  │  Agent  │
    │ System  │                  │ (Lang   │
    │         │                  │  Graph) │
    └─────────┘                  └─────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Google API Key (for Gemini)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd youtube-analysis-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

4. **Run the application**
```bash
streamlit run streamlit_app.py
```

## 🚀 Usage

### Web Interface (Streamlit)

1. **Start the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Enter your Google API key** in the sidebar

3. **Load a video** by pasting a YouTube URL or video ID

4. **Interact with the video**:
   - Use the Chat tab to ask questions
   - Generate summaries in the Summaries tab
   - Perform deep analysis in the Analysis tab
   - Search the transcript in the Transcript tab

### Command Line Interface

```bash
# Analyze a video and ask a question
python main.py VIDEO_ID --api-key YOUR_API_KEY --query "What is this video about?"

# Generate a summary
python main.py VIDEO_ID --api-key YOUR_API_KEY --summarize
```

### Python API

```python
from main import YouTubeAnalysisSystem

# Initialize system
system = YouTubeAnalysisSystem(api_key="your-api-key")

# Load a video
result = system.load_video("VIDEO_ID")

# Ask a question
response = system.query("What are the main points discussed?")
print(response['answer'])

# Generate summary
summary = system.summarize("comprehensive")
print(summary)

# Analyze a topic
analysis = system.analyze_topic("machine learning")
print(analysis)

# Compare topics
comparison = system.compare_topics("supervised learning", "unsupervised learning")
print(comparison)
```

## 📚 Module Documentation

### `data_loader.py`
Handles fetching and processing YouTube transcripts.
- `YouTubeDataLoader`: Main class for loading transcripts
- `VideoTranscript`: Data class for transcript information
- `TranscriptProcessor`: Utilities for cleaning and processing text

### `vectorstore.py`
Manages vector embeddings and similarity search.
- `VectorStoreManager`: Creates and manages FAISS vector stores
- `HybridRetriever`: Combines semantic and keyword search

### `llm.py`
Interfaces with Google Gemini LLM.
- `LLMManager`: Manages LLM interactions
- `PromptManager`: Collection of prompt templates
- `RAGChain`: Retrieval-augmented generation chain

### `rag.py`
Implements RAG system for accurate responses.
- `RAGSystem`: Complete RAG implementation
- Query processing with context retrieval
- Summary generation with various types

### `tools.py`
Provides tools for LangGraph agents.
- `YouTubeTools`: Collection of analysis tools
- Search, analyze, summarize, and compare functions
- Timestamp finding and key point extraction

### `agent.py`
LangGraph agent implementation.
- `VideoAnalysisAgent`: Main agent with tool use
- `MultiStepAgent`: Complex multi-step task planning
- `SpecializedAgents`: Task-specific agent variants

### `database.py`
SQLite database for storage.
- `VideoDatabase`: Stores videos, queries, and summaries
- History tracking and analytics
- Session management

### `utils.py`
Utility functions.
- Video ID extraction
- Timestamp formatting
- Progress tracking
- Error handling

## 🎯 Examples

### Example 1: Basic Q&A
```python
system = YouTubeAnalysisSystem(api_key="your-key")
system.load_video("Gfr50f6ZBvo")

result = system.query("What is deep learning?")
print(result['answer'])
```

### Example 2: Generate Multiple Summaries
```python
# Brief summary
brief = system.summarize("brief")

# Comprehensive summary
detailed = system.summarize("comprehensive")

# Bullet points
bullets = system.summarize("bullet_points")
```

### Example 3: Topic Analysis
```python
# Analyze a specific topic
analysis = system.analyze_topic("neural networks")

# Compare two topics
comparison = system.compare_topics(
    "supervised learning",
    "reinforcement learning"
)
```

### Example 4: Search with Timestamps
```python
# Find when "AI" is mentioned
results = system.search_transcript("artificial intelligence")

for timestamp, text in results:
    print(f"[{timestamp}s]: {text}")
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with:

```env
GOOGLE_API_KEY=your_google_api_key_here
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gemini-2.0-flash-exp
TEMPERATURE=0.3
```

### Advanced Settings

In the Streamlit sidebar, you can configure:
- **Agent Type**: Choose between general, summarizer, qa, or analyzer agents
- **Number of Sources**: How many transcript chunks to retrieve (1-10)
- **Temperature**: LLM creativity level (0.0-1.0)

## 🔧 Troubleshooting

### Common Issues

**"No transcript available"**
- The video may not have captions enabled
- Try a different video with available transcripts

**"API key error"**
- Verify your Google API key is correct
- Check that you have Gemini API access enabled

**"Out of memory"**
- Try reducing the number of retrieved sources
- Use smaller chunk sizes in configuration

**"Network error"**
- Check your internet connection
- Some regions may have YouTube API restrictions

## 📊 System Requirements

- **RAM**: Minimum 4GB, recommended 8GB+
- **Storage**: ~2GB for models and cache
- **Internet**: Required for YouTube access and Gemini API
- **Browser**: Modern browser for Streamlit interface

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **LangChain** for the agent framework
- **LangGraph** for agent orchestration
- **Google Gemini** for the LLM
- **Streamlit** for the UI framework
- **youtube-transcript-api** for transcript access
- **FAISS** for vector search
- **Sentence Transformers** for embeddings

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review example code

## 🗺️ Roadmap

Future enhancements:
- [ ] Support for multiple videos simultaneously
- [ ] Video chapter detection and analysis
- [ ] Export analysis reports to PDF/DOCX
- [ ] Integration with more LLM providers
- [ ] Advanced visualization of topics and themes
- [ ] Batch processing of video playlists
- [ ] Custom agent creation interface
- [ ] Multi-language support

---

Built with using LangGraph, LangChain, and Google Gemini
