"""LangChain Tools for Financial Analysis"""
from langchain.tools import Tool
from langchain.agents import tool
from database import FinancialDatabase
from vectorstore import FinancialVectorStore
from typing import List


class FinancialTools:
    def __init__(self, db: FinancialDatabase, vectorstore: FinancialVectorStore):
        self.db = db
        self.vectorstore = vectorstore
    
    @tool
    def sql_query_tool(query: str) -> str:
        """
        Execute SQL queries on financial metrics database.
        Use this for quantitative questions about revenue, income, assets, etc.
        Example: SELECT revenue FROM financial_metrics WHERE company_ticker='AAPL' AND fiscal_year=2023
        """
        # This will be bound later with actual db instance
        pass
    
    @tool
    def vector_search_tool(query: str) -> str:
        """
        Search qualitative financial information like management discussions and risk factors.
        Use this for sentiment analysis, strategy questions, and risk assessments.
        """
        # This will be bound later with actual vectorstore instance
        pass
    
    def get_tools(self) -> List[Tool]:
        """Return list of configured tools"""
        
        def sql_search(query: str) -> str:
            """Execute SQL query"""
            try:
                result = self.db.execute_query(query)
                if result.empty:
                    return "No results found."
                return result.to_string(index=False)
            except Exception as e:
                return f"Error executing query: {str(e)}"
        
        def vector_search(query: str) -> str:
            """Perform vector similarity search"""
            try:
                docs = self.vectorstore.similarity_search(query, k=3)
                if not docs:
                    return "No relevant information found."
                
                results = []
                for i, doc in enumerate(docs, 1):
                    results.append(f"Result {i}:\n{doc.page_content}\n")
                return "\n".join(results)
            except Exception as e:
                return f"Error searching: {str(e)}"
        
        return [
            Tool(
                name="SQL_Database",
                func=sql_search,
                description="Execute SQL queries on financial metrics. Use for quantitative data like revenue, net income, assets. Input should be a valid SQL query."
            ),
            Tool(
                name="Vector_Search",
                func=vector_search,
                description="Search qualitative financial information. Use for management discussions, risk factors, strategy, and sentiment analysis. Input should be a natural language question."
            )
        ]
