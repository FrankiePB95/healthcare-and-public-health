import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib as mb
import numpy as np
import scipy.stats as stats

# Load and process data
df = pd.read_csv("inputs/alzheimers_disease_data.csv")

# Data preprocessing for risk assessment
def preprocess_data_for_risk_assessment(df):
    """
    Preprocess data for risk assessment dashboard
    """
    # Take a sample for demonstration
    df_sample = df.sample(frac=0.25, random_state=10)
    
    # Create processed dataframe similar to notebook
    processed_df = df_sample.copy()
    
    # Replace categorical values
    if "Gender" in processed_df.columns:
        processed_df["Gender"] = processed_df["Gender"].replace({0: "Male", 1: "Female"})
    
    # Create risk assessment columns
    processed_df = processed_df.rename(columns={
        "Age": "Patient_Age",
        "AlcoholConsumption": "Alcohol_Consumption",
        "PhysicalActivity": "Physical_Activity",
        "CholesterolTotal": "Cholesterol_Total",
        "FunctionalAssessment": "Functional_Assessment",
        "ADL": "Activities_Of_Daily_Living"
    })
    
    return processed_df

# Risk Assessment Functions
def calculate_risk_score(row):
    """
    Calculate comprehensive risk score based on multiple health factors
    Higher scores indicate higher risk for cognitive decline/dementia
    """
    risk_score = 0
    
    # Age risk (40% weight) - older patients at higher risk
    if row['Patient_Age'] >= 80:
        risk_score += 4
    elif row['Patient_Age'] >= 75:
        risk_score += 3
    elif row['Patient_Age'] >= 70:
        risk_score += 2
    else:
        risk_score += 1
        
    # MMSE risk (30% weight) - lower scores indicate cognitive impairment
    if row['MMSE'] < 10:
        risk_score += 3
    elif row['MMSE'] < 18:
        risk_score += 2.5
    elif row['MMSE'] < 24:
        risk_score += 1.5
    else:
        risk_score += 0.5
        
    # BMI risk (15% weight) - both high and low BMI are risk factors
    if row['BMI'] > 35 or row['BMI'] < 18.5:
        risk_score += 1.5
    elif row['BMI'] > 30 or row['BMI'] < 20:
        risk_score += 1
    else:
        risk_score += 0.5
        
    # Functional Assessment (10% weight) - lower scores indicate dependency
    if row['Functional_Assessment'] <= 2:
        risk_score += 1
    elif row['Functional_Assessment'] <= 4:
        risk_score += 0.7
    else:
        risk_score += 0.3
        
    # Cholesterol risk (5% weight) - very high or very low can be concerning
    if row['Cholesterol_Total'] > 280 or row['Cholesterol_Total'] < 160:
        risk_score += 0.5
    elif row['Cholesterol_Total'] > 240:
        risk_score += 0.3
        
    return round(risk_score, 2)

def categorize_risk(score):
    if score >= 7:
        return 'High Risk'
    elif score >= 5:
        return 'Medium Risk'
    else:
        return 'Low Risk'

# Process data for risk assessment
processed_df = preprocess_data_for_risk_assessment(df)

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

