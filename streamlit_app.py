"""Streamlit UI for SEC Financial Analyst"""
import streamlit as st
import pandas as pd
from database import FinancialDatabase
from vectorstore import FinancialVectorStore
from tools import FinancialTools
from agent import FinancialAgent
from rag import FinancialRAG
from utils import initialize_sample_data, classify_query
import os


# Page config
st.set_page_config(
    page_title="SEC Financial Analyst",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Initialize all components"""
    db = FinancialDatabase("financial_data.db")
    vectorstore = FinancialVectorStore("./chroma_db")
    
    # Initialize with sample data
    initialize_sample_data(db, vectorstore)
    
    tools = FinancialTools(db, vectorstore)
    agent = FinancialAgent(tools)
    rag = FinancialRAG(vectorstore)
    
    return db, vectorstore, agent, rag


def main():
    # Header
    st.markdown('<h1 class="main-header">📊 SEC Financial Analyst</h1>', unsafe_allow_html=True)
    st.markdown("### AI-Powered Financial Analysis with LangGraph & Gemini")
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("⚠️ GOOGLE_API_KEY not found! Please set it in your .env file")
        st.code("GOOGLE_API_KEY=your_api_key_here")
        st.stop()
    
    # Initialize system
    try:
        db, vectorstore, agent, rag = initialize_system()
        st.success("✅ System initialized successfully!")
    except Exception as e:
        st.error(f"Error initializing system: {str(e)}")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        mode = st.selectbox(
            "Analysis Mode",
            ["Agent (Recommended)", "RAG Only"],
            help="Agent mode uses multiple tools, RAG mode uses retrieval only"
        )
        
        st.divider()
        
        st.subheader("📈 Available Data")
        st.write("Companies: AAPL, MSFT, GOOGL")
        st.write("Years: 2022-2023")
        
        st.divider()
        
        if st.button("🔄 View Database"):
            with st.spinner("Loading data..."):
                df = db.get_all_data()
                st.dataframe(df, use_container_width=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Ask a Financial Question")
        
        # Example questions
        with st.expander("📝 Example Questions"):
            st.markdown("""
            **Quantitative:**
            - What was Apple's revenue in 2023?
            - Compare Microsoft and Apple's net income in 2023
            - Show me all companies with revenue over 300 billion
            
            **Qualitative:**
            - What are the main risks for Apple?
            - Summarize Microsoft's management discussion
            - What is Alphabet's business strategy?
            
            **Hybrid:**
            - Which company has the best financial performance and lowest risks?
            - How did supply chain issues affect Apple's revenue?
            """)
        
        # Query input
        query = st.text_area(
            "Your Question:",
            placeholder="e.g., What was Apple's revenue in 2023?",
            height=100
        )
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            analyze_button = st.button("🔍 Analyze", type="primary")
        with col_btn2:
            clear_button = st.button("🗑️ Clear")
        
        if clear_button:
            st.rerun()
        
        # Process query
        if analyze_button and query:
            with st.spinner("🤔 Analyzing..."):
                try:
                    if mode == "Agent (Recommended)":
                        response = agent.invoke(query)
                    else:
                        result = rag.query(query)
                        response = result["answer"]
                    
                    st.success("✅ Analysis Complete!")
                    st.markdown("### 📊 Answer:")
                    st.write(response)
                    
                    # Save to session state
                    if "history" not in st.session_state:
                        st.session_state.history = []
                    st.session_state.history.append({"query": query, "response": response})
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        st.subheader("🎯 Query Analysis")
        if query:
            query_type = classify_query(query)
            st.info(f"**Type:** {query_type.title()}")
            
            if query_type == "quantitative":
                st.write("🔢 This query requires numerical data from SQL database")
            elif query_type == "qualitative":
                st.write("📝 This query requires text analysis from vector store")
            elif query_type == "hybrid":
                st.write("🔄 This query requires both SQL and vector search")
            else:
                st.write("💭 General query - agent will determine best approach")
    
    # History
    if "history" in st.session_state and st.session_state.history:
        st.divider()
        st.subheader("📜 Query History")
        for i, item in enumerate(reversed(st.session_state.history[-5:]), 1):
            with st.expander(f"Query {i}: {item['query'][:50]}..."):
                st.write("**Q:**", item['query'])
                st.write("**A:**", item['response'])


if __name__ == "__main__":
    main()
