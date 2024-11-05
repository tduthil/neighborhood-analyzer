import pandas as pd
from typing import Dict

class NeighborhoodAnalyzer:
    """Analyzes neighborhood data and provides statistical insights."""
    
    def __init__(self, df: pd.DataFrame, mapped_headers: Dict[str, str]):
        self.df = df
        self.headers = mapped_headers
        self.process_data()
    
    def process_data(self):
        """Process the raw data for analysis."""
        self.processed_df = self.df.copy()
        price_col = self.headers['price']
        
        # Convert price to numeric if it's not already
        if self.processed_df[price_col].dtype == object:
            self.processed_df[price_col] = pd.to_numeric(
                self.processed_df[price_col].astype(str).str.replace('$', '').str.replace(',', ''), 
                errors='coerce'
            )
        
        # Convert sqft if available
        if 'sqft' in self.headers:
            sqft_col = self.headers['sqft']
            self.processed_df[sqft_col] = pd.to_numeric(self.processed_df[sqft_col], errors='coerce')
    
    def get_basic_stats(self) -> Dict:
        """Calculate basic statistics for the neighborhood."""
        price_col = self.headers['price']
        
        stats = {
            'median_price': self.processed_df[price_col].median(),
            'total_properties': len(self.processed_df),
            'price_range': (
                self.processed_df[price_col].min(),
                self.processed_df[price_col].max()
            )
        }
        
        # Add price per sqft if sqft data is available
        if 'sqft' in self.headers:
            sqft_col = self.headers['sqft']
            valid_mask = (self.processed_df[price_col].notna() & 
                         self.processed_df[sqft_col].notna() & 
                         (self.processed_df[sqft_col] > 0))
            
            if valid_mask.any():
                price_per_sqft = (self.processed_df[price_col][valid_mask] / 
                                self.processed_df[sqft_col][valid_mask])
                stats['median_price_per_sqft'] = price_per_sqft.median()
        
        return stats