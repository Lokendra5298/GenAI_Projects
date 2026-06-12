# agent.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from llm import get_gemini_model
from tools import sql_filter, vector_rag_search, fetch_pdf_texts
import operator

class AgentState(TypedDict):
    messages: Annotated[List[AIMessage | HumanMessage], operator.add]
    filtered_ids: List[str]
    rag_results: List[dict]
    pdf_texts: str
    final_response: str

def router_node(state: AgentState) -> AgentState:
    model = get_gemini_model()
    last_message = state['messages'][-1].content
    tools_needed_prompt = f"Analyze query: {last_message}. Decide which tools to use: sql_filter, vector_rag_search, fetch_pdf_texts. Respond with a list of tools and parameters."
    response = model.invoke(tools_needed_prompt).content
    
    # Parse response (assuming response is a string like "sql_filter: query=recent cs.AI; vector_rag_search: query=Low-rank Adaptation, top_k=5")
    tools_to_call = parse_tools_from_response(response)  # Implement this parser
    
    if 'sql_filter' in tools_to_call:
        state['filtered_ids'] = sql_filter(tools_to_call['sql_filter']['query'])
    
    if 'vector_rag_search' in tools_to_call:
        state['rag_results'] = vector_rag_search(
            tools_to_call['vector_rag_search']['query'],
            tools_to_call['vector_rag_search'].get('top_k', 5)
        )
    
    return state

def pdf_node(state: AgentState) -> AgentState:
    ids = state.get('filtered_ids') or [r['id'] for r in state.get('rag_results', [])]
    if ids:
        state['pdf_texts'] = fetch_pdf_texts(ids)
    return state

def synthesis_node(state: AgentState) -> AgentState:
    model = get_gemini_model()
    synthesis_prompt = f"Query: {state['messages'][-1].content}\nPDF Texts: {state['pdf_texts']}\nGenerate a comprehensive response."
    response = model.invoke(synthesis_prompt)
    state['final_response'] = response.content
    state['messages'].append(AIMessage(content=state['final_response']))
    return state

def parse_tools_from_response(response: str) -> dict:
    # Simple parser: split by ; and :
    tools = {}
    for part in response.split(';'):
        if ':' in part:
            tool, params = part.split(':', 1)
            tool = tool.strip()
            param_dict = {}
            for p in params.split(','):
                if '=' in p:
                    k, v = p.split('=')
                    param_dict[k.strip()] = v.strip()
            tools[tool] = param_dict
    return tools

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("router", router_node)
    workflow.add_node("pdf", pdf_node)
    workflow.add_node("synthesis", synthesis_node)
    
    workflow.set_entry_point("router")
    workflow.add_edge("router", "pdf")
    workflow.add_edge("pdf", "synthesis")
    workflow.add_edge("synthesis", END)
    
    return workflow.compile()