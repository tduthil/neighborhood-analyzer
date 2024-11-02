from typing import Dict, Tuple
import pandas as pd
import streamlit as st
import numpy as np

class DataValidator:
    """Validates and processes input data."""
    
    @staticmethod
    def clean_price(price_str):
        if pd.isna(price_str):
            return np.nan
        try:
            # Remove $ and , then convert to float
            return float(str(price_str).replace('$', '').replace(',', ''))
        except:
            return np.nan
    
    @staticmethod
    def validate_data(df: pd.DataFrame, mapped_headers: Dict[str, str]) -> Tuple[bool, str]:
        """Validates the input dataframe and returns validation status and message."""
        try:
            #st.write("Starting validation with shape:", df.shape)
            
            # Clean and validate price data
            if 'price' in mapped_headers:
                price_col = mapped_headers['price']
                df['clean_price'] = df[price_col].apply(DataValidator.clean_price)
                valid_prices = df['clean_price'] > 1000
                
                #st.write("Price column:", price_col)
                #st.write("Sample of original prices:", df[price_col].head())
                #st.write("Sample of cleaned prices:", df['clean_price'].head())
                #st.write("Number of valid prices:", valid_prices.sum())
                
                if valid_prices.sum() == 0:
                    return False, "No valid price data found"
            else:
                return False, "Price column not found"
            
            # Validate square footage if available
            if 'sqft' in mapped_headers:
                sqft_col = mapped_headers['sqft']
                df['clean_sqft'] = pd.to_numeric(df[sqft_col], errors='coerce')
                valid_sqft = df['clean_sqft'] > 0
                #st.write("Number of valid square footage records:", valid_sqft.sum())
            
            return True, "Data validation successful"
            
        except Exception as e:
            #st.error(f"Validation error details: {str(e)}")
            #st.write("DataFrame info:", df.info())
            return False, f"Error validating data: {str(e)}"