def risk_assessment_dashboard():
    """
    Interactive Risk Assessment & Early Detection Dashboard
    """
    st.header("🏥 Risk Assessment & Early Detection Dashboard")
    
    # Business need explanation
    with st.expander("📋 Business Need & Dashboard Components"):
        st.markdown("""
        ### **Business Need**: 
        Healthcare providers need to identify high-risk patients for early intervention to:
        - Prevent disease progression
        - Optimize resource allocation
        - Improve patient outcomes
        - Reduce healthcare costs

        ### **Dashboard Components**:
        1. **Risk Scoring Algorithm** - Multi-factor risk assessment
        2. **Patient Segmentation** - High, Medium, Low risk categories
        3. **Key Risk Indicators** - BMI, MMSE, Age, Cholesterol patterns
        4. **Early Warning System** - Threshold-based alerts
        5. **Intervention Recommendations** - Actionable insights for clinicians
        """)
    
    # Calculate risk scores
    if 'Risk_Score' not in processed_df.columns:
        processed_df['Risk_Score'] = processed_df.apply(calculate_risk_score, axis=1)
        processed_df['Risk_Category'] = processed_df['Risk_Score'].apply(categorize_risk)
        processed_df['Early_Detection_Flag'] = (
            (processed_df['MMSE'] < 18) | 
            (processed_df['Patient_Age'] > 75) | 
            (processed_df['BMI'] > 35) |
            (processed_df['Functional_Assessment'] <= 3)
        )
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_patients = len(processed_df)
        st.metric("Total Patients", total_patients)
    
    with col2:
        high_risk_count = len(processed_df[processed_df['Risk_Category'] == 'High Risk'])
        st.metric("High Risk Patients", high_risk_count, delta=f"{(high_risk_count/total_patients*100):.1f}%")
    
    with col3:
        early_detection_count = processed_df['Early_Detection_Flag'].sum()
        st.metric("Early Detection Flags", early_detection_count, delta=f"{(early_detection_count/total_patients*100):.1f}%")
    
    with col4:
        avg_risk_score = processed_df['Risk_Score'].mean()
        st.metric("Average Risk Score", f"{avg_risk_score:.2f}")
    
    # Risk distribution
    st.subheader("📊 Risk Category Distribution")
    risk_distribution = processed_df['Risk_Category'].value_counts()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pie chart for risk distribution
        fig_pie = px.pie(values=risk_distribution.values, names=risk_distribution.index,
                        color_discrete_map={'High Risk': '#e74c3c', 'Medium Risk': '#f39c12', 'Low Risk': '#2ecc71'},
                        title="Patient Risk Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart for risk distribution
        fig_bar = px.bar(x=risk_distribution.index, y=risk_distribution.values,
                        color=risk_distribution.index,
                        color_discrete_map={'High Risk': '#e74c3c', 'Medium Risk': '#f39c12', 'Low Risk': '#2ecc71'},
                        title="Risk Category Counts")
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Interactive 3D Risk Assessment
    st.subheader("🎯 Interactive 3D Risk Assessment Matrix")
    
    fig_3d = px.scatter_3d(processed_df, 
                          x='Patient_Age', y='MMSE', z='BMI',
                          color='Risk_Category',
                          size='Risk_Score',
                          hover_data=['Cholesterol_Total', 'Functional_Assessment'],
                          color_discrete_map={'High Risk': '#e74c3c', 'Medium Risk': '#f39c12', 'Low Risk': '#2ecc71'},
                          title="3D Risk Assessment: Age vs MMSE vs BMI")
    
    fig_3d.update_layout(scene=dict(
        xaxis_title='Patient Age',
        yaxis_title='MMSE Score (Cognitive Function)',
        zaxis_title='BMI'
    ))
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Risk factor correlation heatmap
    st.subheader("🔥 Risk Factor Correlation Analysis")
    
    risk_variables = ['Patient_Age', 'MMSE', 'BMI', 'Cholesterol_Total', 
                     'Functional_Assessment', 'Physical_Activity', 
                     'Alcohol_Consumption', 'Risk_Score']
    
    # Filter variables that exist in the dataframe
    available_vars = [var for var in risk_variables if var in processed_df.columns]
    correlation_matrix = processed_df[available_vars].corr()
    
    fig_heatmap = px.imshow(correlation_matrix, 
                           text_auto=True, 
                           color_continuous_scale='RdBu_r',
                           title="Risk Factor Correlation Heatmap")
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Clinical insights by risk category
    st.subheader("🏥 Clinical Insights by Risk Category")
    
    for risk_cat in ['High Risk', 'Medium Risk', 'Low Risk']:
        subset = processed_df[processed_df['Risk_Category'] == risk_cat]
        if len(subset) > 0:
            with st.expander(f"{risk_cat} Patients (n={len(subset)})"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Average MMSE", f"{subset['MMSE'].mean():.1f}")
                
                with col2:
                    st.metric("Average Age", f"{subset['Patient_Age'].mean():.1f}")
                
                with col3:
                    st.metric("Average BMI", f"{subset['BMI'].mean():.1f}")
                
                with col4:
                    st.metric("Early Detection Flags", f"{subset['Early_Detection_Flag'].sum()}")
    
    # Patient risk table
    st.subheader("📋 High-Risk Patient Details")
    
    high_risk_patients = processed_df[processed_df['Risk_Category'] == 'High Risk'].copy()
    if len(high_risk_patients) > 0:
        # Display key columns for high-risk patients
        display_cols = ['Patient_Age', 'MMSE', 'BMI', 'Risk_Score', 'Early_Detection_Flag']
        available_display_cols = [col for col in display_cols if col in high_risk_patients.columns]
        
        st.dataframe(high_risk_patients[available_display_cols].head(10))
        
        st.info(f"Showing top 10 of {len(high_risk_patients)} high-risk patients requiring immediate attention.")
    
    return processed_df

def dashboard_body():
    st.title("Healthcare Analytics Dashboard")
    
    # Create tabs for different dashboard sections
    tab1, tab2 = st.tabs(["📊 General Analytics", "🏥 Risk Assessment & Early Detection"])
    
    with tab1:
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
        
        st.info("This is a basic dashboard for Alzheimer's Disease data analysis.")

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
    
    with tab2:
        # Risk Assessment Dashboard
        risk_df = risk_assessment_dashboard()
        
        st.markdown("---")
        st.markdown("### 📈 Dashboard Usage Instructions")
        st.markdown("""
        1. **Risk Categories**: Green (Low), Orange (Medium), Red (High)
        2. **Interactive Elements**: Hover over charts for detailed information
        3. **Clinical Thresholds**: 
           - MMSE < 18: Cognitive impairment concern
           - Age > 75: Increased risk factor
           - BMI > 35: High obesity risk
        4. **Early Detection**: Patients flagged for immediate clinical review
        """) 



