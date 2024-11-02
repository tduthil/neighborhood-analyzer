import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict

def clean_price_value(value):
    if pd.isna(value):
        return np.nan
    try:
        str_value = str(value)
        cleaned = str_value.replace('$', '').replace(',', '').replace(' ', '')
        return float(cleaned) if cleaned else np.nan
    except:
        return np.nan

def is_sale_row(row):
    row_str = ' '.join([str(x) for x in row if pd.notna(x)])
    return ('WARRANTY DEED' in row_str and 
            '$' in row_str and
            'Address:' not in row_str and
            'Parcel' not in row_str)

def process_data(df: pd.DataFrame, mapped_headers: Dict[str, str]) -> pd.DataFrame:
    """Process the raw dataframe by cleaning and transforming data."""
    try:
        # Create a copy to avoid modifying original
        processed_df = df.copy()
        
        # Filter for valid sale rows only
        sale_rows = processed_df.apply(is_sale_row, axis=1)
        processed_df = processed_df[sale_rows].copy()
        
        st.write("Initial sale records:", len(processed_df))
        
        # Process price data
        if mapped_headers.get('price'):
            price_col = mapped_headers['price']
            processed_df[price_col] = processed_df[price_col].apply(clean_price_value)
            processed_df = processed_df[processed_df[price_col] > 1000]
            st.write("Valid price records:", len(processed_df))
        
        # Process square footage
        if mapped_headers.get('sqft'):
            sqft_col = mapped_headers['sqft']
            processed_df[sqft_col] = pd.to_numeric(processed_df[sqft_col], errors='coerce')
            processed_df = processed_df[processed_df[sqft_col] > 0]
            
            if mapped_headers.get('price'):
                processed_df['price_per_sqft'] = (
                    processed_df[mapped_headers['price']] / 
                    processed_df[sqft_col]
                )
        
        #st.write("Final processed records:", len(processed_df))
        #st.write("Columns in final data:", processed_df.columns.tolist())
        #st.write("Final data sample:", processed_df.head())
        
        return processed_df
        
    except Exception as e:
        #st.error(f"Processing error details: {str(e)}")
        #st.write("Current state of data:", processed_df.head())
        raise