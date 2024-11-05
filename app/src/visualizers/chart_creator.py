import plotly.express as px
import pandas as pd
from src.constants import BRAND_COLOR

def create_price_trends_chart(df: pd.DataFrame, date_column: str, price_column: str):
    """Generate price trends visualization."""
    df['date'] = pd.to_datetime(df[date_column])
    
    fig = px.line(
        df.sort_values('date'),
        x='date',
        y=price_column,
        title='Price Trends Over Time',
        line_shape='spline'
    )
    fig.update_traces(line_color=BRAND_COLOR)
    return fig

def create_price_distribution_chart(df: pd.DataFrame, price_column: str):
    """Generate price distribution visualization."""
    fig = px.histogram(
        df,
        x=price_column,
        nbins=30,
        title='Price Distribution'
    )
    fig.update_traces(marker_color=BRAND_COLOR)
    return fig