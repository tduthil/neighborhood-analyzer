import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

def get_unit_stats(df: pd.DataFrame, headers: dict):
    """Calculate statistics for each unique unit type."""
    # Get relevant columns
    beds_col = headers['beds']
    baths_col = headers['baths']
    sqft_col = headers['sqft']
    price_col = headers['price']
    
    # Ensure numeric types for all columns
    df[beds_col] = pd.to_numeric(df[beds_col], errors='coerce')
    df[baths_col] = pd.to_numeric(df[baths_col], errors='coerce')
    df[sqft_col] = pd.to_numeric(df[sqft_col], errors='coerce')
    
    # Create clean price column
    if df[price_col].dtype == object:
        df['price_clean'] = pd.to_numeric(
            df[price_col].astype(str).str.replace('$', '').str.replace(',', ''), 
            errors='coerce'
        )
    else:
        df['price_clean'] = pd.to_numeric(df[price_col], errors='coerce')
    
    # Group by unit type
    grouped = df.groupby([beds_col, baths_col, sqft_col]).agg({
        'price_clean': ['mean', 'count', 'min', 'max']
    }).reset_index()
    
    # Calculate price per sqft
    grouped['price_per_sqft'] = grouped['price_clean']['mean'] / grouped[sqft_col].astype(float)
    
    # Rename columns for clarity
    grouped.columns = ['Beds', 'Baths', 'Sq. Ft', 'Avg Price', 'Count', 'Min Price', 'Max Price', 'Price/SqFt']
    
    return grouped.sort_values(['Beds', 'Baths', 'Sq. Ft'])

def display_unit_analysis(unit_stats: pd.DataFrame):
    """Display unit statistics in a formatted table."""
    # Format numeric columns
    formatted_stats = unit_stats.copy()
    formatted_stats['Avg Price'] = formatted_stats['Avg Price'].map('${:,.2f}'.format)
    formatted_stats['Min Price'] = formatted_stats['Min Price'].map('${:,.2f}'.format)
    formatted_stats['Max Price'] = formatted_stats['Max Price'].map('${:,.2f}'.format)
    formatted_stats['Price/SqFt'] = formatted_stats['Price/SqFt'].map('${:,.2f}'.format)
    
    # Apply styling
    styled_df = formatted_stats.style.set_properties(**{
        'background-color': 'white',
        'color': 'black',
        'border-color': '#e6e6e6',
        'padding': '12px 15px',
        'text-align': 'center'
    })
    
    # Add specific column styling
    styled_df = styled_df.set_table_styles([
        {'selector': 'th',
         'props': [
             ('background-color', '#f8f9fa'),
             ('color', '#782F40'),
             ('font-weight', 'bold'),
             ('text-align', 'center'),
             ('padding', '12px 15px'),
             ('border', '1px solid #e6e6e6')
         ]},
        {'selector': 'td',
         'props': [
             ('text-align', 'center'),
             ('padding', '12px 15px'),
             ('border', '1px solid #e6e6e6')
         ]},
        {'selector': '',
         'props': [
             ('border-collapse', 'collapse'),
             ('margin', '25px auto'),
             ('font-size', '14px'),
             ('width', '100%'),
             ('box-shadow', '0 0 20px rgba(0, 0, 0, 0.1)')
         ]}
    ])
    
    # Add hover effect
    styled_df = styled_df.set_table_styles([
        {'selector': 'tbody tr:hover',
         'props': [('background-color', '#f5f5f5')]},
    ], overwrite=False)
    
    # Center the table in the column and add padding
    st.markdown(
        """
        <style>
        .stDataFrame {
            width: 100%;
            margin: 25px 0;
        }
        .stDataFrame > div {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Display the styled table
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )


def display_unit_price_charts(unit_stats: pd.DataFrame):
    """Display visualizations of price/sqft by unit type."""
    fig = px.bar(
        unit_stats,
        x='Beds',
        y='Price/SqFt',
        color='Baths',
        title='Average Price per Square Foot by Unit Type',
        error_y='Count',  # Shows volume as error bars
        barmode='group',
        hover_data=['Sq. Ft', 'Count']
    )
    
    fig.update_layout(
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        font={'color': 'white'},
        xaxis={'title': 'Bedrooms'},
        yaxis={'title': 'Price per Square Foot ($)'}
    )
    
    st.plotly_chart(fig, use_container_width=True)