import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

def scatter(df):
    fig = plt.figure(figsize=(10,8))
    ax = plt.axes(prejection="3d")

    x = df["age"]
    y = df["bmi"]
    z = df["physical activity"]

    ax.scatter(x, y, z)
    st.pyplot(fig)

