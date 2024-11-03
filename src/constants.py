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
REQUIRED_FIELDS = ['price']

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
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #782F40;
        padding: 10px 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: white;
        border-radius: 4px;
        color: #782F40;
        font-weight: 600;
        border-left: 1px solid #ddd;
    }

    .stTabs [data-baseweb="tab"]:first-child {
        border-left: none;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #782F40;
        color: white;
    }
    </style>
"""