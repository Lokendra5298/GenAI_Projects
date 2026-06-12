"""Main Entry Point for SEC Financial Analyst"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_api_key():
    """Check if API key is set"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("=" * 60)
        print("ERROR: GOOGLE_API_KEY not found!")
        print("=" * 60)
        print("\nPlease create a .env file with your API key:")
        print("GOOGLE_API_KEY=your_api_key_here")
        print("\nGet your API key from: https://makersuite.google.com/app/apikey")
        print("=" * 60)
        sys.exit(1)
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("SEC Financial Analyst - LangGraph + Gemini")
    print("=" * 60)
    
    # Check API key
    check_api_key()
    
    print("\n✅ API Key found!")
    print("\n🚀 Starting Streamlit app...")
    print("\nRun the following command to start:")
    print("streamlit run streamlit_app.py")
    print("\n" + "=" * 60)
    
    # Import and run streamlit app
    os.system("streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()
