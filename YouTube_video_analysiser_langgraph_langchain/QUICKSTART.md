# 🚀 Quick Start Guide

Get up and running with the YouTube Video Analysis System in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all necessary packages including:
- LangChain and LangGraph
- Google Generative AI
- Streamlit
- FAISS and Sentence Transformers
- YouTube Transcript API

## Step 2: Get Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Step 3: Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

## Step 4: Launch the Application

### Option A: Web Interface (Recommended)

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Option B: Command Line

```bash
python main.py VIDEO_ID --api-key YOUR_API_KEY --query "What is this video about?"
```

### Option C: Python Script

```python
from main import YouTubeAnalysisSystem

# Initialize
system = YouTubeAnalysisSystem(api_key="your-api-key")

# Load video
system.load_video("Gfr50f6ZBvo")

# Ask question
result = system.query("What are the main topics?")
print(result['answer'])
```

## Step 5: Try These Examples

### Example 1: Analyze an AI Tutorial Video

```bash
streamlit run streamlit_app.py
```

1. Enter your API key in the sidebar
2. Paste this URL: `https://www.youtube.com/watch?v=Gfr50f6ZBvo`
3. Click "Load Video"
4. Try these queries in the Chat tab:
   - "What is this video about?"
   - "What are the key takeaways?"
   - "Explain the main concepts discussed"

### Example 2: Generate Different Summaries

In the Summaries tab:
1. Select "brief" and generate a quick overview
2. Select "comprehensive" for detailed summary
3. Select "bullet_points" for key points list

### Example 3: Deep Topic Analysis

In the Analysis tab:
1. Enter a topic like "machine learning"
2. Click "Analyze Topic"
3. Compare two topics: "supervised learning" vs "unsupervised learning"

### Example 4: Search the Transcript

In the Transcript tab:
1. Search for "neural network"
2. View all occurrences with timestamps
3. Click timestamps to see context

## 📝 Common Use Cases

### Use Case 1: Educational Videos

Perfect for:
- Summarizing lectures
- Extracting key concepts
- Finding specific topics
- Comparing different approaches

### Use Case 2: Tech Tutorials

Ideal for:
- Quick reference without rewatching
- Finding code examples
- Understanding prerequisites
- Comparing techniques

### Use Case 3: Research Videos

Great for:
- Extracting methodology
- Finding citations and references
- Comparing different studies
- Understanding conclusions

## 🎯 Quick Tips

### Get Better Results

1. **Be Specific**: Ask detailed questions
   - ❌ "Tell me about this video"
   - ✅ "What specific techniques are discussed for training neural networks?"

2. **Use the Right Agent**: 
   - Use "summarizer" for overviews
   - Use "qa" for questions
   - Use "analyzer" for deep dives

3. **Adjust Sources**: 
   - More sources (7-10) for comprehensive answers
   - Fewer sources (3-4) for quick responses

4. **Search First**:
   - Use transcript search to find timestamps
   - Then ask detailed questions about that section

### Optimize Performance

1. **Video Length**:
   - Works best with 5-60 minute videos
   - Very long videos (2+ hours) may be slower

2. **API Usage**:
   - Summaries use more tokens than Q&A
   - Agent mode uses more calls than direct RAG

3. **Memory Management**:
   - Close browser tabs when not in use
   - Restart app if it becomes slow

## 🔧 Troubleshooting

### Problem: "No captions available"

**Solution**: 
- Not all videos have transcripts
- Try enabling auto-captions on YouTube
- Use videos with official captions

### Problem: "API key error"

**Solution**:
- Double-check your API key
- Ensure it's in the `.env` file correctly
- Verify Gemini API access in your Google account

### Problem: Slow responses

**Solution**:
- Reduce number of sources in settings
- Use smaller chunk sizes
- Try "brief" summaries instead of "comprehensive"

### Problem: Out of memory

**Solution**:
- Close other applications
- Reduce chunk size to 500
- Process shorter videos

## 📚 Next Steps

Once you're comfortable with the basics:

1. **Explore Agent Types**:
   - Try different specialized agents
   - Create custom agents for specific tasks

2. **Advanced Analysis**:
   - Compare multiple topics
   - Extract detailed timelines
   - Generate custom reports

3. **Integrate into Workflows**:
   - Use Python API in your scripts
   - Build custom tools
   - Extend with new capabilities

4. **Check the Full Documentation**:
   - Read `README.md` for complete details
   - Review module documentation
   - Explore example code

## 💡 Example Workflows

### Workflow 1: Research Assistant

```python
system = YouTubeAnalysisSystem(api_key="key")
system.load_video("VIDEO_ID")

# Get overview
overview = system.summarize("brief")

# Extract key points
points = system.extract_key_points(10)

# Analyze specific topic
analysis = system.analyze_topic("methodology")

# Save to file
with open("research_notes.txt", "w") as f:
    f.write(f"Overview:\n{overview}\n\n")
    f.write(f"Key Points:\n{points}\n\n")
    f.write(f"Analysis:\n{analysis}")
```

### Workflow 2: Course Note-Taker

```python
system = YouTubeAnalysisSystem(api_key="key")

# Process multiple lectures
lectures = ["VIDEO_ID_1", "VIDEO_ID_2", "VIDEO_ID_3"]

for i, lecture_id in enumerate(lectures, 1):
    system.load_video(lecture_id)
    summary = system.summarize("bullet_points")
    
    with open(f"lecture_{i}_notes.md", "w") as f:
        f.write(f"# Lecture {i}\n\n")
        f.write(summary)
```

### Workflow 3: Comparative Analysis

```python
system = YouTubeAnalysisSystem(api_key="key")
system.load_video("VIDEO_ID")

# Compare multiple concepts
comparisons = [
    ("concept1", "concept2"),
    ("approach1", "approach2"),
]

for c1, c2 in comparisons:
    result = system.compare_topics(c1, c2)
    print(f"\n{c1} vs {c2}:")
    print(result)
```
