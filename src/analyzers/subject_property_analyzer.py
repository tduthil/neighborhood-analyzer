import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

class SubjectPropertyAnalyzer:
    def __init__(self, df: pd.DataFrame, mapped_headers: dict, subject_property: dict):
        self.df = df
        self.headers = mapped_headers
        self.subject = subject_property
        self.process_data()
    
    def process_data(self):
        """Process data for comparison."""
        price_col = self.headers['price']
        
        # Handle price data that might be either string or numeric
        if self.df[price_col].dtype == object:
            # If string, clean it
            self.df['price_clean'] = pd.to_numeric(
                self.df[price_col].astype(str).str.replace('$', '').str.replace(',', ''), 
                errors='coerce'
            )
        else:
            # If already numeric, just copy
            self.df['price_clean'] = pd.to_numeric(self.df[price_col], errors='coerce')
    
    def get_neighborhood_avg(self):
        """Get neighborhood average price."""
        return self.df['price_clean'].mean()
    
    def get_exact_models_avg(self):
        """Get average price for exact matches (beds, baths, sqft)."""
        beds_col = self.headers['beds']
        baths_col = self.headers['baths']
        sqft_col = self.headers['sqft']
        
        # Define tolerances
        SQFT_TOLERANCE = 5  # Allow ±5 sqft difference
        
        mask = (
            (pd.to_numeric(self.df[beds_col], errors='coerce') == self.subject['beds']) &
            (pd.to_numeric(self.df[baths_col], errors='coerce') == self.subject['baths']) &
            (abs(pd.to_numeric(self.df[sqft_col], errors='coerce') - self.subject['sqft']) <= SQFT_TOLERANCE)
        )
        
        matches = self.df[mask]
        return matches['price_clean'].mean() if not matches.empty else np.nan
    
    def get_similar_models_avg(self):
        """Get average price for similar models (same beds)."""
        beds_col = self.headers['beds']
        mask = (pd.to_numeric(self.df[beds_col], errors='coerce') == self.subject['beds'])
        matches = self.df[mask]
        return matches['price_clean'].mean() if not matches.empty else np.nan
    
    def get_comparison_results(self):
        """Get all comparison metrics."""
        return {
            'neighborhood_avg': self.get_neighborhood_avg(),
            'exact_models_avg': self.get_exact_models_avg(),
            'similar_models_avg': self.get_similar_models_avg(),
            'subject_price': self.subject['price']
        }
    
    def get_decision(self):
        """Get decision based on comparison results."""
        results = self.get_comparison_results()
        
        # Count how many averages are above subject price
        comps = [
            results['neighborhood_avg'],
            results['exact_models_avg'],
            results['similar_models_avg']
        ]
        
        valid_comps = [comp for comp in comps if not np.isnan(comp)]
        if not valid_comps:
            return "INVESTIGATE"
            
        higher_count = sum(1 for comp in valid_comps if comp > results['subject_price'])
        
        if higher_count >= len(valid_comps):
            return "BUY"
        elif higher_count <= 1:
            return "PASS"
        else:
            return "INVESTIGATE"
    
    def plot_comparison_chart(self):
        """Create visualization comparing subject property to neighborhood data."""
        results = self.get_comparison_results()
        
        fig = go.Figure()
        
        # Add neighborhood distribution
        fig.add_trace(go.Histogram(
            x=self.df['price_clean'],
            name='Neighborhood Sales',
            opacity=0.7,
            nbinsx=30
        ))
        
        # Add vertical lines for comparisons
        comparisons = {
            'Subject Price': results['subject_price'],
            'Neighborhood Avg': results['neighborhood_avg'],
            'Similar Models Avg': results['similar_models_avg'],
            'Exact Models Avg': results['exact_models_avg']
        }
        
        colors = {
            'Subject Price': '#FF4B4B',      # Brighter red
            'Neighborhood Avg': '#00CED1',    # Bright turquoise
            'Similar Models Avg': '#50C878',  # Emerald green
            'Exact Models Avg': '#BA55D3'     # Bright purple
        }
        
        # Calculate range for positioning labels
        price_range = [
            min(v for v in comparisons.values() if not pd.isna(v)),
            max(v for v in comparisons.values() if not pd.isna(v))
        ]
        range_size = price_range[1] - price_range[0]
        
        # Position labels at different y-coordinates
        label_positions = {
            'Subject Price': 1.15,
            'Neighborhood Avg': 1.10,
            'Similar Models Avg': 1.05,
            'Exact Models Avg': 1.00
        }
        
        # Add lines and labels with different positions
        for i, (name, value) in enumerate(comparisons.items()):
            if not pd.isna(value):
                fig.add_vline(
                    x=value,
                    line_dash="dash",
                    line_color=colors[name],
                    annotation={
                        'text': f"{name}:<br>${value:,.0f}",
                        'y': label_positions[name],
                        'yref': 'paper',
                        'showarrow': False,
                        'font': {'size': 12, 'color': colors[name]},  # Increased font size from 10 to 12
                        'bgcolor': 'rgba(14, 17, 23, 0.8)',
                        'bordercolor': colors[name],
                        'borderwidth': 2,  # Increased from 1 to 2 for more visibility
                        'borderpad': 4,
                        'align': 'center'
                    }
                )
        
        # Update layout with dark theme
        fig.update_layout(
            title={
                'text': "Subject Property Price Comparison",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': 'white'}  # White text for title
            },
            xaxis_title="Price",
            yaxis_title="Number of Sales",
            showlegend=True,
            margin={'t': 100, 'b': 50, 'l': 50, 'r': 50},
            height=500,
            plot_bgcolor='#0E1117',    # Dark background
            paper_bgcolor='#0E1117',   # Dark background
            font={'color': 'white'},   # White text for all labels
            xaxis={
                'gridcolor': 'rgba(255, 255, 255, 0.1)',  # Subtle grid
                'showgrid': True,
                'zeroline': False,
                'title': {'font': {'color': 'white'}},    # White axis title
                'tickfont': {'color': 'white'}            # White tick labels
            },
            yaxis={
                'gridcolor': 'rgba(255, 255, 255, 0.1)',  # Subtle grid
                'showgrid': True,
                'zeroline': False,
                'title': {'font': {'color': 'white'}},    # White axis title
                'tickfont': {'color': 'white'}            # White tick labels
            },
            legend={
                'font': {'color': 'white'},               # White legend text
                'bgcolor': 'rgba(14, 17, 23, 0.8)'        # Semi-transparent dark background
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)