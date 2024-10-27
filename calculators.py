#calculator functions
##########################
#import libraries
import streamlit as st

def calculate_neighborhood_avg_sale_amount(data, threshold=None):
    # Filter the data to exclude sale amounts greater than the threshold
    filtered_data = data[data['saleAmount'] <= threshold]

    # Group the filtered data by the 'neighborhood_name' and calculate the average sale amount
    neighborhood_avg = filtered_data['saleAmount'].mean()
    return neighborhood_avg


def calculate_neighborhood_avg_price_per_sqft(data, threshold=None):
    # If a threshold is provided, filter the data to exclude sale amounts greater than the threshold
    if threshold is not None:
        data = data[data['saleAmount'] <= threshold]

    # Calculate the price per square foot
    neighborhood_avg_price_per_sq_ft = data['pricePerSqFt'].mean()

    # Group the data by distinct unit combinations and calculate the average price per square foot
    #unit_avg = data.groupby(['Bedrooms', 'Bathrooms', 'squareFeet'])['price_per_sqft'].mean()
    return neighborhood_avg_price_per_sq_ft


def calculate_avg_price_per_sqft_unit(data, threshold=None):
    # If a threshold is provided, filter the data to exclude sale amounts greater than the threshold
    if threshold is not None:
        data = data[data['saleAmount'] <= threshold]

    # Calculate the price per square foot for each unit
    data['price_per_sqft'] = data['saleAmount'] / data['squareFeet']

    # Group the data by distinct unit combinations and calculate the average price per square foot
    unit_avg = data.groupby(['Bedrooms', 'Bathrooms', 'squareFeet'])['price_per_sqft'].mean()
    return unit_avg


def calculate_comp_price_per_sqft_similar_beds(data, beds, threshold=None):
    # Filter the data for units with the specified number of bedrooms
    comps_data = data[data['Bedrooms'] == beds]

    if threshold is not None:
        comps_data = comps_data[comps_data['saleAmount'] <= threshold]

    # Calculate the average price per square foot for the filtered units
    avg_price_per_sqft_similar_beds = comps_data['pricePerSqFt'].mean()
    return avg_price_per_sqft_similar_beds

#def add_neighborhood_name(data):
    # Prompt the user to enter the neighborhood name
    neighborhood_name = data["neighborhoodName"]

    if neighborhood_name:
        # Check if the neighborhoodName column already exists
        if 'neighborhoodName' in data.columns:
            # If the column already exists, update the existing column with the new values
            data['neighborhoodName'] = neighborhood_name
        else:
            # If the column doesn't exist, insert it at the beginning
            data.insert(0, 'neighborhoodName', neighborhood_name)

    return data

def add_neighborhood_name(data, neighborhood_name):
    # Check if the 'neighborhoodName' column already exists
    if 'neighborhoodName' in data.columns:
        # If the column already exists, update the existing column with the new values
        data['neighborhoodName'] = neighborhood_name
    else:
        # If the column doesn't exist, insert it at the beginning
        data.insert(0, 'neighborhoodName', neighborhood_name)

    return data

def add_price_per_square_foot(data):
    try:
        # Attempt to insert the neighborhood name column at the beginning
        data.insert(7, 'pricePerSqFt', data['saleAmount'] / data['squareFeet'])
    except ValueError:
        # If the column already exists, update the existing column with the new values
        data['pricePerSqFt'] = data['saleAmount'] / data['squareFeet']

    return data


def compare_price_per_square_foot(ppsf1, ppsf2):
    green_icon = '<span style="color:green; font-size: 24px;">▼</span>'
    red_icon = '<span style="color:red; font-size: 24px;">▲</span>'

    if ppsf1 is not None and ppsf2 is not None:
        if ppsf1 < ppsf2:
            # Do something if ppsf1 is lower
             return green_icon
        elif ppsf1 > ppsf2:
            # Do something if ppsf2 is lower
            return red_icon
        elif ppsf1 == ppsf2:
            return '=='
    else:
        # Handle the case where one or both values are None
        return "Insufficient data for comparison"  # Example handling
    

def calculate_comp_price_per_sqft(data, beds, baths, sqft, threshold=None):
    # Filter the data for the specific unit with matching bedrooms, bathrooms, and square footage
    unit_data = data[(data['Bedrooms'] == beds) & (data['Bathrooms'] == baths) & (data['squareFeet'] == sqft)]

    if threshold is not None:
        unit_data = unit_data[unit_data['saleAmount'] <= threshold]

    # Calculate the average price per square foot for the filtered unit
    avg_price_per_sqft = unit_data['pricePerSqFt'].mean()

    return avg_price_per_sqft


def get_subject_property_details():
    subject_address = st.text_input("Enter Property Address")
    subject_beds = st.text_input("Enter Number of Beds")
    if subject_beds:
        subject_beds = int(subject_beds)
    subject_baths = st.text_input("Enter Number of Baths")
    if subject_baths:
        subject_baths = float(subject_baths)

    # Validate and convert subject_sqft
    subject_sqft = st.text_input("Enter Square Feet")
    if subject_sqft:
        subject_sqft = int(subject_sqft)
    else:
        st.error("Square Feet cannot be empty.")

    # Validate and convert subject_price
    subject_price = st.text_input("Enter Asking Price")
    if subject_price:
        subject_price = float(subject_price)
    else:
        st.error("Asking Price cannot be empty.")

    # Calculate subject_price_per_sqft only if subject_sqft and subject_price are valid
    subject_price_per_sqft = None
    if subject_sqft and subject_price:
        subject_price_per_sqft = subject_price / subject_sqft
    else:
        st.error("Please enter valid Square Feet and Asking Price.")

    return subject_address, subject_beds, subject_baths, subject_sqft, subject_price, subject_price_per_sqft
