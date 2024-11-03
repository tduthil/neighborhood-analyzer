import sys
from pathlib import Path
import io

# Add the project root directory to Python path
file_path = Path(__file__).parent.absolute()
sys.path.append(str(file_path))

import streamlit as st
import pandas as pd
import re

# Import after path setup
from src.constants import CUSTOM_CSS
from src.data_handlers.header_mapper import HeaderMapper
from src.data_handlers.data_validator import DataValidator
from src.analyzers.neighborhood_analyzer import NeighborhoodAnalyzer
from src.visualizers.chart_creator import create_price_trends_chart, create_price_distribution_chart
from src.visualizers.metrics_display import display_metrics
from src.analyzers.subject_property_analyzer import SubjectPropertyAnalyzer
from src.analyzers.unit_analyzer import get_unit_stats, display_unit_analysis, display_unit_price_charts

def get_subject_property_details():
    """Get subject property details from user input."""
    st.subheader("Subject Property Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject_address = st.text_input("Property Address")
        subject_beds = st.number_input("Bedrooms", min_value=0, max_value=10, step=1)
        subject_baths = st.number_input("Bathrooms", min_value=0.0, max_value=10.0, step=0.5)
    
    with col2:
        subject_sqft = st.number_input("Square Feet", min_value=0, step=1)
        subject_price = st.number_input("Asking Price", min_value=0, step=1000)
    
    return {
        'address': subject_address,
        'beds': subject_beds,
        'baths': subject_baths,
        'sqft': subject_sqft,
        'price': subject_price
    }

def detect_county(filename):
    """Detect county based on file name or content."""
    filename = filename.lower()
    if 'sutton' in filename:
        return 'Seminole County'
    elif 'anthem' in filename:
        return 'Orange County'
    elif 'audobon' in filename:
        return 'Orange County'
    elif 'baylake' in filename:
        return 'Orange County'
    else:
        return 'Unknown County'

def detect_file_format(file_content, filename):
    """Detect the format of the input file."""
    content_str = file_content.decode('utf-8')
    
    # Check file format based on content patterns
    if 'Address:' in content_str and 'Parcel #:' in content_str:
        return 'seminole_format'
    elif 'sep=$' in content_str:
        return 'dollar_delimited'
    else:
        return 'standard_csv'

def read_dollar_delimited(file_content):
    """Read a file that uses $ as delimiter."""
    content_str = file_content.decode('utf-8')
    # Skip the 'sep=$' line if present
    if content_str.startswith('sep=$'):
        content_str = '\n'.join(content_str.split('\n')[1:])
    
    # Use StringIO to create a file-like object
    string_io = io.StringIO(content_str)
    return pd.read_csv(string_io, sep='$')

def preprocess_seminole_format(file_content):
    """Preprocess the Seminole County format."""
    lines = file_content.decode('utf-8').split('\n')
    processed_data = []
    current_address = None
    
    for line in lines:
        if not line.strip() or 'Subdivision:' in line or 'Parcel #:' in line:
            continue
            
        if 'Address:' in line:
            match = re.search(r'Address: (.*?) -', line)
            if match:
                current_address = match.group(1).strip()
            continue
            
        if re.search(r'\d{2}/\d{4}|\$\d+,\d+', line):
            date = re.search(r'\d{2}/\d{4}', line)
            price = re.search(r'\$[\d,]+', line)
            numbers = re.findall(r'\b\d+\.?\d*\b', line)
            
            if date and price and len(numbers) >= 3:
                bed = next((float(n) for n in numbers if float(n) < 5), None)
                bath = next((float(n) for n in numbers if '.' in str(n)), None)
                sqft = next((float(n) for n in numbers if float(n) > 1000 and float(n) < 5000), None)
                
                if all(v is not None for v in [bed, bath, sqft]):
                    # Clean price value
                    price_str = price.group(0)
                    price_val = float(price_str.replace('$', '').replace(',', ''))
                    
                    processed_data.append({
                        'Property Address': current_address,
                        'Date': date.group(0),
                        'Sale Amount': price_val,  # Store as float
                        'Bed': bed,
                        'Bath': bath,
                        'Living': sqft
                    })
    
    df = pd.DataFrame(processed_data)
    
    # Ensure numeric types
    numeric_columns = ['Sale Amount', 'Bed', 'Bath', 'Living']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def read_standard_csv(file_content):
    """Read a standard CSV file."""
    return pd.read_csv(io.BytesIO(file_content))

def main():
    st.set_page_config(
        page_title="Neighborhood Analyzer",
        page_icon="🏘️",
        layout="wide",
    )
    
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    st.title("🏘️ Neighborhood Analyzer")
    
    uploaded_file = st.file_uploader(
        "Upload your neighborhood data (CSV)",
        type=['csv'],
        help="Upload a CSV file containing property sales data"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file content
            file_content = uploaded_file.read()
            
            # Detect county and file format
            county = detect_county(uploaded_file.name)
            file_format = detect_file_format(file_content, uploaded_file.name)
            
            # Process file according to its format
            if file_format == 'seminole_format':
                df = preprocess_seminole_format(file_content)
            elif file_format == 'dollar_delimited':
                df = read_dollar_delimited(file_content)
            else:
                df = read_standard_csv(file_content)
            
            # Continue with analysis
            mapped_headers = HeaderMapper.identify_headers(df)
            
            is_valid, message = DataValidator.validate_data(df, mapped_headers)
            
            if not is_valid:
                st.error(message)
                return
            
            analyzer = NeighborhoodAnalyzer(df, mapped_headers)
            stats = analyzer.get_basic_stats()
            
            # Create tabs for different analyses
            tab1, tab2, tab3 = st.tabs(["Neighborhood Overview", "Unit Analysis", "Subject Property Analysis"])
            
            with tab1:
                # Existing neighborhood metrics and charts
                display_metrics(stats)
                
                col1, col2 = st.columns(2)
                with col1:
                    if 'date' in mapped_headers:
                        price_trends = create_price_trends_chart(
                            df, 
                            mapped_headers['date'], 
                            mapped_headers['price']
                        )
                        st.plotly_chart(price_trends, use_container_width=True)
                
                with col2:
                    price_dist = create_price_distribution_chart(
                        df,
                        mapped_headers['price']
                    )
                    st.plotly_chart(price_dist, use_container_width=True)
            
            with tab2:
                st.subheader("Price Analysis by Unit Type")
                # Add the unit breakdown analysis
                unit_stats = get_unit_stats(df, mapped_headers)
                display_unit_analysis(unit_stats)
                
                # Option to show visualization of price/sqft by unit type
                if st.checkbox("Show Price/Sqft Distribution by Unit Type"):
                    display_unit_price_charts(unit_stats)
            
            with tab3:
                # Subject property analysis
                subject_property = get_subject_property_details()
                
                if all(subject_property.values()): # Check if all fields are filled
                    analyzer = SubjectPropertyAnalyzer(df, mapped_headers, subject_property)
                    comparison_results = analyzer.get_comparison_results()
                    decision = analyzer.get_decision()
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        neighborhood_avg = comparison_results['neighborhood_avg']
                        display_value = f"${neighborhood_avg:,.2f}" if pd.notna(neighborhood_avg) else "No Data"
                        st.metric("Neighborhood Avg", display_value)
                    
                    with col2:
                        similar_avg = comparison_results['similar_models_avg']
                        display_value = f"${similar_avg:,.2f}" if pd.notna(similar_avg) else "No Similar Models Found"
                        st.metric("Similar Models Avg", display_value)
                    
                    with col3:
                        exact_avg = comparison_results['exact_models_avg']
                        display_value = f"${exact_avg:,.2f}" if pd.notna(exact_avg) else "No Exact Matches Found"
                        st.metric("Exact Models Avg", display_value)
                    
                    # Decision and visualization
                    decision_color = {
                        "BUY": "green",
                        "INVESTIGATE": "yellow",
                        "PASS": "red"
                    }
                    st.markdown(
                        f"<h2 style='text-align: center; color: {decision_color[decision]};'>{decision}</h2>",
                        unsafe_allow_html=True
                    )
                    
                    analyzer.plot_comparison_chart()
            
            with st.expander("View Raw Data"):
                st.dataframe(df)
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            raise e

if __name__ == "__main__":
    main()