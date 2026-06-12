# main.py
from data_loader import load_data
from data_base import setup_db
from rag import build_vector_store
from agent import build_graph
from langchain_core.messages import HumanMessage

if __name__ == "__main__":
    # Setup
    df = load_data()
    setup_db(df)
    build_vector_store(df)
    
    # Run example
    app = build_graph()
    query = "Find me recent papers on 'Low-rank Adaptation' and explain how they differ from standard fine-tuning."
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "filtered_ids": [],
        "rag_results": [],
        "pdf_texts": "",
        "final_response": ""
    }
    result = app.invoke(initial_state)
    print(result['final_response'])