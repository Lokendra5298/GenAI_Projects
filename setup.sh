#!/bin/bash

echo "=================================================="
echo "SEC Financial Analyst - Setup Script"
echo "=================================================="
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python --version

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo ""
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your GOOGLE_API_KEY"
else
    echo ""
    echo "✅ .env file already exists"
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your GOOGLE_API_KEY"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the app: streamlit run streamlit_app.py"
echo ""
echo "=================================================="
