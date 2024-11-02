# Color schemes and styling constants
BRAND_COLOR = "#782F40"

# Header mapping configurations
HEADER_MAPPINGS = {
    'price': ['price', 'saleamount', 'sale amount', 'sale price', 'amount', 'value', 'Price', 'Sale Amount'],
    'address': ['address', 'property address', 'location', 'street address', 'Property Address'],
    'beds': ['beds', 'bedrooms', 'br', 'number of bedrooms', 'Bed', 'Bedrooms'],
    'baths': ['baths', 'bathrooms', 'ba', 'number of bathrooms', 'Bath', 'Bathrooms'],
    'sqft': ['sqft', 'square feet', 'squarefeet', 'living area', 'size', 'SqFt', 'Living'],
    'date': ['date', 'saledate', 'sale date', 'transaction date', 'Date Sold', 'Date']
}

# Required fields for analysis
REQUIRED_FIELDS = ['price']  # Made only price required since some files might not have sqft

# Custom CSS
CUSTOM_CSS = """
    <style>
    .stApp a, .stApp a:hover {
        color: #782F40;
    }
    .stButton>button {
        background-color: #782F40;
        color: white;
    }
    .stProgress .st-bo {
        background-color: #782F40;
    }
    div[data-testid="stMetricValue"] {
        color: #782F40;
    }
    </style>
"""