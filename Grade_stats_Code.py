# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 19:41:40 2023

@author: Yehuda Yungstein
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

def main():
    st.title("Grades by Category")

    # Load data into a Pandas dataframe
    df = pd.read_excel(r"C:\Users\User\Downloads\Grades_Stats.xlsx")
    
    #drop nan values:
    df = df.dropna()

    # Show the raw data in a table
    st.write("Raw data:")
    st.dataframe(df[['Course_Name', 'Grade', 'Points', 'Number_Course', 'Degree', 'Year']])

    # Let the user select one or more categories to display
    category_cols = df.columns[6:]  # Replace with the actual names of your category columns
    selected_categories = st.multiselect(label = "Select categories to display",
                                         options=category_cols.tolist(),
                                         default=category_cols.tolist())

    if selected_categories:
        # Convert the data to a long format
        df_long = df.melt(id_vars=['Course_Name', 'Grade', 'Points', 'Number_Course', 'Degree', 'Year'], value_vars=category_cols, var_name='Category', value_name='Category_Value')
        df_long = df_long[df_long['Category_Value'] != 0]  # Filter out categories with value of 0

        # Filter the data to only include the selected categories
        filtered_df = df_long[df_long['Category'].isin(selected_categories)]

        st.write("Filtered data:")
        st.dataframe(filtered_df[['Course_Name', 'Grade', 'Points', 'Number_Course', 'Degree', 'Year', 'Category']])

        # Show an interactive histogram of the grades in each category
        st.write("Histograms:")
        fig = px.histogram(filtered_df, x="Grade", color="Category", nbins=30,
                           title="Distribution of grades by category",
                           marginal="rug", hover_data=['Course_Name', 'Grade', 'Degree','Category',])
        st.plotly_chart(fig)