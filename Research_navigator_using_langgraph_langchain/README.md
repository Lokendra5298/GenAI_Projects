# Scholarly Research Navigator

**AI-powered academic paper discovery, filtering, semantic search and literature review generator**  
using ArXiv metadata (~2M papers), LangChain/LangGraph agents, Google Gemini, and local embeddings.
## ✨ Features

- Natural language queries about research papers
- **SQL filtering** by category, author, year, etc.
- **Semantic vector search** over abstracts (using sentence-transformers)
- Automatic fetching & text extraction from arXiv PDFs
- Long-context literature review / comparison generation powered by **Gemini 1.5 Pro**
- Simple Streamlit web interface
- LangGraph-based agent workflow with clear tool routing

Example query:
> Find recent papers on Low-Rank Adaptation (LoRA) and explain how they differ from standard fine-tuning.

## 🛠 Tech Stack

| Layer                | Technology                                 |
|----------------------|--------------------------------------------|
| LLM / Chat           | Google Gemini 1.5 Pro                      |
| Embeddings           | sentence-transformers/all-MiniLM-L6-v2     |
| Agent framework      | LangGraph + LangChain                      |
| Vector store         | FAISS (local)                              |
| Structured filtering | SQLite + LangChain SQL toolkit             |
| PDF extraction       | PyPDF                                      |
| UI                   | Streamlit                                  |
| Data                 | arXiv metadata snapshot (Kaggle)           |

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- Google Gemini API key → [Get one here](https://aistudio.google.com/app/apikey)
- ~20 GB free disk space (for full dataset + index)
- 16–32 GB RAM recommended for first indexing run

### 2. Installation

```bash
# 1. Clone / download project
# 2. Create virtual environment
python -m venv venv
source venv/bin/activate           # Linux/macOS
# venv\Scripts\activate            # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API key
export GOOGLE_API_KEY="your-key-here"

# 5. Download ArXiv metadata (~1.2 GB)
# https://www.kaggle.com/datasets/Cornell-University/arxiv
# → place arxiv-metadata-oai-snapshot.json in project root

# 6. Run the app (first run builds DB + vector index — be patient)
streamlit run streamlit_app.py
