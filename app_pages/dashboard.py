# Import necessary packages
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats
from app_pages.shared_styles import apply_shared_css

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
    Interactive Risk Assessment & Early Detection Dashboard with Filtering
    """
    st.markdown('<h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🏥 Risk Assessment & Early Detection Dashboard</strong></h3>', unsafe_allow_html=True)
    
    # Add comprehensive filtering options
    st.markdown('<h4 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🔍 Patient Population Filters</strong></h4>', unsafe_allow_html=True)
    
    # Add reset button
    reset_col, info_col = st.columns([1, 4])
    with reset_col:
        if st.button("🔄 Reset All Filters", type="secondary"):
            st.experimental_rerun()
    
    with info_col:
        st.info("💡 **Tip:** Use filters to analyze specific patient populations and risk patterns")
    
    # Create filter columns
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        # Gender filter
        gender_options = ['All'] + sorted(df['Gender'].unique().tolist())
        selected_gender = st.selectbox("👤 Gender Filter", gender_options)
        
        # Depression filter
        depression_options = ['All'] + sorted(df['Depression'].unique().tolist())
        selected_depression = st.selectbox("🧠 Depression Status", depression_options)
    
    with filter_col2:
        # Ethnicity filter
        ethnicity_options = ['All'] + sorted(df['Ethnicity'].unique().tolist())
        selected_ethnicity = st.selectbox("🌍 Ethnicity Filter", ethnicity_options)
        
        # Cardiovascular Disease filter
        cvd_options = ['All'] + sorted(df['Cardiovascular_Disease'].unique().tolist())
        selected_cvd = st.selectbox("❤️ Cardiovascular Disease", cvd_options)
    
    with filter_col3:
        # Smoking filter
        smoking_options = ['All'] + sorted(df['Smoking'].unique().tolist())
        selected_smoking = st.selectbox("🚬 Smoking Status", smoking_options)
        
        # Age range filter
        age_min, age_max = int(df['Patient_Age'].min()), int(df['Patient_Age'].max())
        age_range = st.slider("📅 Age Range", age_min, age_max, (age_min, age_max))
    
    with filter_col4:
        # Diagnosis filter
        if 'Diagnosis' in df.columns:
            diagnosis_options = ['All'] + sorted(df['Diagnosis'].unique().tolist())
            selected_diagnosis = st.selectbox("🩺 Diagnosis Filter", diagnosis_options)
        else:
            selected_diagnosis = 'All'
        
        # MMSE range filter
        mmse_min, mmse_max = float(df['MMSE'].min()), float(df['MMSE'].max())
        mmse_range = st.slider("🧩 MMSE Score Range", mmse_min, mmse_max, (mmse_min, mmse_max))
    
    # Apply filters to the dataframe
    filtered_df = df.copy()
    
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    if selected_depression != 'All':
        filtered_df = filtered_df[filtered_df['Depression'] == selected_depression]
    
    if selected_ethnicity != 'All':
        filtered_df = filtered_df[filtered_df['Ethnicity'] == selected_ethnicity]
    
    if selected_cvd != 'All':
        filtered_df = filtered_df[filtered_df['Cardiovascular_Disease'] == selected_cvd]
    
    if selected_smoking != 'All':
        filtered_df = filtered_df[filtered_df['Smoking'] == selected_smoking]
    
    if selected_diagnosis != 'All':
        filtered_df = filtered_df[filtered_df['Diagnosis'] == selected_diagnosis]
    
    # Apply age and MMSE filters
    filtered_df = filtered_df[
        (filtered_df['Patient_Age'] >= age_range[0]) & 
        (filtered_df['Patient_Age'] <= age_range[1])
    ]
    
    filtered_df = filtered_df[
        (filtered_df['MMSE'] >= mmse_range[0]) & 
        (filtered_df['MMSE'] <= mmse_range[1])
    ]
    
    # Display filter summary
    st.markdown("---")
    st.markdown(f"**📊 Filtered Population: {len(filtered_df)} out of {len(df)} patients**")
    
    # Show active filters
    active_filters = []
    if selected_gender != 'All': active_filters.append(f"Gender: {selected_gender}")
    if selected_depression != 'All': active_filters.append(f"Depression: {selected_depression}")
    if selected_ethnicity != 'All': active_filters.append(f"Ethnicity: {selected_ethnicity}")
    if selected_cvd != 'All': active_filters.append(f"CVD: {selected_cvd}")
    if selected_smoking != 'All': active_filters.append(f"Smoking: {selected_smoking}")
    if selected_diagnosis != 'All': active_filters.append(f"Diagnosis: {selected_diagnosis}")
    if age_range != (age_min, age_max): active_filters.append(f"Age: {age_range[0]}-{age_range[1]}")
    if mmse_range != (mmse_min, mmse_max): active_filters.append(f"MMSE: {mmse_range[0]:.1f}-{mmse_range[1]:.1f}")
    
    if active_filters:
        st.info(f"**Active Filters:** {', '.join(active_filters)}")
    
    if len(filtered_df) == 0:
        st.warning("⚠️ No patients match the selected filters. Please adjust your filter criteria.")
        return df
    
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
        1. **Dynamic Filtering System** - Analyze specific patient populations
        2. **Risk Scoring Algorithm** - Multi-factor risk assessment
        3. **Patient Segmentation** - High, Medium, Low risk categories
        4. **Key Risk Indicators** - BMI, MMSE, Age, Cholesterol patterns
        5. **Early Warning System** - Threshold-based alerts
        6. **Intervention Recommendations** - Actionable insights for clinicians
        """)
    
    # Calculate risk scores for filtered data
    if "Risk_Score" not in filtered_df.columns:
        filtered_df["Risk_Score"] = filtered_df.apply(calculate_risk_score, axis=1)
        filtered_df["Risk_Category"] = filtered_df["Risk_Score"].apply(categorize_risk)
        filtered_df["Early_Detection_Flag"] = (
            (filtered_df["MMSE"] < 18) | 
            (filtered_df["Patient_Age"] > 75) | 
            (filtered_df["BMI"] > 35) |
            (filtered_df["Functional_Assessment"] <= 3)
        )
    
    # Key metrics for filtered population
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_patients = len(filtered_df)
        st.metric("Total Patients", total_patients)
    
    with col2:
        high_risk_count = len(filtered_df[filtered_df["Risk_Category"] == "High Risk"])
        high_risk_pct = (high_risk_count/total_patients*100) if total_patients > 0 else 0
        st.metric("High Risk Patients", high_risk_count, delta=f"{high_risk_pct:.1f}%")
    
    with col3:
        early_detection_count = filtered_df["Early_Detection_Flag"].sum()
        early_detection_pct = (early_detection_count/total_patients*100) if total_patients > 0 else 0
        st.metric("Early Detection Flags", early_detection_count, delta=f"{early_detection_pct:.1f}%")
    
    with col4:
        avg_risk_score = filtered_df["Risk_Score"].mean()
        st.metric("Average Risk Score", f"{avg_risk_score:.2f}")
    
    # Risk distribution for filtered data
    st.markdown('<h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>📊 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Risk Category Distribution</span></strong></h3>', unsafe_allow_html=True)
    risk_distribution = filtered_df["Risk_Category"].value_counts()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pie chart for risk distribution
        fig_pie = px.pie(values=risk_distribution.values, names=risk_distribution.index,
                        color_discrete_map={"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#2ecc71"},
                        title="Patient Risk Distribution (Filtered)")
        fig_pie.update_layout(
            title=dict(font=dict(size=16, color="#000000", family="Arial Black")),
            font=dict(size=12, color="#000000", family="Arial", weight="bold"),
            plot_bgcolor="rgba(255, 255, 255, 0.1)",
            paper_bgcolor="rgba(255, 255, 255, 0.1)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart for risk distribution
        fig_bar = px.bar(x=risk_distribution.index, y=risk_distribution.values,
                        color=risk_distribution.index,
                        color_discrete_map={"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#2ecc71"},
                        title="Risk Category Counts (Filtered)")
        fig_bar.update_layout(
            showlegend=False,
            title=dict(font=dict(size=16, color="#000000", family="Arial Black")),
            font=dict(size=12, color="#000000", family="Arial", weight="bold"),
            xaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
            yaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
            plot_bgcolor="rgba(255, 255, 255, 0.1)",
            paper_bgcolor="rgba(255, 255, 255, 0.1)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Interactive 3D Risk Assessment for filtered data
    st.markdown('<h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🎯 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Interactive 3D Risk Assessment Matrix</span></strong></h3>', unsafe_allow_html=True)
    
    fig_3d = px.scatter_3d(filtered_df, 
                          x="Patient_Age", y="MMSE", z="BMI",
                          color="Risk_Category",
                          size="Risk_Score",
                          hover_data=["Cholesterol_Total", "Functional_Assessment", "Gender", "Depression"],
                          color_discrete_map={"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#2ecc71"},
                          title="3D Risk Assessment: Age vs MMSE vs BMI (Filtered Population)",
                          labels={
                              "Patient_Age": "Patient Age",
                              "MMSE": "MMSE",
                              "BMI": "BMI",
                              "Risk_Category": "Risk Category",
                              "Risk_Score": "Risk Score",
                              "Cholesterol_Total": "Cholesterol Total",
                              "Functional_Assessment": "Functional Assessment",
                              "Gender": "Gender",
                              "Depression": "Depression"
                          })
    
    fig_3d.update_layout(
        scene=dict(
            xaxis_title="Patient Age",
            yaxis_title="MMSE Score (Cognitive Function)",
            zaxis_title="BMI",
            xaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
            yaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
            zaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black")))
        ),
        title=dict(font=dict(size=16, color="#000000", family="Arial Black")),
        font=dict(size=12, color="#000000", family="Arial", weight="bold"),
        plot_bgcolor="rgba(255, 255, 255, 0.1)",
        paper_bgcolor="rgba(255, 255, 255, 0.1)"
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Risk factor correlation heatmap for filtered data
    st.markdown('<h4 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🔥 Risk Factor Correlation Analysis</strong></h4>', unsafe_allow_html=True)
    
    risk_variables = ["Patient_Age", "MMSE", "BMI", "Cholesterol_Total", 
                     "Functional_Assessment", "Physical_Activity", 
                     "Alcohol_Consumption", "Risk_Score"]
    
    # Filter variables that exist in the dataframe
    available_vars = [var for var in risk_variables if var in filtered_df.columns]
    correlation_matrix = filtered_df[available_vars].corr()
    
    # Format correlation matrix labels for display
    correlation_matrix_display = correlation_matrix.copy()
    correlation_matrix_display.index = correlation_matrix_display.index.str.replace('_', ' ').str.replace('-', ' ')
    correlation_matrix_display.columns = correlation_matrix_display.columns.str.replace('_', ' ').str.replace('-', ' ')
    
    fig_heatmap = px.imshow(correlation_matrix_display, 
                           text_auto=True, 
                           color_continuous_scale="RdBu_r",
                           title="Risk Factor Correlation Heatmap (Filtered Population)")
    
    fig_heatmap.update_layout(
        title=dict(font=dict(size=16, color="#000000", family="Arial Black")),
        font=dict(size=12, color="#000000", family="Arial", weight="bold"),
        xaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
        yaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
        plot_bgcolor="rgba(255, 255, 255, 0.1)",
        paper_bgcolor="rgba(255, 255, 255, 0.1)"
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Clinical insights by risk category for filtered data
    st.markdown('<h4 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🏥 Clinical Insights by Risk Category</strong></h4>', unsafe_allow_html=True)
    
    for risk_cat in ["High Risk", "Medium Risk", "Low Risk"]:
        subset = filtered_df[filtered_df["Risk_Category"] == risk_cat]
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
                
                # Additional demographic insights for filtered population
                if len(subset) > 0:
                    demo_col1, demo_col2 = st.columns(2)
                    
                    with demo_col1:
                        st.markdown("**Gender Distribution:**")
                        gender_dist = subset['Gender'].value_counts()
                        for gender, count in gender_dist.items():
                            percentage = (count / len(subset)) * 100
                            st.write(f"• {gender}: {count} ({percentage:.1f}%)")
                    
                    with demo_col2:
                        st.markdown("**Depression Status:**")
                        depression_dist = subset['Depression'].value_counts()
                        for status, count in depression_dist.items():
                            percentage = (count / len(subset)) * 100
                            st.write(f"• {status}: {count} ({percentage:.1f}%)")
    
    # Patient risk table for filtered data
    st.markdown('<h4 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>📋 High-Risk Patient Details</strong></h4>', unsafe_allow_html=True)
    
    high_risk_patients = filtered_df[filtered_df["Risk_Category"] == "High Risk"].copy()
    if len(high_risk_patients) > 0:
        # Display key columns for high-risk patients
        display_cols = ["Patient_Age", "Gender", "MMSE", "BMI", "Depression", "Risk_Score", "Early_Detection_Flag"]
        available_display_cols = [col for col in display_cols if col in high_risk_patients.columns]
        
        # Format column names for display (replace underscores and hyphens with spaces)
        high_risk_display = high_risk_patients[available_display_cols].head(10).copy()
        high_risk_display.columns = high_risk_display.columns.str.replace('_', ' ').str.replace('-', ' ')
        
        st.dataframe(high_risk_display)
        
        st.info(f"Showing top 10 of {len(high_risk_patients)} high-risk patients requiring immediate attention.")
        
        # Summary insights for filtered high-risk patients
        if len(high_risk_patients) > 0:
            st.markdown("**🎯 High-Risk Population Insights:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_age = high_risk_patients['Patient_Age'].mean()
                st.metric("Avg Age", f"{avg_age:.1f} years")
            
            with col2:
                avg_mmse = high_risk_patients['MMSE'].mean()
                st.metric("Avg MMSE", f"{avg_mmse:.1f}")
            
            with col3:
                depression_count = (high_risk_patients['Depression'] == 'Yes').sum() if 'Depression' in high_risk_patients.columns else 0
                depression_pct = (depression_count / len(high_risk_patients)) * 100 if len(high_risk_patients) > 0 else 0
                st.metric("Depression Rate", f"{depression_pct:.1f}%")
    else:
        st.info("No high-risk patients found in the filtered population.")
    
    return filtered_df

def dashboard_body():
    # Apply consistent styling across all pages
    apply_shared_css()
    
    # Enhanced title with black text, bold styling, and black underline - icons separate from underlined text
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #000000; font-size: 3rem; margin-bottom: 0.5rem; font-weight: 900;">🏥 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 3px;">Healthcare Analytics Dashboard</span></h1>
        <p style="font-size: 1.2rem; color: #000000; margin-top: 0; font-weight: bold;">
            Advanced Alzheimer's Disease Risk Assessment & Clinical Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Usage Instructions with dark theme and bold black text - icons separate from underlined text
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #000000; margin-top: 0; font-weight: bold;">📋 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Dashboard Navigation Guide</span></h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Click here for comprehensive usage instructions", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(21, 101, 192, 0.3), rgba(25, 118, 210, 0.3)); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        
        ### 📊 **General Analytics Tab**
        <div style="margin-left: 1rem; margin-bottom: 1rem;">
        • <strong style="color: #000000;">Dataset Overview</strong>: Comprehensive view of the Alzheimer's disease research dataset<br>
        • <strong style="color: #000000;">Data Preview</strong>: Interactive exploration of patient demographics and clinical data<br>
        • <strong style="color: #000000;">Statistical Insights</strong>: Key metrics and distributions across patient populations
        </div>
        
        ### 🏥 **Risk Assessment & Early Detection Tab**
        <div style="margin-left: 1rem; margin-bottom: 1rem;">
        • <strong style="color: #000000;">Risk Stratification</strong>: AI-powered patient categorization system<br>
        • <strong style="color: #000000;">Interactive Visualizations</strong>: Dynamic charts with real-time data insights<br>
        • <strong style="color: #000000;">3D Clinical Analysis</strong>: Multi-dimensional risk factor relationships<br>
        • <strong style="color: #000000;">Correlation Matrix</strong>: Statistical dependencies between health variables
        </div>
        
        ### 🎯 **Risk Classification System**
        <div style="display: flex; justify-content: space-around; margin: 1rem 0;">
            <div style="text-align: center; padding: 0.5rem;">
                <span style="font-size: 2rem;">🟢</span><br>
                <strong style="color: #000000;">Low Risk</strong><br>
                <small style="color: #000000;">Routine monitoring</small>
            </div>
            <div style="text-align: center; padding: 0.5rem;">
                <span style="font-size: 2rem;">🟠</span><br>
                <strong style="color: #000000;">Medium Risk</strong><br>
                <small style="color: #000000;">Enhanced screening</small>
            </div>
            <div style="text-align: center; padding: 0.5rem;">
                <span style="font-size: 2rem;">🔴</span><br>
                <strong style="color: #000000;">High Risk</strong><br>
                <small style="color: #000000;">Immediate attention</small>
            </div>
        </div>
        
        ### 🏥 **Clinical Decision Thresholds**
        <div style="background: rgba(52, 73, 94, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        • <strong style="color: #000000;">MMSE Score < 18</strong>: Significant cognitive impairment indicator<br>
        • <strong style="color: #000000;">Age > 75 years</strong>: Increased neurodegeneration risk factor<br>
        • <strong style="color: #000000;">BMI > 35 kg/m²</strong>: Severe obesity-related complications<br>
        • <strong style="color: #000000;">Functional Assessment ≤ 2</strong>: Activities of daily living impairment
        </div>
        
        ### 💡 **Optimization Tips**
        <div style="margin-left: 1rem;">
        1. <strong style="color: #000000;">Sequential Analysis</strong>: Begin with General Analytics for dataset familiarization<br>
        2. <strong style="color: #000000;">Interactive Exploration</strong>: Utilize hover functionality for detailed patient profiles<br>
        3. <strong style="color: #000000;">Pattern Recognition</strong>: Examine correlation heatmaps for clinical insights<br>
        4. <strong style="color: #000000;">Risk Prioritization</strong>: Focus on high-risk patient clusters in 3D visualizations<br>
        5. <strong style="color: #000000;">Clinical Integration</strong>: Cross-reference findings with established medical guidelines
        </div>
        
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create tabs for different dashboard sections
    tab1, tab2 = st.tabs(["📊 General Analytics", "🏥 Risk Assessment & Early Detection"])
    
    with tab1:
        # Enhanced General Analytics Tab - Dark Theme with Bold Black Text - icons separate from underlined text
        st.markdown("""
        <div class="custom-card">
            <h2 style="color: #000000; margin-top: 0; font-weight: bold;">📊 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Alzheimer's Disease Research Analytics</span></h2>
            <p style="font-size: 1.1rem; color: #000000; margin-bottom: 0; font-weight: bold;">
                Comprehensive clinical dataset analysis for cognitive health research
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Dataset overview with enhanced dark theme styling and black text
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
                value="10",
                delta="Biomarkers"
            )
        with col3:
            st.metric(
                label="🎯 Analysis Focus", 
                value="Risk Assessment",
                delta="Early Detection"
            )

        st.markdown("---")

        # Enhanced Data Preview Section - Blue Theme with Bold Black Text and Borders - icons separate from underlined text
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(21, 101, 192, 0.3), rgba(25, 118, 210, 0.3)); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border: 3px solid rgba(100, 100, 120, 0.8); font-weight: bold;">
            <h3 style="color: #000000; margin-top: 0; font-weight: bold;">🔍 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Clinical Data Preview</span></h3>
            <p style="color: #000000; font-weight: bold;">Sample patient records showing key demographic and clinical parameters</p>
        </div>
        """, unsafe_allow_html=True)
        
        df_display = df.head().copy()
        df_display.columns = df_display.columns.str.replace('_', ' ')
        st.dataframe(df_display, use_container_width=True)
        
        # Enhanced Statistics Section - Blue Theme with Bold Black Text and Borders - icons separate from underlined text
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(21, 101, 192, 0.3), rgba(25, 118, 210, 0.3)); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border: 3px solid rgba(100, 100, 120, 0.8); font-weight: bold;">
            <h3 style="color: #000000; margin-top: 0; font-weight: bold;">📈 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Statistical Summary</span></h3>
            <p style="color: #000000; font-weight: bold;">Descriptive statistics for numerical clinical variables</p>
        </div>
        """, unsafe_allow_html=True)
        
        df_stats = df.describe().copy()
        if 'Patient_ID' in df_stats.columns:
            df_stats = df_stats.drop('Patient_ID', axis=1)
        df_stats.columns = df_stats.columns.str.replace('_', ' ')
        st.dataframe(df_stats, use_container_width=True)
    
    with tab2:
        # Enhanced Risk Assessment Tab - Dark Theme with Bold Black Text - Left justified - icons separate from underlined text
        st.markdown("""
        <div class="custom-card" style="text-align: left;">
            <h2 style="color: #000000; margin-top: 0; font-weight: bold; text-align: left;">🏥 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Advanced Risk Assessment & Clinical Decision Support</span></h2>
            <p style="font-size: 1.1rem; color: #000000; margin-bottom: 0; font-weight: bold; text-align: left;">
                AI-powered patient stratification and early detection system
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Assessment Dashboard
        risk_df = risk_assessment_dashboard() 



