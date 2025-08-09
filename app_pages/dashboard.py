import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = pd.read_csv("inputs/alzheimers_disease_data.csv")

def scatter(df):
    try:
        fig = plt.figure(figsize=(10, 8))
        ax = plt.axes(projection="3d")

        x = df["Age"]
        y = df["BMI"]
        z = df["PhysicalActivity"]

        ax.scatter(x, y, z, alpha=0.6)
        ax.set_xlabel("Age")
        ax.set_ylabel("BMI")
        ax.set_zlabel("Physical Activity")
        ax.set_title("3D Scatter Plot: Age, BMI, and Physical Activity")
            
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error creating 3D scatter plot: {str(e)}")
        st.write("Available columns:", df.columns.tolist())

def stacked(df):
    try:
        # Create a new figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create a copy of the dataframe and replace 0 with "yes" for the relevant columns
        df_modified = df.copy()
        
        # Replace 0 with "no" and 1 with "yes"
        if "Smoking" in df_modified.columns:
            df_modified["Smoking"] = df_modified["Smoking"].replace({0: "No", 1: "Yes"})
        if "CardiovascularDisease" in df_modified.columns:
            df_modified["CardiovascularDisease"] = df_modified["CardiovascularDisease"].replace({0: "No", 1: "Yes"})
        
        # Create the stacked bar chart
        df_modified.groupby(["Smoking", "CardiovascularDisease"]).size().unstack().plot(
            kind="bar", 
            stacked=True, 
            ax=ax
        )
        
        # Add labels and title
        ax.set_title("Smoking vs Cardiovascular Disease")
        ax.set_xlabel("Smoking Status")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error creating stacked bar chart: {str(e)}")
        st.write("Available columns:", df.columns.tolist())


def dashboard_body():
    st.title("Dashboard")
    st.header("Alzheimer's Disease Dashboard")
    st.subheader("Dataset Overview")
    st.write("This dashboard provides insights into Alzheimer's disease.")
    st.write(f"**Dataset shape:** {df.shape[0]} rows × {df.shape[1]} columns")

    
    # Show first few rows
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    # Basic statistics
    st.subheader("Basic Statistics")
    st.dataframe(df.describe())
    
    st.info("This is a basic dashboard for Alzheimer's Disease data analysis. Add more visualizations and analysis as needed.")


    st.write("Scatter plot of age, BMI and physical activity")
    scatter(df) 
    stacked(df)  



