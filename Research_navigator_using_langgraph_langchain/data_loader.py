# data_loader.py
import pandas as pd
import os
import json

DATASET_PATH = "arxiv-metadata-oai-snapshot.json"

# data_loader.py

def load_data():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"File not found: {DATASET_PATH}")

    print(f"Loading from: {os.path.abspath(DATASET_PATH)}")
    
    # Read as regular JSON array (works with your current indented file)
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    print(f"→ Loaded {len(df):,} papers")
    
    if len(df) < 100:
        print("Note: small test dataset detected")
    
    df['update_date'] = pd.to_datetime(df['update_date'])
    df = df[['id', 'title', 'authors', 'categories', 'abstract', 'update_date']]
    return df