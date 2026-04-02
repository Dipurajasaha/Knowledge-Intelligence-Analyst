import pandas as pd

import pandas as pd
import re

def clean_text(text: str) -> str:
    """
    Standardizes text by converting it to lowercase, stripping URLs, 
    removing unwanted special characters, and normalizing whitespace.
    """
    if not isinstance(text, str):
        return ""
    
    # Convert text to lowercase for uniformity across the dataset
    text = text.lower()
    
    # Identify and remove web links (http, https, www)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Filter out special symbols, keeping only alphanumeric characters and basic punctuation
    text = re.sub(r'[^a-z0-9\s.,!?]', '', text)
    
    # Collapse multiple consecutive spaces into a single space and trim edges
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def prepare_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the raw dataframe by removing invalid/empty data, 
    applying the text cleaning function, and enforcing a strict column schema.
    """
    if df is None or df.empty:
        return pd.DataFrame()
        
    print("\nStarting Data Cleaning & Preparation...")
    initial_len = len(df)
    
    # Drop rows that are fundamentally missing their core content
    df = df.dropna(subset=["text", "title"])
    
    # Apply the regex cleaning transformations to the text fields
    print("   -> Removing noise, URLs, and formatting text...")
    df.loc[:, "text"] = df["text"].apply(clean_text)
    df.loc[:, "title"] = df["title"].apply(clean_text)
    
    # Drop rows that became completely empty *after* the regex cleaning stripped the noise
    df = df[df["text"].str.strip() != ""]
    
    # Keep only rows with meaningful length (filters out 1-word garbage posts or empty titles)
    df = df[df["text"].str.len() > 20] 
    
    # Remove exact text duplicates to prevent skewing the analysis with cross-posted spam
    df = df.drop_duplicates(subset=["text"])
    
    # Enforce a consistent dataset schema across all platforms
    expected_columns = ["topic", "platform", "title", "text", "date", "engagement", "url"]
    for col in expected_columns:
        if col not in df.columns:
            # Fill any completely missing columns with None to prevent downstream crashes
            df[col] = None 
            
    # Reorder the dataframe to match the strict schema layout
    df = df[expected_columns] 
    
    final_len = len(df)
    print(f"Data Cleaning Complete! Removed {initial_len - final_len} noisy/duplicate rows.")
    print(f"Cleaned Dataset Size: {final_len} rows.")
    
    return df