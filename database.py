"""SQL Database for Financial Metrics"""
import sqlite3
from typing import List, Dict, Any
import pandas as pd


class FinancialDatabase:
    def __init__(self, db_path="financial_data.db"):
        self.db_path = db_path
        self.conn = None
        self._initialize_db()
    
    def _initialize_db(self):
        """Create tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_ticker TEXT,
                company_name TEXT,
                fiscal_year INTEGER,
                revenue REAL,
                net_income REAL,
                total_assets REAL,
                total_liabilities REAL,
                operating_cash_flow REAL,
                eps REAL
            )
        """)
        self.conn.commit()
    
    def insert_metrics(self, data: Dict[str, Any]):
        """Insert financial metrics"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO financial_metrics 
            (company_ticker, company_name, fiscal_year, revenue, net_income, 
             total_assets, total_liabilities, operating_cash_flow, eps)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('ticker'), data.get('company_name'), data.get('fiscal_year'),
            data.get('revenue'), data.get('net_income'), data.get('total_assets'),
            data.get('total_liabilities'), data.get('operating_cash_flow'), data.get('eps')
        ))
        self.conn.commit()
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return DataFrame"""
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            return pd.DataFrame({"error": [str(e)]})
    
    def get_all_data(self) -> pd.DataFrame:
        """Get all financial data"""
        return pd.read_sql_query("SELECT * FROM financial_metrics", self.conn)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
