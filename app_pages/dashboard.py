import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import matplotlib as mb

df = pd.read_csv("inputs/alzheimers_disease_data.csv")

def scatter(df):
    try:
        # Create matplotlib figure (non-interactive for Streamlit)
        fig = plt.figure(figsize=(14, 12))
        ax = plt.axes(projection="3d")

        x = df["Age"]
        y = df["BMI"]
        z = df["PhysicalActivity"]

        # Create scatter plot with color mapping for better identification
        scatter_plot = ax.scatter(x, y, z, alpha=0.6, c=range(len(df)), cmap="viridis")
        ax.set_xlabel("Age")
        ax.set_ylabel("BMI")
        ax.set_zlabel("Physical Activity")
        ax.set_title("3D Scatter Plot: Age, BMI, and Physical Activity")
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating 3D scatter plot: {str(e)}")
        st.write("Available columns:", df.columns.tolist())
        return None

def histogram(df):
    try:
        # Create matplotlib figure for histogram
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle("Distribution Analysis - Matplotlib", fontsize=16)
        
        # Age distribution
        axes[0,0].hist(df["Age"], bins=20, alpha=0.7, color="skyblue", edgecolor="black")
        axes[0,0].set_title("Age Distribution")
        axes[0,0].set_xlabel("Age")
        axes[0,0].set_ylabel("Frequency")
        
        # BMI distribution
        axes[0,1].hist(df["BMI"], bins=20, alpha=0.7, color="lightgreen", edgecolor="black")
        axes[0,1].set_title("BMI Distribution")
        axes[0,1].set_xlabel("BMI")
        axes[0,1].set_ylabel("Frequency")
        
        # Physical Activity distribution
        axes[1,0].hist(df["PhysicalActivity"], bins=20, alpha=0.7, color="salmon", edgecolor="black")
        axes[1,0].set_title("Physical Activity Distribution")
        axes[1,0].set_xlabel("Physical Activity")
        axes[1,0].set_ylabel("Frequency")
        
        # Gender distribution (if available)
        if "Gender" in df.columns:
            gender_counts = df["Gender"].value_counts()
            axes[1,1].bar(gender_counts.index, gender_counts.values, alpha=0.7, color="orange")
            axes[1,1].set_title("Gender Distribution")
            axes[1,1].set_xlabel("Gender")
            axes[1,1].set_ylabel("Count")
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating matplotlib histogram: {str(e)}")
        st.write("Available columns:", df.columns.tolist())
        return None


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

def correlation_heatmap(df):
    try:
        # Create seaborn figure for correlation heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Select only numeric columns for correlation
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
        correlation_matrix = df[numeric_cols].corr()
        
        # Create heatmap
        sns.heatmap(correlation_matrix, 
                   annot=True, 
                   cmap="coolwarm", 
                   center=0,
                   square=True,
                   fmt=".2f",
                   cbar_kws={"shrink": .8},
                   ax=ax)
        
        ax.set_title("Correlation Matrix - Seaborn Heatmap", fontsize=16, pad=20)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating seaborn heatmap: {str(e)}")
        st.write("Available columns:", df.columns.tolist())
        return None

def parallel(df):
    try:
        fig = px.parallel_coordinates(df, color="Smoking", dimensions = ["Age", "Gender", "BMI", "Ethnicity", "CardiovascularDisease", "PhysicalActivity"])
        st.plotly_chart(fig)
        return fig
    except Exception as e:
        st.error(f"Error creating parallel coordinates chart: {str(e)}")
        st.write("Available columns:", df.columns.tolist())
        return None

def box_plots(df):
    try:
        # Create plotly subplots for box plots
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Age by Smoking Status", "BMI by Gender", 
                          "Physical Activity by Cardiovascular Disease", "Age Distribution"),
            specs=[[{"type": "box"}, {"type": "box"}],
                   [{"type": "box"}, {"type": "histogram"}]]
        )
        
        # Box plot 1: Age by Smoking Status
        if "Smoking" in df.columns:
            for smoking_status in df["Smoking"].unique():
                subset = df[df["Smoking"] == smoking_status]
                fig.add_trace(
                    go.Box(y=subset["Age"], name=f"Smoking: {smoking_status}", 
                          showlegend=False),
                    row=1, col=1
                )
        
        # Box plot 2: BMI by Gender
        if "Gender" in df.columns:
            for gender in df["Gender"].unique():
                subset = df[df["Gender"] == gender]
                fig.add_trace(
                    go.Box(y=subset["BMI"], name=f"Gender: {gender}",
                          showlegend=False),
                    row=1, col=2
                )
        
        # Box plot 3: Physical Activity by Cardiovascular Disease
        if "CardiovascularDisease" in df.columns:
            for cvd_status in df["CardiovascularDisease"].unique():
                subset = df[df["CardiovascularDisease"] == cvd_status]
                fig.add_trace(
                    go.Box(y=subset["PhysicalActivity"], name=f"CVD: {cvd_status}",
                          showlegend=False),
                    row=2, col=1
                )
        
        # Histogram: Age Distribution
        fig.add_trace(
            go.Histogram(x=df["Age"], name="Age Distribution", showlegend=False,
                        marker_color="lightblue"),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Healthcare Data Analysis - Plotly Box Plots & Histogram",
            title_x=0.5,
            height=600,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating plotly box plots: {str(e)}")
        st.write("Available columns:", df.columns.tolist())
        return None

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
    
    st.write("Distribution Analysis - Matplotlib")
    histogram(df)
    
    stacked(df)
    
    st.write("Correlation Matrix - Seaborn")
    correlation_heatmap(df)
    
    parallel(df)
    
    st.write("Box Plots and Histogram - Plotly")
    box_plots(df) 



