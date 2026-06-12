# streamlit_app.py
import streamlit as st
from agent import build_graph
from data_loader import load_data
from data_base import setup_db
from rag import build_vector_store
from langchain_core.messages import HumanMessage
import os

st.title("Scholarly Research Navigator")

# Setup data if not done
if 'data_setup' not in st.session_state:
    with st.spinner("Setting up database and vector store... This may take a while."):
        df = load_data()
        setup_db(df)
        build_vector_store(df)
    st.session_state['data_setup'] = True
    st.success("Setup complete!")

query = st.text_input("Enter your query:", "Find me recent papers on 'Low-rank Adaptation' and explain how they differ from standard fine-tuning.")

if st.button("Run Query"):
    with st.spinner("Processing..."):
        app = build_graph()
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "filtered_ids": [],
            "rag_results": [],
            "pdf_texts": "",
            "final_response": ""
        }
        result = app.invoke(initial_state)
        st.write(result['final_response'])