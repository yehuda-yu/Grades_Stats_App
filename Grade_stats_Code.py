# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 19:41:40 2023

@author: Yehuda Yungstein
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def main():
  
    st.title("Yehuda Yungstein Grades Visualization App")
    st.write("The application showcases the grade distribution of my research bachelor's and master's degrees in The Hebrew University of Jerusalem, Faculty of Agriculture, Food and Environment, across multiple courses. Users can explore the grade distribution according to different categories and time periods.")
    st.markdown("""
                ---
                """)

    # Load data into a Pandas dataframe
    df = pd.read_excel("Grades_Stats.xlsx")
    
    # Convert 'Grade' and 'Points' columns to numeric
    df['Grade'] = pd.to_numeric(df['Grade'], errors='coerce')
    df['Points'] = pd.to_numeric(df['Points'], errors='coerce')
    
    #drop nan values:
    df = df.dropna()
    
    st.markdown("#### **B.S. Soil & Water Science**")
    st.write("**Mean grade**: 88.6")
    st.write("	:sparkles: Dean's Award for Academic Excellence 2022")
    st.markdown("#### M.Sc. Environmental Science (Soil & water)")
    st.write("Data Science specialization")    
    st.write("**Mean grade** (temp): 94.3")
    st.write("	:sparkles: Dean's Award for Academic Excellence 2023")
    
    # Calculate weighted grades by category
    category_cols = df.columns[6:] # Replace with the actual names of your category columns
    for category in category_cols:
        # Calculate total points earned and total points available for this category
        total_points_earned = (df['Grade']*df['Points']*df[category]).sum()
        total_points_available = (df['Points']*df[category]).sum()
        
        # Calculate weighted average grade for this category
        weighted_grade = total_points_earned / total_points_available
        
        # Merge weighted grade for this category back into original dataframe
        df.loc[df[category] == 1, 'Weighted_Grade'] = weighted_grade
        
        
    
    # Show the raw data in a table
    st.subheader("All Grades Data:")
    st.dataframe(df[['Course_Name', 'Grade', 'Points', 'Number_Course', 'Degree', 'Year', 'Weighted_Grade']])
    
    # Let the user select one or more categories to display
    selected_categories = st.multiselect(label = "Select categories to display",
                                         options=category_cols.tolist(),
                                         default=category_cols.tolist())
    
    if selected_categories:
        # Convert the data to a long format
        df_long = df.melt(id_vars=['Course_Name', 'Grade', 'Points', 'Number_Course', 'Degree', 'Year', 'Weighted_Grade'], value_vars=category_cols, var_name='Category', value_name='Category_Value')
        df_long = df_long[df_long['Category_Value'] != 0]  # Filter out categories with value of 0
    
        # Filter the data to only include the selected categories
        filtered_df = df_long[df_long['Category'].isin(selected_categories)]
    
        st.write("Filtered data:")
        st.dataframe(filtered_df[['Course_Name', 'Grade', 'Points', 'Number_Course', 'Degree', 'Year', 'Category', 'Weighted_Grade']])
    
       
        # Create the Box plot
        st.subheader("Comparison of Grades by Category:")
        fig = px.box(filtered_df, x='Category', y='Weighted_Grade', color='Category')
        
        # Add title and labels
        fig.update_layout(title=' ', xaxis_title='Category', yaxis_title='Grade')
        
        # Add text above each box
        for i, category in enumerate(selected_categories):
            weighted_grade_avg = filtered_df.loc[filtered_df['Category']==category, 'Weighted_Grade'].mean()
            fig.add_annotation(x=i, y=weighted_grade_avg, text=f"{weighted_grade_avg:.1f}", showarrow=False)
            
        # Show the Box plot
        st.plotly_chart(fig)
        
        # Show an interactive histogram of the grades in each category
        st.subheader("Distribution of grades by category:")
        fig = px.histogram(filtered_df, x="Weighted_Grade", color="Category", nbins=30,
                           title=" ",
                           marginal="rug", hover_data=['Course_Name', 'Weighted_Grade', 'Degree', 'Category'])
        st.plotly_chart(fig)
        
        
        # Group by year and calculate weighted grade mean
        df_year = df.groupby("Year", as_index=False)["Weighted_Grade"].mean()
        
        # Define color map for each degree
        color_map = {
            "B.S.": "#07f49e",
            "M.Sc.": "#42047e",
        }

        st.subheader("Comparison of Grades by Year:")
        # Create box plot with Plotly Express
        fig = px.box(df, x="Year", y="Grade", color='Degree',color_discrete_map=color_map)
        
        # Update layout to customize appearance
        fig.update_layout(
            title="",
            xaxis_title="Year",
            yaxis_title="Grade",
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        
        # Display figure using Streamlit
        st.plotly_chart(fig)
        
        
        
if __name__ == "__main__":
    main()
