# 🚀 Installation Guide - SEC Financial Analyst

## Prerequisites

- Python 3.8+ installed
- pip package manager
- Google Gemini API key (free at https://makersuite.google.com/app/apikey)
- 2GB free disk space

---

## Step-by-Step Installation

### Step 1: Extract Project Files
```bash
# Navigate to the project directory
cd sec_financial_analyst
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Expected output:**
```
✅ Installing streamlit...
✅ Installing langchain...
✅ Installing sentence-transformers...
[... more packages ...]
✅ Successfully installed all packages
```

**⏱️ Time**: ~3-5 minutes (depending on internet speed)

### Step 4: Get Google Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the API key (starts with `AIza...`)

### Step 5: Configure Environment Variables

**Option A: Manual**
```bash
# Copy the example file
cp .env.example .env

# Edit .env file
nano .env
# or
code .env

# Add your API key:
GOOGLE_API_KEY=AIzaSy...your_actual_key_here...
```

**Option B: Command Line**
```bash
# Create .env file directly
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### Step 6: Verify Installation
```bash
# Test Python imports
python -c "import langchain; import streamlit; print('✅ All imports successful!')"
```

### Step 7: Run the Application
```bash
# Start Streamlit
streamlit run streamlit_app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 8: Open in Browser

The app should automatically open at `http://localhost:8501`

If not, manually navigate to: http://localhost:8501

---

## 🎉 First Run Checklist

When you first run the app:

- [ ] App loads successfully
- [ ] Green "System initialized" message appears
- [ ] Sample data loaded automatically
- [ ] Query input box is visible
- [ ] Sidebar shows 3 companies (AAPL, MSFT, GOOGL)

**Try your first query:**
```
What was Apple's revenue in 2023?
```

**Expected response:**
```
✅ Analysis Complete!
Apple's revenue in 2023 was $383.29 billion...
```

---

## 🐛 Troubleshooting

### Problem: "GOOGLE_API_KEY not found"

**Solution:**
```bash
# Check if .env file exists
ls -la .env

# If missing, create it:
echo "GOOGLE_API_KEY=your_key_here" > .env

# Verify contents:
cat .env
```

### Problem: Import errors

**Solution:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Or install individually:
pip install langchain langchain-google-genai langgraph
pip install streamlit sentence-transformers chromadb
```

### Problem: "ModuleNotFoundError: No module named 'langchain_google_genai'"

**Solution:**
```bash
# Ensure you're in virtual environment
which python  # Should show venv/bin/python

# Install specific package
pip install langchain-google-genai
```

### Problem: Slow first startup

**Expected behavior:**
The first run downloads the HuggingFace embeddings model (~80MB).

```
Downloading: 100%|██████████| 80MB/80MB [00:30<00:00]
```

This is **normal** and only happens once.

### Problem: Database errors

**Solution:**
```bash
# Delete existing database
rm financial_data.db

# Delete vector store
rm -rf chroma_db

# Restart app (will recreate fresh)
streamlit run streamlit_app.py
```

### Problem: Port 8501 already in use

**Solution:**
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502

# Or kill existing process
lsof -ti:8501 | xargs kill -9
```

---

## 🔧 Alternative Installation Methods

### Method 1: Using setup.sh (Linux/Mac)
```bash
# Make executable
chmod +x setup.sh

# Run automated setup
./setup.sh

# Follow prompts
```

### Method 2: Docker (Coming Soon)
```bash
# Build image
docker build -t sec-analyst .

# Run container
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key sec-analyst
```

### Method 3: Conda Environment
```bash
# Create conda environment
conda create -n sec-analyst python=3.11

# Activate
conda activate sec-analyst

# Install dependencies
pip install -r requirements.txt
```

---

## 📋 System Requirements

### Minimum
- **CPU**: 2 cores
- **RAM**: 2GB
- **Disk**: 2GB free
- **OS**: Windows 10, macOS 10.14+, Ubuntu 20.04+

### Recommended
- **CPU**: 4+ cores
- **RAM**: 4GB+
- **Disk**: 5GB free
- **OS**: Latest version
- **Internet**: Stable connection for API calls

---

## 🔄 Updating

### Update Dependencies
```bash
# Pull latest requirements
git pull  # if using git

# Update packages
pip install --upgrade -r requirements.txt
```

### Update API Key
```bash
# Edit .env file
nano .env

# Change the key
GOOGLE_API_KEY=new_key_here
```

---

## 🧹 Uninstallation

### Remove Virtual Environment
```bash
# Deactivate
deactivate

# Delete venv
rm -rf venv
```

### Remove Data Files
```bash
# Delete database
rm financial_data.db

# Delete vector store
rm -rf chroma_db

# Delete cache
rm -rf __pycache__
rm -rf .streamlit
```

### Complete Removal
```bash
# Delete entire project
cd ..
rm -rf sec_financial_analyst
```

---

## ✅ Verification Commands

Run these to verify everything is working:

```bash
# Check Python version
python --version
# Should be 3.8+

# Check pip
pip --version

# Check installations
pip list | grep langchain
pip list | grep streamlit

# Check API key (don't share output!)
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ Key loaded' if os.getenv('GOOGLE_API_KEY') else '❌ Key not found')"

# Test imports
python -c "from langchain_google_genai import ChatGoogleGenerativeAI; print('✅ Gemini OK')"

# Test database
python -c "from database import FinancialDatabase; db = FinancialDatabase(); print('✅ Database OK')"
```

---

## 🎓 Post-Installation

### Learn the Codebase
1. Read `README.md` - Full documentation
2. Read `QUICKSTART.md` - Quick reference
3. Read `PROJECT_SUMMARY.md` - Architecture overview
4. Explore `agent.py` - Core logic
5. Check `streamlit_app.py` - UI code

### Try Example Queries
See `QUICKSTART.md` for 12+ example queries to test the system.

### Customize
- Add your own financial data in `data_loader.py`
- Modify prompts in `agent.py`
- Adjust UI in `streamlit_app.py`

---

## 🆘 Getting Help

### Resources
- **Documentation**: README.md, QUICKSTART.md
- **LangChain**: https://python.langchain.com/
- **Streamlit**: https://docs.streamlit.io/
- **Gemini**: https://ai.google.dev/

### Common Issues
- API key issues → Check .env file format
- Import errors → Reinstall requirements.txt
- Slow performance → Normal on first run (downloading model)
- Empty results → Check sample data loaded

---

## 🎉 Success!

If you see this in your browser:

```
📊 SEC Financial Analyst
AI-Powered Financial Analysis with LangGraph & Gemini
✅ System initialized successfully!
```

**Congratulations! 🎊 You're ready to analyze financial data!**

Try your first query:
```
What was Apple's revenue in 2023?
```

---

**Happy Analyzing! 📈**
