import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("inputs/alzheimers_disease_data.csv")

def scatter(df):
    fig = plt.figure(figsize=(10,8))
    ax = plt.axes(projection="3d")

    x = df["Age"]
    y = df["BMI"]
    z = df["PhysicalActivity"]

    ax.scatter(x, y, z)
    st.pyplot(fig)

def stacked(df):

df.groupby[("Smoking", "CardiovascularDisease")].size().unstack().plot(kind="bar", stacked=True)
    st.pyplot(plt)

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



