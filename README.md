# GenAI Projects

A collection of hands-on projects exploring **Generative AI** and **RAG (Retrieval-Augmented Generation)** systems. Each project demonstrates practical applications of cutting-edge AI technologies.

## 📚 About

This repository contains learning projects and experiments with generative AI frameworks, large language models, and advanced retrieval systems. The projects showcase real-world applications from financial analysis to academic research navigation.

## 🛠️ Technologies & Stack

- **LLM Frameworks**: LangChain, LangGraph
- **Language Models**: Google Gemini, OpenAI GPT
- **Vector Databases**: FAISS, ChromaDB
- **Embeddings**: sentence-transformers, HuggingFace
- **Data Sources**: ArXiv, SEC EDGAR, Kaggle
- **UI Framework**: Streamlit
- **Core Language**: Python 3.8+
- **Notebooks**: Jupyter Notebook

## 📊 Repository Composition

- **Jupyter Notebooks (95.9%)** - Interactive explorations, tutorials, and experiments
- **Python Scripts (4.1%)** - Utility functions, modules, and supporting code

## 🚀 Projects

### 1. **Scholarly Research Navigator** 📚
*AI-powered academic paper discovery and literature review generator*

**Features:**
- Natural language queries about research papers
- SQL-based filtering by category, author, year
- Semantic vector search over abstracts
- Automatic PDF extraction from ArXiv
- Long-context literature review generation
- Streamlit web interface

**Tech Stack:** LangChain, LangGraph, Google Gemini, FAISS, PyPDF

**Directory:** `Research_navigator_using_langgraph_langchain/`

---

### 2. **SEC Financial Analyst** 💰
*Multi-tool agentic framework for SEC 10-K filing analysis*

**Features:**
- Quantitative analysis using SQL database
- Qualitative analysis using vector store
- Hybrid query capabilities
- Financial metrics extraction
- Risk factor analysis
- Interactive Streamlit dashboard

**Tech Stack:** LangChain, LangGraph, Google Gemini, ChromaDB, SQLite

**Directory:** `Sec_financial_analysis_agentic_framework/`

---

## 🎯 Learning Outcomes

Through these projects, you'll learn:

✅ How to build RAG (Retrieval-Augmented Generation) systems  
✅ Multi-tool agentic frameworks with LangGraph  
✅ Prompt engineering and chain-of-thought techniques  
✅ Vector embeddings and semantic search  
✅ Integration of multiple data sources  
✅ Building production-ready AI applications  
✅ Streamlit for rapid prototyping  
✅ LLM-powered decision making  

## 🏁 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- API keys (Google Gemini, etc.)
- Jupyter Notebook or JupyterLab (for notebooks)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Lokendra5298/GenAI_Projects.git
cd GenAI_Projects
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
Each project has its own `requirements.txt`. Navigate to the project directory and install:
```bash
pip install -r requirements.txt
```

### Running Projects

**For Jupyter Notebooks:**
```bash
jupyter notebook
# Then open the .ipynb files
```

**For Streamlit Applications:**
```bash
cd <project_directory>
streamlit run streamlit_app.py
```

**For Python Scripts:**
```bash
python main.py
```

## 📁 Repository Structure

```
GenAI_Projects/
├── Research_navigator_using_langgraph_langchain/
│   ├── streamlit_app.py
│   ├── agent.py
│   ├── requirements.txt
│   └── README.md
├── Sec_financial_analysis_agentic_framework/
│   ├── streamlit_app.py
│   ├── agent.py
│   ├── tools.py
│   ├── requirements.txt
│   └── README.md
├── [Other projects and notebooks]/
└── README.md (this file)
```

## 📖 Usage Guide

### For Each Project:

1. **Read the project-specific README** - Located in each project directory
2. **Check requirements** - Install dependencies from the project's `requirements.txt`
3. **Set up API keys** - Most projects require Google Gemini or similar APIs
4. **Run the application** - Use the provided command (Streamlit, Jupyter, or Python)
5. **Explore and experiment** - Modify prompts, add data, customize behavior

### Example Queries

**Research Navigator:**
```
"Find recent papers on Retrieval-Augmented Generation and explain their key contributions"
```

**SEC Financial Analyst:**
```
"Compare Apple and Microsoft's financial performance and explain the differences"
```

## 🔧 Configuration

### Setting API Keys

Most projects use Google Gemini API. Set it up:

```bash
export GOOGLE_API_KEY="your-api-key-here"
# Or create a .env file in the project directory:
# GOOGLE_API_KEY=your-api-key-here
```

Get your API key from: [Google AI Studio](https://aistudio.google.com/app/apikey)

## 💡 Key Concepts Demonstrated

### RAG Systems
- Data ingestion and preprocessing
- Vector embeddings and indexing
- Semantic search and retrieval
- Context-aware generation

### Agent Frameworks
- Multi-tool integration
- Reasoning and planning
- Tool selection and routing
- State management

### LLM Integration
- Prompt engineering
- Context window management
- Chain-of-thought prompting
- Output parsing

## 🧪 Testing & Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install --upgrade -r requirements.txt
```

**API Key Not Found:**
- Verify `.env` file exists
- Check key format and validity
- Restart the application

**Memory Issues:**
- Reduce dataset size for vector indexing
- Use smaller embedding models
- Increase system RAM or use cloud resources

**Vector Store Errors:**
- Delete cached indices and rebuild
- Verify disk space availability

## 📚 Resources & References

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Google Gemini API](https://ai.google.dev/)
- [Retrieval-Augmented Generation Paper](https://arxiv.org/abs/2005.11401)
- [ArXiv API Documentation](https://arxiv.org/help/api)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Fork the repository
- Create feature branches
- Submit pull requests
- Report issues
- Suggest improvements

## 📝 License

This project is open source and available under the **MIT License**.

## 👤 Author

**Lokendra5298**

- GitHub: [@Lokendra5298](https://github.com/Lokendra5298)
- Repository: [GenAI_Projects](https://github.com/Lokendra5298/GenAI_Projects)

## 📞 Support & Questions

- Open an **GitHub Issue** for bugs or feature requests
- Check project-specific READMEs for detailed documentation
- Review code comments and docstrings for implementation details

## 🎓 Learning Path

**Recommended order for learning:**

1. Start with Jupyter notebooks for foundational concepts
2. Explore the SEC Financial Analyst project for multi-tool systems
3. Study the Research Navigator for advanced RAG implementation
4. Experiment and modify projects to build intuition
5. Build your own GenAI applications!

---

**Last Updated:** June 2026  
**Python Version:** 3.8+  
**Status:** Active Development 🚀

Happy learning! Let's build amazing AI applications together! 🎉
