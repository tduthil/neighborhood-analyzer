##########################
#import libraries
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import json
import plotly.express as px
from urllib.error import URLError
import requests
from datetime import datetime



import calculators as cal

#######Set Page Configuration#########
st.set_page_config(
    page_title="Neighborhood Analyzer",
    page_icon="🏘️",
    layout="wide",  # Use "wide" layout for a wide page
)


######PAGE TITLE#######################
st.title("     🏘️Neighborhood Analyzer :chart_with_upwards_trend:")
st.markdown("How to Use")
st.markdown("1. Navigate to your county property appraiser's site.")
st.markdown("2. Look for Advanced Search or Sales Search.")
st.markdown("    - Orange County FL: https://ocpaweb.ocpafl.org/parcelsearch")
st.markdown("3. Enter Search criteria for subject Neighborhood.")
st.markdown("4. Download csv files.")
st.markdown("5. Upload csv files.")
st.markdown("6. Follow on-page instructions.")
######PAGE TITLE#######################

# Initialize an empty DataFrame
data = pd.DataFrame()


##########functions#############



def display_unit_data(data, threshold=None):
    
    #Remove the index column
    data = data.reset_index(drop=True)

    
    # Display headers using st.header()
    #header = data.columns
    #for column in data.columns:
    #    column = st.header(column)

    # Group the data by distinct units [bed, bath, sq. ft]
    units = data.groupby(['Bedrooms', 'Bathrooms', 'squareFeet'])

    # Initialize lists to store data for each unit
    beds_list, baths_list, sqft_list, price_list, pr_sqft_list = [], [], [], [], []

    # Iterate through each unit and extract data
    for (bed, bath, sqft), unit_data in units:
        if threshold is not None:
            unit_data = unit_data[unit_data['saleAmount'] <= threshold]

        if not unit_data.empty:
            beds_list.append(bed)
            baths_list.append(bath)
            sqft_list.append(sqft)
            price_list.append(unit_data['saleAmount'].mean())  # Calculate the average price for this unit
            pr_sqft_list.append(unit_data['pricePerSqFt'].mean())  # Calculate the average price per sq. ft.

    # Create a new DataFrame for the table
    unit_df = pd.DataFrame({
        'Beds': beds_list,
        'Baths': baths_list,
        'Sq. Ft': sqft_list,
        'Sale Amount': price_list,
        '$Pr/Sq. Ft': pr_sqft_list
    })


    # Display the table
    #st.table(unit_df)
    format_table_alternative(unit_df)

def format_table_alternative(data):
    
    #Remove the index column
    data = data.reset_index(drop=True)

    # Use Pandas Styler to format the DataFrame
    styled_data = data.style.format({
        'Baths': "{:.2f}",  # Format 'Baths' to two decimal places
        'Sale Amount': "${:,.2f}",  # Format 'Sale Amount' as currency
        '$Pr/Sq. Ft': "${:,.2f}"  # Format '$Pr/Sq. Ft' as currency
    })

    

    # Display the styled DataFrame using st.write
    st.table(styled_data)

def make_decision(subject_price_per_sqft, neighborhood_avg_price_per_sqft, direct_comps_price_per_sqft, similar_comps_price_per_sqft):
    comps_price_per_sqft = [neighborhood_avg_price_per_sqft, direct_comps_price_per_sqft, similar_comps_price_per_sqft]
    num_comps = len(comps_price_per_sqft)

    if subject_price_per_sqft is not None:
        less_than_count = sum(subject_price_per_sqft < comp for comp in comps_price_per_sqft)
    else:
        less_than_count = num_comps  # If subject_price_per_sqft is None, consider it less than all

    if less_than_count == 0:
        return "PASS"
    elif less_than_count <= 1:
        return "Investigate"
    else:
        return "Buy"

##########functions#############
subject_price_per_sqft = 0.0  # Define with a default value 
direct_comps_price_per_sqft = 0.0  # Define with a default value
similar_comps_price_per_sqft = 0.0  # Define with a default value

uploaded_file = st.file_uploader("Please Upload Neighborhood Sales Data (.csv)", type=["csv"])

