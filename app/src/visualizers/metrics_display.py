import streamlit as st
import pandas as pd
from typing import Dict

def display_metrics(stats: Dict):
    """Display key metrics in a formatted layout."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Median Price", 
            f"${stats['median_price']:,.2f}" if 'median_price' in stats else "N/A"
        )
    
    with col2:
        st.metric(
            "Median Price/Sq.Ft", 
            f"${stats['median_price_per_sqft']:,.2f}" if 'median_price_per_sqft' in stats else "N/A"
        )
    
    with col3:
        st.metric(
            "Total Properties", 
            stats['total_properties'] if 'total_properties' in stats else "N/A"
        )
    
    with col4:
        if 'price_range' in stats and all(pd.notna(x) for x in stats['price_range']):
            range_display = f"${stats['price_range'][0]:,.0f} - ${stats['price_range'][1]:,.0f}"
        else:
            range_display = "N/A"
        st.metric("Price Range", range_display)

# Add export of the function
__all__ = ['display_metrics']