from typing import Dict
import pandas as pd
import numpy as np
import streamlit as st

class NeighborhoodAnalyzer:
    """Analyzes neighborhood data and provides statistical insights."""
    
    @staticmethod
    def clean_price(price_str):
        if pd.isna(price_str):
            return np.nan
        try:
            return float(str(price_str).replace('$', '').replace(',', ''))
        except:
            return np.nan
    
    def __init__(self, df: pd.DataFrame, mapped_headers: Dict[str, str]):
        self.df = df
        self.headers = mapped_headers
        self.process_data()
    
    def process_data(self):
        """Process the raw data for analysis."""
        self.processed_df = self.df.copy()
        
        # Clean price data
        if 'price' in self.headers:
            price_col = self.headers['price']
            self.processed_df['clean_price'] = self.processed_df[price_col].apply(self.clean_price)
        
        # Clean square footage data
        if 'sqft' in self.headers:
            sqft_col = self.headers['sqft']
            self.processed_df['clean_sqft'] = pd.to_numeric(
                self.processed_df[sqft_col], 
                errors='coerce'
            )
        
        # Show processing results
        ##st.write("Processed data sample:", self.processed_df.head())
    
    def get_basic_stats(self) -> Dict:
        """Calculate basic statistics for the neighborhood."""
        stats = {}
        
        try:
            valid_prices = self.processed_df[
                self.processed_df['clean_price'].notna() & 
                (self.processed_df['clean_price'] > 1000)
            ]
            
            if len(valid_prices) > 0:
                stats['avg_price'] = valid_prices['clean_price'].mean()
                stats['total_properties'] = len(valid_prices)
                stats['price_range'] = (
                    valid_prices['clean_price'].min(),
                    valid_prices['clean_price'].max()
                )
                
                if 'clean_sqft' in self.processed_df.columns:
                    valid_records = valid_prices[
                        valid_prices['clean_sqft'].notna() & 
                        (valid_prices['clean_sqft'] > 0)
                    ]
                    if len(valid_records) > 0:
                        stats['avg_price_per_sqft'] = (
                            valid_records['clean_price'] / 
                            valid_records['clean_sqft']
                        ).mean()
            
            #st.write("Stats calculated from records:", len(valid_prices))
            #st.write("Available statistics:", list(stats.keys()))
            
            return stats
            
        except Exception as e:
            st.error(f"Error calculating stats: {str(e)}")
            return stats