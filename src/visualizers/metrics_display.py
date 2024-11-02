import streamlit as st
from typing import Dict
import pandas as pd
import numpy as np

def display_metrics(stats: Dict):
    """Display key metrics in a formatted layout."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_price = stats['avg_price']
        if pd.notna(avg_price):
            st.metric("Average Price", f"${avg_price:,.2f}")
        else:
            st.metric("Average Price", "N/A")
    
    with col2:
        avg_ppsf = stats.get('avg_price_per_sqft')
        if pd.notna(avg_ppsf):
            st.metric("Price per Sq.Ft", f"${avg_ppsf:,.2f}")
        else:
            st.metric("Price per Sq.Ft", "N/A")
    
    with col3:
        st.metric("Total Properties", stats['total_properties'])
    
    with col4:
        if pd.notna(stats['price_range'][0]) and pd.notna(stats['price_range'][1]):
            st.metric(
                "Price Range", 
                f"${stats['price_range'][0]:,.0f} - ${stats['price_range'][1]:,.0f}"
            )
        else:
            st.metric("Price Range", "N/A")