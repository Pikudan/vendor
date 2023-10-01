import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re
import os

def convert_price_to_digits(price, to_int=False):
    if isinstance(price, str):
        # Use regex to remove letters, punctuation, and spaces
        cleaned_price = re.sub(r'[^\d]+', '', price)
        if to_int:
            try:
                cleaned_price = int(cleaned_price)
            except ValueError:
                pass
        return cleaned_price
    return price
    
def load_csv():
    path_folder = os.path.dirname(__file__)
    filename = 'full_data.csv'
    #path_output_file = os.path.join(path_folder, filename)
    data = pd.read_csv(filename, delimiter='@')
    data = data.drop('full_desc', axis=1)
    data['price'] = data['price'].apply(lambda x: convert_price_to_digits(x, to_int=True))
    return data



def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f'{n}{suffix}'

# Apply the conversion function to the 'price' column and convert to integers if possible


# Define a function for Page 1
def page1(data):
    #data = load_csv()
    # Create a list of unique vendors
    data['price'] = data['price'].apply(lambda x: convert_price_to_digits(x, to_int=True))
    unique_vendors = data['vendor'].unique()

    # Streamlit app
    st.title('Vendor Analytics')

    # Autocomplete search field for selecting a vendor
    selected_vendor = st.selectbox('Search for Vendor (Autocomplete)', unique_vendors, format_func=lambda x: x)

    # Filter data for the selected vendor
    filtered_data = data[data['vendor'] == selected_vendor]

    # Number of categories for the selected vendor
    num_categories = len(filtered_data['category'].unique())

    # Number of unique products for the selected vendor
    num_unique_products = len(filtered_data['name'].unique())

    # Sort vendors by the number of categories
    sorted_vendors = data.groupby('vendor')['category'].nunique().sort_values(ascending=False).index.tolist()

    # Find the position of the current vendor
    vendor_position = sorted_vendors.index(selected_vendor) + 1

    # Display number of categories and unique products along with the vendor's position
    st.subheader(f'Analytics for {selected_vendor}')
    st.write(f'Number of Categories for {selected_vendor}: {num_categories}')
    st.write(f'Number of Unique Products for {selected_vendor}: {num_unique_products}')
    st.write(f'{selected_vendor} is the {ordinal(vendor_position)} biggest vendor in terms of categories.')


    # Region Distribution Plot (Bar chart)
    st.subheader(f'Region Distribution for {selected_vendor}')
    region_counts = filtered_data['region'].value_counts().reset_index()
    region_counts.columns = ['Region', 'Number of Products']

    # Create a bar chart (using Plotly)
    fig_region = px.bar(region_counts, x='Region', y='Number of Products',
                        labels={'Region': 'Region Name', 'Number of Products': 'Count'},
                        title='Region Distribution')
    st.plotly_chart(fig_region)

    # Remove outliers (>99th quantile) for Price vs Region and Price vs Categories plots
    filtered_data_no_outliers = filtered_data.copy()
    quantile_99 = filtered_data['price'].quantile(0.95)
    filtered_data_no_outliers = filtered_data_no_outliers[filtered_data_no_outliers['price'] <= quantile_99]

    # Price Distribution Plot (Histogram with sorted bins, using Plotly)
    st.subheader(f'Price Distribution for {selected_vendor}')
    sorted_bins = np.sort(filtered_data_no_outliers['price'].unique())
    fig_price = px.histogram(filtered_data_no_outliers, x='price', nbins=len(sorted_bins), 
                            title='Price Distribution', 
                            category_orders={'price': sorted_bins})
    st.plotly_chart(fig_price)

    # Product Category Distribution (Bar chart)
    st.subheader(f'Product Category Distribution for {selected_vendor}')
    category_counts = filtered_data_no_outliers['category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Number of Products']

    # Truncate x-axis labels to the first two words
    category_counts['Short Category'] = category_counts['Category'].str.split().str[:3].str.join(' ')

    # Create a bar chart (using Plotly) with custom hover text
    fig_category = px.bar(category_counts, x='Short Category', y='Number of Products',
                        labels={'Short Category': 'Category Name', 'Number of Products': 'Count'},
                        title='Product Category Distribution')
    fig_category.update_traces(customdata=category_counts['Category'], hovertemplate='%{customdata}<br>Count: %{y}')
    st.plotly_chart(fig_category)


    # Truncate x-axis labels to the first two words
    filtered_data_no_outliers['Short Category'] = filtered_data_no_outliers['category'].str.split().str[:3].str.join(' ')

    # Price vs. Category (Box plot)
    st.subheader(f'Price vs. Category for {selected_vendor}')
    fig_price_category = px.box(filtered_data_no_outliers, x='Short Category', y='price', 
                                labels={'Short Category': 'Category', 'price': 'Price'},
                                title='Price vs. Category')
    fig_price_category.update_xaxes(title_text='Category')

    # Update hovertemplate to show full category names
    fig_price_category.update_traces(customdata=filtered_data_no_outliers['category'],
                                    hovertemplate='%{x}<br>Category: %{customdata}<br>Price: %{y}')

    st.plotly_chart(fig_price_category)



    # Price vs. Region (Box plot)
    st.subheader(f'Price vs. Region for {selected_vendor}')
    fig_price_region = px.box(filtered_data_no_outliers, x='region', y='price', 
                            labels={'region': 'Region', 'price': 'Price'},
                            title='Price vs. Region')
    st.plotly_chart(fig_price_region)

# Define a function for Page 2
def page2(data):
    #data = load_csv()
    data['price'] = data['price'].apply(lambda x: convert_price_to_digits(x, to_int=True))
    # Create a list of unique categories
    unique_categories = data['category'].unique()

    # Streamlit app
    st.title('Category Analytics')

    # Autocomplete search field for selecting a category
    selected_category = st.selectbox('Search for Category (Autocomplete)', unique_categories, format_func=lambda x: x)

    # Filter data for the selected category
    filtered_data = data[data['category'] == selected_category]

    # Number of vendors for the selected category
    num_vendors = len(filtered_data['vendor'].unique())

    # Number of unique products for the selected category
    num_unique_products = len(filtered_data['name'].unique())

    # Display number of vendors and unique products for the selected category
    st.subheader(f'Analytics for {selected_category}')
    st.write(f'Number of Vendors for {selected_category}: {num_vendors}')
    st.write(f'Number of Unique Products for {selected_category}: {num_unique_products}')
   
    # Bar chart showing the distribution of vendors in the category
    st.subheader(f'Distribution of Vendors in {selected_category}')
    vendor_distribution = filtered_data['vendor'].value_counts()
    st.bar_chart(vendor_distribution)

    # Box plot of prices for products in the category
    st.subheader(f'Price Distribution for {selected_category}')
    fig_price = px.box(filtered_data, x='vendor', y='price', title=f'Price Distribution for {selected_category}')
    st.plotly_chart(fig_price)

    # Scatter plot of prices vs. regions for products in the category
    st.subheader(f'Price vs. Region for {selected_category}')
    fig_price_region = px.scatter(filtered_data, x='region', y='price', title=f'Price vs. Region for {selected_category}')
    st.plotly_chart(fig_price_region)

    # Price distribution histogram for products in the category
    st.subheader(f'Price Distribution (Histogram) for {selected_category}')
    fig_price_distribution = px.histogram(filtered_data, x='price', title=f'Price Distribution for {selected_category}')
    st.plotly_chart(fig_price_distribution)

