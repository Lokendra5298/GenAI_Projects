# Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get API Key
Visit: https://makersuite.google.com/app/apikey

### 3. Create .env File
```bash
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### 4. Run App
```bash
streamlit run streamlit_app.py
```

## 📝 Try These Queries

**Start Simple:**
```
What was Apple's revenue in 2023?
```

**Compare Companies:**
```
Compare Microsoft and Apple's net income in 2023
```

**Analyze Risks:**
```
What are the main risk factors for Apple?
```

**Hybrid Analysis:**
```
Which company has better financial performance: Microsoft or Google?
```

## 🎯 Architecture Flow

```
User asks question 
    ↓
Gemini LLM analyzes intent
    ↓
Agent selects tools:
    • SQL Database (for numbers)
    • Vector Store (for text)
    ↓
Tools return results
    ↓
Gemini synthesizes answer
    ↓
Display in Streamlit UI
```

## 📊 What's Inside

- **3 Companies**: Apple, Microsoft, Alphabet
- **2 Years**: 2022-2023 data
- **Metrics**: Revenue, Net Income, Assets, Liabilities, Cash Flow, EPS
- **Qualitative**: Management Discussion, Risk Factors

## 🔧 Files Overview

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Web UI interface |
| `agent.py` | LangGraph agent logic |
| `tools.py` | SQL & Vector tools |
| `database.py` | Financial metrics storage |
| `vectorstore.py` | Text embeddings |
| `llm.py` | Gemini configuration |

## 💡 Tips

- **For numbers**: Ask about revenue, income, assets
- **For insights**: Ask about strategy, risks, outlook
- **For comparison**: Compare metrics across companies
- **For depth**: Combine quantitative and qualitative

## 🐛 Common Issues

**"API Key not found"**
→ Check your `.env` file exists and has correct format

**Import errors**
→ Run: `pip install -r requirements.txt`

**Slow first run**
→ Normal! Downloading embeddings model (~80MB)

**Empty results**
→ Check sample data loaded (automatic on first run)

## 🎓 Learn More

- LangChain Docs: https://python.langchain.com/
- LangGraph Guide: https://langchain-ai.github.io/langgraph/
- Gemini API: https://ai.google.dev/

---