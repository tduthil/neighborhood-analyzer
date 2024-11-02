from typing import Dict
import pandas as pd
import streamlit as st
from src.constants import HEADER_MAPPINGS, REQUIRED_FIELDS

class HeaderMapper:
    """Maps various possible header names to standardized fields."""
    
    @staticmethod
    def identify_headers(df: pd.DataFrame) -> Dict[str, str]:
        """Identifies relevant headers from the dataframe."""
        headers = df.columns
        mapped_headers = {}
        
        for key, possible_names in HEADER_MAPPINGS.items():
            for header in headers:
                if any(name.lower() in header.lower() for name in possible_names):
                    mapped_headers[key] = header
                    break
        
        # Only show warning if missing fields
        missing_fields = [field for field in REQUIRED_FIELDS if field not in mapped_headers]
        if missing_fields:
            st.warning(f"Missing required fields: {missing_fields}")
            
        return mapped_headers