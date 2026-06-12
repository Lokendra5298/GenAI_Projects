# data_base.py
from langchain_community.utilities import SQLDatabase
import sqlite3
import os

DB_PATH = "arxiv.db"

def setup_db(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('papers', conn, if_exists='replace', index=False)
    conn.close()

def get_db():
    return SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")