# 📊 SEC Financial Analyst

An AI-powered financial analysis system using **LangChain**, **LangGraph**, and **Google Gemini API** to analyze SEC 10-K filings.

## 🚀 Features

- **Multi-Tool Agent**: Uses both SQL database and vector store for comprehensive analysis
- **Quantitative Analysis**: Query financial metrics (revenue, income, assets, etc.)
- **Qualitative Analysis**: Analyze management discussions and risk factors
- **Hybrid Queries**: Combine both quantitative and qualitative insights
- **Interactive UI**: Streamlit-based web interface

## 🏗️ Architecture

```
User Query → Agent (LangGraph) → [SQL Tool | Vector Tool] → Gemini LLM → Response
```

**Components:**
- **SQL Database**: Stores structured financial metrics
- **Vector Store**: Stores unstructured text (MD&A, risk factors) with HuggingFace embeddings
- **LangGraph Agent**: Orchestrates tool usage and reasoning
- **Gemini LLM**: Powers natural language understanding and generation

## 📦 Installation

### 1. Clone and Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
GOOGLE_API_KEY=your_actual_api_key_here
```

## 🎯 Usage

### Run the Streamlit App

```bash
# Option 1: Direct streamlit command
streamlit run streamlit_app.py

# Option 2: Using main.py
python main.py
```

The app will open in your browser at `http://localhost:8501`

### Example Queries

**Quantitative:**
```
- What was Apple's revenue in 2023?
- Compare Microsoft and Apple's net income
- Show companies with revenue over 300 billion
```

**Qualitative:**
```
- What are the main risks for Apple?
- Summarize Microsoft's business strategy
- What does Alphabet's management say about AI?
```

**Hybrid:**
```
- Which company has the best performance and lowest risks?
- How do supply chain issues affect Apple's financials?
```

## 📁 Project Structure

```
sec_financial_analyst/
├── agent.py              # LangGraph agent implementation
├── llm.py                # Gemini LLM configuration
├── rag.py                # RAG pipeline
├── tools.py              # LangChain tools (SQL, Vector)
├── vectorstore.py        # ChromaDB vector store
├── database.py           # SQLite database
├── data_loader.py        # Sample data loader
├── utils.py              # Utility functions
├── streamlit_app.py      # Streamlit UI
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── .env                  # Environment variables (create this)
```

## 🔧 Technical Details

### Embeddings
- Model: `all-MiniLM-L6-v2` from HuggingFace
- Vector Store: ChromaDB with persistent storage

### Database Schema
```sql
financial_metrics (
    company_ticker TEXT,
    company_name TEXT,
    fiscal_year INTEGER,
    revenue REAL,
    net_income REAL,
    total_assets REAL,
    total_liabilities REAL,
    operating_cash_flow REAL,
    eps REAL
)
```

### Available Companies (Sample Data)
- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation
- **GOOGL** - Alphabet Inc.

### Data Years
- 2022-2023 financial data

## 🧪 Testing

Test the system with these queries:

1. **Simple Quantitative**: "What was Apple's revenue in 2023?"
2. **Comparison**: "Compare Microsoft and Google's net income"
3. **Qualitative**: "What are Apple's main risk factors?"
4. **Hybrid**: "Does Microsoft's revenue growth justify its risk profile?"

## 🛠️ Customization

### Add More Data

Edit `data_loader.py` to add more companies or years:

```python
def get_sample_financial_data():
    return [
        {
            'ticker': 'TSLA',
            'company_name': 'Tesla Inc.',
            'fiscal_year': 2023,
            # ... more fields
        }
    ]
```

### Adjust LLM Settings

Edit `llm.py` to change model or temperature:

```python
def get_gemini_llm(temperature=0, model="gemini-1.5-pro"):
    # Change to gemini-1.5-pro for better reasoning
    pass
```

## 📝 Notes

- This is a **demo project** with sample data
- For production use, integrate real SEC EDGAR API
- Consider rate limits on Gemini API
- Vector store persists in `./chroma_db`
- Database persists in `financial_data.db`

## 🤝 Contributing

Feel free to extend this project:
- Add more financial metrics
- Integrate real SEC filings
- Add data visualization
- Implement conversation memory
- Add export functionality

## 📄 License

MIT License - feel free to use for learning and development!

## 🆘 Troubleshooting

**API Key Error:**
- Ensure `.env` file exists and contains valid API key
- Check key format: `GOOGLE_API_KEY=AIza...`

**Import Errors:**
- Reinstall dependencies: `pip install -r requirements.txt`
- Ensure virtual environment is activated

**Vector Store Issues:**
- Delete `./chroma_db` folder and restart
- Check disk space for embeddings storage

**Database Issues:**
- Delete `financial_data.db` and restart
- Will automatically recreate with sample data
