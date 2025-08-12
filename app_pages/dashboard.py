# Import necessary packages
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats

# Load processed data (already cleaned and transformed)
df = pd.read_csv("outputs/processed_alzheimers_disease_data_unscaled_and_unencoded.csv")

# Risk Assessment Functions
def calculate_risk_score(row):
    """
    Calculate comprehensive risk score based on multiple health factors
    Higher scores indicate higher risk for cognitive decline/dementia
    """
    risk_score = 0
    
    # Age risk (40% weight) - older patients at higher risk
    if row["Patient_Age"] >= 80:
        risk_score += 4
    elif row["Patient_Age"] >= 75:
        risk_score += 3
    elif row["Patient_Age"] >= 70:
        risk_score += 2
    else:
        risk_score += 1
        
    # MMSE risk (30% weight) - lower scores indicate cognitive impairment
    if row["MMSE"] < 10:
        risk_score += 3
    elif row["MMSE"] < 18:
        risk_score += 2.5
    elif row["MMSE"] < 24:
        risk_score += 1.5
    else:
        risk_score += 0.5
        
    # BMI risk (15% weight) - both high and low BMI are risk factors
    if row["BMI"] > 35 or row["BMI"] < 18.5:
        risk_score += 1.5
    elif row["BMI"] > 30 or row["BMI"] < 20:
        risk_score += 1
    else:
        risk_score += 0.5
        
    # Functional Assessment (10% weight) - lower scores indicate dependency
    if row["Functional_Assessment"] <= 2:
        risk_score += 1
    elif row["Functional_Assessment"] <= 4:
        risk_score += 0.7
    else:
        risk_score += 0.3
        
    # Cholesterol risk (5% weight) - very high or very low can be concerning
    if row["Cholesterol_Total"] > 280 or row["Cholesterol_Total"] < 160:
        risk_score += 0.5
    elif row["Cholesterol_Total"] > 240:
        risk_score += 0.3
        
    return round(risk_score, 2)

def categorize_risk(score):
    if score >= 7:
        return "High Risk"
    elif score >= 5:
        return "Medium Risk"
    else:
        return "Low Risk"

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
    if "Risk_Score" not in df.columns:
        df["Risk_Score"] = df.apply(calculate_risk_score, axis=1)
        df["Risk_Category"] = df["Risk_Score"].apply(categorize_risk)
        df["Early_Detection_Flag"] = (
            (df["MMSE"] < 18) | 
            (df["Patient_Age"] > 75) | 
            (df["BMI"] > 35) |
            (df["Functional_Assessment"] <= 3)
        )
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_patients = len(df)
        st.metric("Total Patients", total_patients)
    
    with col2:
        high_risk_count = len(df[df["Risk_Category"] == "High Risk"])
        st.metric("High Risk Patients", high_risk_count, delta=f"{(high_risk_count/total_patients*100):.1f}%")
    
    with col3:
        early_detection_count = df["Early_Detection_Flag"].sum()
        st.metric("Early Detection Flags", early_detection_count, delta=f"{(early_detection_count/total_patients*100):.1f}%")
    
    with col4:
        avg_risk_score = df["Risk_Score"].mean()
        st.metric("Average Risk Score", f"{avg_risk_score:.2f}")
    
    # Risk distribution
    st.subheader("📊 Risk Category Distribution")
    risk_distribution = df["Risk_Category"].value_counts()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pie chart for risk distribution
        fig_pie = px.pie(values=risk_distribution.values, names=risk_distribution.index,
                        color_discrete_map={"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#2ecc71"},
                        title="Patient Risk Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart for risk distribution
        fig_bar = px.bar(x=risk_distribution.index, y=risk_distribution.values,
                        color=risk_distribution.index,
                        color_discrete_map={"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#2ecc71"},
                        title="Risk Category Counts")
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Interactive 3D Risk Assessment
    st.subheader("🎯 Interactive 3D Risk Assessment Matrix")
    
    fig_3d = px.scatter_3d(df, 
                          x="Patient_Age", y="MMSE", z="BMI",
                          color="Risk_Category",
                          size="Risk_Score",
                          hover_data=["Cholesterol_Total", "Functional_Assessment"],
                          color_discrete_map={"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#2ecc71"},
                          title="3D Risk Assessment: Age vs MMSE vs BMI")
    
    fig_3d.update_layout(scene=dict(
        xaxis_title="Patient Age",
        yaxis_title="MMSE Score (Cognitive Function)",
        zaxis_title="BMI"
    ))
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Risk factor correlation heatmap
    st.subheader("🔥 Risk Factor Correlation Analysis")
    
    risk_variables = ["Patient_Age", "MMSE", "BMI", "Cholesterol_Total", 
                     "Functional_Assessment", "Physical_Activity", 
                     "Alcohol_Consumption", "Risk_Score"]
    
    # Filter variables that exist in the dataframe
    available_vars = [var for var in risk_variables if var in df.columns]
    correlation_matrix = df[available_vars].corr()
    
    fig_heatmap = px.imshow(correlation_matrix, 
                           text_auto=True, 
                           color_continuous_scale="RdBu_r",
                           title="Risk Factor Correlation Heatmap")
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Clinical insights by risk category
    st.subheader("🏥 Clinical Insights by Risk Category")
    
    for risk_cat in ["High Risk", "Medium Risk", "Low Risk"]:
        subset = df[df["Risk_Category"] == risk_cat]
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
    
    high_risk_patients = df[df["Risk_Category"] == "High Risk"].copy()
    if len(high_risk_patients) > 0:
        # Display key columns for high-risk patients
        display_cols = ["Patient_Age", "MMSE", "BMI", "Risk_Score", "Early_Detection_Flag"]
        available_display_cols = [col for col in display_cols if col in high_risk_patients.columns]
        
        st.dataframe(high_risk_patients[available_display_cols].head(10))
        
        st.info(f"Showing top 10 of {len(high_risk_patients)} high-risk patients requiring immediate attention.")
    
    return df

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
        df_display = df.head().copy()
        df_display.columns = df_display.columns.str.replace('_', ' ')
        st.dataframe(df_display)
        
        # Basic statistics
        st.subheader("Basic Statistics")
        df_stats = df.describe().copy()
        df_stats.columns = df_stats.columns.str.replace('_', ' ')
        st.dataframe(df_stats)
    
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



