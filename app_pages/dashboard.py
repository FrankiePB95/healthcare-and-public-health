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
                          title="3D Risk Assessment: Age vs MMSE vs BMI",
                          labels={
                              "Patient_Age": "Patient Age",
                              "MMSE": "MMSE",
                              "BMI": "BMI",
                              "Risk_Category": "Risk Category",
                              "Risk_Score": "Risk Score",
                              "Cholesterol_Total": "Cholesterol Total",
                              "Functional_Assessment": "Functional Assessment"
                          })
    
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
    
    # Format correlation matrix labels for display
    correlation_matrix_display = correlation_matrix.copy()
    correlation_matrix_display.index = correlation_matrix_display.index.str.replace('_', ' ').str.replace('-', ' ')
    correlation_matrix_display.columns = correlation_matrix_display.columns.str.replace('_', ' ').str.replace('-', ' ')
    
    fig_heatmap = px.imshow(correlation_matrix_display, 
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
        
        # Format column names for display (replace underscores and hyphens with spaces)
        high_risk_display = high_risk_patients[available_display_cols].head(10).copy()
        high_risk_display.columns = high_risk_display.columns.str.replace('_', ' ').str.replace('-', ' ')
        
        st.dataframe(high_risk_display)
        
        st.info(f"Showing top 10 of {len(high_risk_patients)} high-risk patients requiring immediate attention.")
    
    return df

def dashboard_body():
    # Custom CSS for enhanced visual appeal and consistent theme
    st.markdown("""
    <style>
    /* Main background and theme */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Content container styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Header styling */
    h1 {
        color: #2c3e50;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 3rem !important;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Subheader styling */
    h2, h3 {
        color: #34495e;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white !important;
        font-weight: bold;
        border: none;
        padding: 0.8rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #2c3e50 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Info box styling */
    .stAlert > div {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #74b9ff, #0984e3);
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
    }
    
    .streamlit-expanderContent {
        background: rgba(116, 185, 255, 0.1);
        border-radius: 8px;
        border: 1px solid #74b9ff;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }
    
    /* Success/Warning/Error message styling */
    .stSuccess {
        background: linear-gradient(135deg, #00b894, #00a085);
        border-radius: 10px;
        color: white;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fdcb6e, #e17055);
        border-radius: 10px;
        color: white;
    }
    
    /* Metric cards styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        border: none;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea, #764ba2);
    }
    
    /* Custom card styling */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 5px solid #3498db;
    }
    
    /* Text styling improvements */
    .stMarkdown {
        text-align: justify;
        line-height: 1.6;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced title with styling
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🏥 Healthcare Analytics Dashboard</h1>
        <p style="font-size: 1.2rem; color: #7f8c8d; margin-top: 0;">
            Advanced Alzheimer's Disease Risk Assessment & Clinical Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Usage Instructions with custom styling
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #2c3e50; margin-top: 0;">📋 Dashboard Navigation Guide</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Click here for comprehensive usage instructions", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(116, 185, 255, 0.1), rgba(9, 132, 227, 0.1)); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        
        ### 📊 **General Analytics Tab**
        <div style="margin-left: 1rem; margin-bottom: 1rem;">
        • <strong style="color: #3498db;">Dataset Overview</strong>: Comprehensive view of the Alzheimer's disease research dataset<br>
        • <strong style="color: #3498db;">Data Preview</strong>: Interactive exploration of patient demographics and clinical data<br>
        • <strong style="color: #3498db;">Statistical Insights</strong>: Key metrics and distributions across patient populations
        </div>
        
        ### 🏥 **Risk Assessment & Early Detection Tab**
        <div style="margin-left: 1rem; margin-bottom: 1rem;">
        • <strong style="color: #e74c3c;">Risk Stratification</strong>: AI-powered patient categorization system<br>
        • <strong style="color: #e74c3c;">Interactive Visualizations</strong>: Dynamic charts with real-time data insights<br>
        • <strong style="color: #e74c3c;">3D Clinical Analysis</strong>: Multi-dimensional risk factor relationships<br>
        • <strong style="color: #e74c3c;">Correlation Matrix</strong>: Statistical dependencies between health variables
        </div>
        
        ### 🎯 **Risk Classification System**
        <div style="display: flex; justify-content: space-around; margin: 1rem 0;">
            <div style="text-align: center; padding: 0.5rem;">
                <span style="font-size: 2rem;">🟢</span><br>
                <strong style="color: #27ae60;">Low Risk</strong><br>
                <small>Routine monitoring</small>
            </div>
            <div style="text-align: center; padding: 0.5rem;">
                <span style="font-size: 2rem;">🟠</span><br>
                <strong style="color: #f39c12;">Medium Risk</strong><br>
                <small>Enhanced screening</small>
            </div>
            <div style="text-align: center; padding: 0.5rem;">
                <span style="font-size: 2rem;">🔴</span><br>
                <strong style="color: #e74c3c;">High Risk</strong><br>
                <small>Immediate attention</small>
            </div>
        </div>
        
        ### 🏥 **Clinical Decision Thresholds**
        <div style="background: rgba(52, 73, 94, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        • <strong>MMSE Score < 18</strong>: Significant cognitive impairment indicator<br>
        • <strong>Age > 75 years</strong>: Increased neurodegeneration risk factor<br>
        • <strong>BMI > 35 kg/m²</strong>: Severe obesity-related complications<br>
        • <strong>Functional Assessment ≤ 2</strong>: Activities of daily living impairment
        </div>
        
        ### 💡 **Optimization Tips**
        <div style="margin-left: 1rem;">
        1. <strong>Sequential Analysis</strong>: Begin with General Analytics for dataset familiarization<br>
        2. <strong>Interactive Exploration</strong>: Utilize hover functionality for detailed patient profiles<br>
        3. <strong>Pattern Recognition</strong>: Examine correlation heatmaps for clinical insights<br>
        4. <strong>Risk Prioritization</strong>: Focus on high-risk patient clusters in 3D visualizations<br>
        5. <strong>Clinical Integration</strong>: Cross-reference findings with established medical guidelines
        </div>
        
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create tabs for different dashboard sections
    tab1, tab2 = st.tabs(["📊 General Analytics", "🏥 Risk Assessment & Early Detection"])
    
    with tab1:
        # Enhanced General Analytics Tab
        st.markdown("""
        <div class="custom-card">
            <h2 style="color: #2c3e50; margin-top: 0;">📊 Alzheimer's Disease Research Analytics</h2>
            <p style="font-size: 1.1rem; color: #7f8c8d; margin-bottom: 0;">
                Comprehensive clinical dataset analysis for cognitive health research
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Dataset overview with enhanced styling
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="📋 Total Patients", 
                value="537",
                delta="Research Cohort"
            )
        with col2:
            st.metric(
                label="📊 Clinical Features", 
                value="23",
                delta="Biomarkers"
            )
        with col3:
            st.metric(
                label="🎯 Analysis Focus", 
                value="Risk Assessment",
                delta="Early Detection"
            )

        st.markdown("---")

        # Enhanced Data Preview Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(155, 89, 182, 0.1)); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <h3 style="color: #2c3e50; margin-top: 0;">🔍 Clinical Data Preview</h3>
            <p style="color: #7f8c8d;">Sample patient records showing key demographic and clinical parameters</p>
        </div>
        """, unsafe_allow_html=True)
        
        df_display = df.head().copy()
        df_display.columns = df_display.columns.str.replace('_', ' ')
        st.dataframe(df_display, use_container_width=True)
        
        # Enhanced Statistics Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(46, 204, 113, 0.1), rgba(26, 188, 156, 0.1)); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <h3 style="color: #2c3e50; margin-top: 0;">📈 Statistical Summary</h3>
            <p style="color: #7f8c8d;">Descriptive statistics for numerical clinical variables</p>
        </div>
        """, unsafe_allow_html=True)
        
        df_stats = df.describe().copy()
        if 'Patient_ID' in df_stats.columns:
            df_stats = df_stats.drop('Patient_ID', axis=1)
        df_stats.columns = df_stats.columns.str.replace('_', ' ')
        st.dataframe(df_stats, use_container_width=True)
    
    with tab2:
        # Enhanced Risk Assessment Tab
        st.markdown("""
        <div class="custom-card">
            <h2 style="color: #2c3e50; margin-top: 0;">🏥 Advanced Risk Assessment & Clinical Decision Support</h2>
            <p style="font-size: 1.1rem; color: #7f8c8d; margin-bottom: 0;">
                AI-powered patient stratification and early detection system
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Assessment Dashboard
        risk_df = risk_assessment_dashboard() 



