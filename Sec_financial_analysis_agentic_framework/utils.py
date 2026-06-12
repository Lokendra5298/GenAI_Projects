"""Utility Functions"""
from pydantic import BaseModel, Field
from typing import Optional


class FinancialMetrics(BaseModel):
    """Pydantic model for structured financial data extraction"""
    company_ticker: str = Field(description="Stock ticker symbol")
    company_name: str = Field(description="Full company name")
    fiscal_year: int = Field(description="Fiscal year")
    revenue: Optional[float] = Field(description="Total revenue in dollars")
    net_income: Optional[float] = Field(description="Net income in dollars")
    total_assets: Optional[float] = Field(description="Total assets in dollars")
    total_liabilities: Optional[float] = Field(description="Total liabilities in dollars")
    operating_cash_flow: Optional[float] = Field(description="Operating cash flow in dollars")
    eps: Optional[float] = Field(description="Earnings per share")


def format_large_number(num: float) -> str:
    """Format large numbers with B/M suffixes"""
    if num >= 1_000_000_000:
        return f"${num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"${num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"${num / 1_000:.2f}K"
    else:
        return f"${num:.2f}"


def initialize_sample_data(db, vectorstore):
    """Initialize database with sample data"""
    from data_loader import get_sample_financial_data, get_sample_qualitative_data
    
    # Load quantitative data
    financial_data = get_sample_financial_data()
    for data in financial_data:
        try:
            db.insert_metrics(data)
        except:
            pass  # Skip if already exists
    
    # Load qualitative data
    qualitative_docs = get_sample_qualitative_data()
    try:
        vectorstore.add_documents(qualitative_docs)
    except:
        pass  # Skip if already exists
    
    return True


def classify_query(query: str) -> str:
    """Simple query classification"""
    query_lower = query.lower()
    
    sql_keywords = ['revenue', 'income', 'asset', 'liability', 'eps', 'cash flow', 
                    'compare', 'how much', 'financial', 'metric']
    vector_keywords = ['risk', 'strategy', 'management', 'discussion', 'outlook', 
                       'why', 'threat', 'opportunity', 'sentiment']
    
    has_sql = any(keyword in query_lower for keyword in sql_keywords)
    has_vector = any(keyword in query_lower for keyword in vector_keywords)
    
    if has_sql and has_vector:
        return "hybrid"
    elif has_sql:
        return "quantitative"
    elif has_vector:
        return "qualitative"
    else:
        return "general"