#original
#if uploaded_file is not None:
#    data = pd.read_csv(uploaded_file, sep='$', skiprows=1, header=0)
#    data = pd.read_csv(uploaded_file, engine='python', skiprows=1, header=0) other option
#end original
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, sep='$', skiprows=1, header=0)
    #troubleshooting upload
    ##st.write(data.head())  # Print the first few rows
    ##st.write(data.shape)
    # Specify the correct column names
    data.columns = ['Property Address', 'saleDate', 'saleAmount', 'Bedrooms', 'Bathrooms', 'squareFeet', 'year', 'seller', 'buyer', 'Parcel ID', 'totalCount', 'Link']


        
    # Extract the data into separate columns
    bedrooms = data['Bedrooms'].astype(int)
    bathrooms = data['Bathrooms'].astype(float)
    square_feet = data['squareFeet'].astype(int)
    sale_amount = data['saleAmount'].astype(float)

    
    # Prompt the user to enter the neighborhood name

    neighborhood_name = st.text_input("Enter Neighborhood Name")

    if neighborhood_name:
        cal.add_neighborhood_name(data, neighborhood_name)

    # if neighborhood_name:
    #     # Check if the 'neighborhoodName' column already exists
    #     if 'neighborhoodName' in data.columns:
    #         # If the column already exists, update the existing column with the new values
    #         data['neighborhoodName'] = neighborhood_name
    #     else:
    #         # If the column doesn't exist, insert it at the beginning
    #         data.insert(0, 'neighborhoodName', neighborhood_name)

        
    data = cal.add_price_per_square_foot(data)

    st.title("Enter Subject Property Details")

    #get subject property details
    subject_address, subject_beds, subject_baths, subject_sqft, subject_price, subject_price_per_sqft = cal.get_subject_property_details()

    

    neighborhood_avg_sale_amount = cal.calculate_neighborhood_avg_sale_amount(data, threshold=500000)
    neighborhood_avg_price_per_sq_ft = cal.calculate_neighborhood_avg_price_per_sqft(data, threshold=500000)

   
    direct_comps_price_per_sqft = cal.calculate_comp_price_per_sqft(data, beds=subject_beds, baths=subject_baths, sqft=subject_sqft, threshold=500000)
    similar_comps_price_per_sqft = cal.calculate_comp_price_per_sqft_similar_beds(data, beds=subject_beds, threshold=500000)

     # Calculate the comparison variables only if subject data is available
    #if subject_price_per_sqft:
     #   direct_comps_price_per_sqft = cal.calculate_comp_price_per_sqft(data, beds=subject_beds, baths=subject_baths, sqft=subject_sqft, threshold=500000)
     #   similar_comps_price_per_sqft = cal.calculate_comp_price_per_sqft(data, beds=subject_beds, baths=None, sqft=None, threshold=500000)

    decision = make_decision(subject_price_per_sqft, neighborhood_avg_price_per_sq_ft, direct_comps_price_per_sqft, similar_comps_price_per_sqft)



    #variable placeholder#




    st.markdown("---")
    st.header(f"{neighborhood_name}")


    one_col, two_col = st.columns(2)

    # Define the width for each column
    column_width = 0.50  # 12.5%

    with one_col:
        st.subheader(f"Avg Price: ${neighborhood_avg_sale_amount:.0f}")
        
    with two_col:
        st.subheader(f"Avg Price Per Sq. Foot: ${neighborhood_avg_price_per_sq_ft:.2f}")


    st.header(f"Neighborhood Avg. By Unit")



    # Display the table using the function
    #display_unit_data(data, threshold=500000) use with threshold if desired
    display_unit_data(data)



    ##subject home section
    st.header(f"Subject: {subject_address}")
    one_col, two_col, three_col, four_col, five_col = st.columns(5)

    # Define the width for each column
    column_width = 0.20  # 12.5%

    with one_col:
        st.subheader("Beds")
        st.subheader(f"{subject_beds}")
        
    with two_col:
        st.subheader("Baths")
        st.subheader(f"{subject_baths}")
    
    with three_col:
        st.subheader("Sq. Ft")
        st.subheader(f"{subject_sqft}")
        
    with four_col:
        st.subheader("Price")
        st.subheader(f"${subject_price}")
        
    with five_col:
        st.subheader("$Pr/Sq. Ft")
        if subject_price_per_sqft is not None:
            st.subheader(f"{subject_price_per_sqft:.2f}")
        else:
            st.error("Subject Price Per Sq. Ft is not available.")

    st.markdown("")
        
    # Define the width for each column
    column_width = 0.20  # 12.5%
    one_col, two_col, three_col, four_col, five_col = st.columns(5)
    with one_col:
        st.subheader("")
        
    with two_col:
        st.subheader("Neighboorhood Avg")
        st.markdown(cal.compare_price_per_square_foot(subject_price_per_sqft, neighborhood_avg_price_per_sq_ft), unsafe_allow_html=True)
        
    with three_col:
        st.subheader("Direct Comps")
        st.markdown(cal.compare_price_per_square_foot(subject_price_per_sqft, direct_comps_price_per_sqft), unsafe_allow_html=True)
    
    with four_col:
        st.subheader("Similar Comps")
        st.markdown(cal.compare_price_per_square_foot(subject_price_per_sqft, similar_comps_price_per_sqft), unsafe_allow_html=True)
        
    with five_col:
        st.subheader("Decision")
        st.subheader(f"{decision}")


    #troubleshooting comp avg function
    ##st.write(direct_comps_price_per_sqft, similar_comps_price_per_sqft)

    # Create a checkbox
    show_data = st.checkbox("Show Data Table")

    # Check if the checkbox is selected
    if show_data:
        st.table(data)  # Display the data table when the checkbox is selected

    

    st.markdown("---")
