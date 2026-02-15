"""LangGraph Agent for Financial Analysis"""
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import FinancialTools
from llm import get_gemini_llm
import operator


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    response: str


class FinancialAgent:
    def __init__(self, tools: FinancialTools):
        self.llm = get_gemini_llm(temperature=0.2)
        self.tools_list = tools.get_tools()
        self.agent_executor = self._create_agent()
    
    def _create_agent(self):
        """Create agent with tools"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial analyst assistant specializing in SEC 10-K filings.

You have access to two tools:
1. SQL_Database: For quantitative metrics (revenue, income, assets, etc.)
2. Vector_Search: For qualitative information (management discussion, risk factors)

When answering questions:
- Use SQL for numerical comparisons and financial metrics
- Use Vector Search for strategic insights, risks, and sentiment
- Combine both tools when needed for comprehensive answers
- Be specific and cite your sources
- Format numbers clearly with proper units (billions, millions)"""),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools_list, prompt)
        return AgentExecutor(agent=agent, tools=self.tools_list, verbose=True)
    
    def invoke(self, query: str) -> str:
        """Run the agent on a query"""
        try:
            result = self.agent_executor.invoke({"input": query})
            return result["output"]
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def create_graph(self):
        """Create LangGraph workflow (simplified)"""
        workflow = StateGraph(AgentState)
        
        def agent_node(state: AgentState):
            query = state["query"]
            response = self.invoke(query)
            return {"response": response, "messages": [AIMessage(content=response)]}
        
        workflow.add_node("agent", agent_node)
        workflow.set_entry_point("agent")
        workflow.add_edge("agent", END)
        
        return workflow.compile()
