import streamlit as st
import pandas as pd

# Load the data
df = pd.read_csv("inputs/alzheimers_disease_data.csv")


def dashboard_body():
    """
    Contents of the Alzheimer's Disease dashboard page
    """
    st.header("Alzheimer's Disease Dashboard")
    
    # Display basic information about the dataset
    st.subheader("Dataset Overview")
    st.write(f"**Dataset shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Show first few rows
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    # Basic statistics
    st.subheader("Basic Statistics")
    st.dataframe(df.describe())
    
    st.info("This is a basic dashboard for Alzheimer's Disease data analysis. Add more visualizations and analysis as needed.")
