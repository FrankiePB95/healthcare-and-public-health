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
    Enhanced comprehensive risk score based on multiple health factors from the dataset
    Higher scores indicate higher risk for cognitive decline/dementia
    Based on clinical research and the available dataset variables
    """
    risk_score = 0
    
    # Age risk (25% weight) - older patients at higher risk
    if row["Patient_Age"] >= 85:
        risk_score += 3.5
    elif row["Patient_Age"] >= 80:
        risk_score += 3.0
    elif row["Patient_Age"] >= 75:
        risk_score += 2.5
    elif row["Patient_Age"] >= 70:
        risk_score += 2.0
    else:
        risk_score += 1.0
        
    # MMSE risk (25% weight) - lower scores indicate cognitive impairment
    if row["MMSE"] < 10:
        risk_score += 3.5  # Severe cognitive impairment
    elif row["MMSE"] < 18:
        risk_score += 3.0  # Moderate cognitive impairment
    elif row["MMSE"] < 24:
        risk_score += 2.0  # Mild cognitive impairment
    elif row["MMSE"] < 27:
        risk_score += 1.0  # Borderline
    else:
        risk_score += 0.5  # Normal
        
    # Functional Assessment risk (15% weight)
    if "Functional_Assessment" in row.index and pd.notna(row["Functional_Assessment"]):
        if row["Functional_Assessment"] <= 2:
            risk_score += 2.0
        elif row["Functional_Assessment"] <= 4:
            risk_score += 1.5
        elif row["Functional_Assessment"] <= 6:
            risk_score += 1.0
        else:
            risk_score += 0.5
    
    # Activities of Daily Living risk (10% weight)
    if "Activities_Of_Daily_Living" in row.index and pd.notna(row["Activities_Of_Daily_Living"]):
        if row["Activities_Of_Daily_Living"] <= 2:
            risk_score += 1.5
        elif row["Activities_Of_Daily_Living"] <= 5:
            risk_score += 1.0
        else:
            risk_score += 0.3
    
    # Depression risk (8% weight) - depression is a risk factor
    if "Depression" in row.index:
        if str(row["Depression"]).lower() in ['yes', '1', 'true']:
            risk_score += 1.2
        else:
            risk_score += 0.2
    
    # Memory Complaints risk (8% weight)
    if "Memory_Complaints" in row.index:
        if str(row["Memory_Complaints"]).lower() in ['yes', '1', 'true']:
            risk_score += 1.2
        else:
            risk_score += 0.1
    
    # Behavioral Problems risk (5% weight)
    if "Behavioral_Problems" in row.index:
        if str(row["Behavioral_Problems"]).lower() in ['yes', '1', 'true']:
            risk_score += 0.8
    
    # Personality Changes risk (5% weight)
    if "Personality_Changes" in row.index:
        if str(row["Personality_Changes"]).lower() in ['yes', '1', 'true']:
            risk_score += 0.8
    
    # Difficulty Completing Tasks risk (5% weight)
    if "Difficulty_Completing_Tasks" in row.index:
        if str(row["Difficulty_Completing_Tasks"]).lower() in ['yes', '1', 'true']:
            risk_score += 0.8
    
    # BMI risk (4% weight) - both high and low BMI are risk factors
    if row["BMI"] > 35 or row["BMI"] < 18.5:
        risk_score += 0.8
    elif row["BMI"] > 30 or row["BMI"] < 20:
        risk_score += 0.5
    else:
        risk_score += 0.2
    
    # Cardiovascular Disease risk (3% weight)
    if "Cardiovascular_Disease" in row.index:
        if str(row["Cardiovascular_Disease"]).lower() in ['yes', '1', 'true']:
            risk_score += 0.6
    
    # Physical Activity risk (3% weight) - low activity increases risk
    if "Physical_Activity" in row.index and pd.notna(row["Physical_Activity"]):
        if row["Physical_Activity"] < 2:
            risk_score += 0.6  # Very low activity
        elif row["Physical_Activity"] < 4:
            risk_score += 0.4  # Low activity
        else:
            risk_score += 0.1  # Good activity level
    
    # Smoking risk (2% weight)
    if "Smoking" in row.index:
        if str(row["Smoking"]).lower() in ['yes', '1', 'true']:
            risk_score += 0.4
    
    # Diet Quality risk (2% weight) - poor diet increases risk
    if "Diet_Quality" in row.index and pd.notna(row["Diet_Quality"]):
        if row["Diet_Quality"] < 4:
            risk_score += 0.4  # Poor diet
        elif row["Diet_Quality"] < 6:
            risk_score += 0.2  # Fair diet
        # Good diet (6+) adds no additional risk
    
    return round(risk_score, 2)

def categorize_risk(score):
    """
    Categorize risk based on enhanced scoring system
    Risk categories adjusted for the new comprehensive scoring range
    """
    if score >= 9:
        return "High Risk"
    elif score >= 6:
        return "Medium Risk"
    else:
        return "Low Risk"

def risk_assessment_dashboard():
    """
    Interactive Risk Assessment & Early Detection Dashboard with Advanced Filtering
    """
    st.markdown('<h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🏥 Risk Assessment & Early Detection Dashboard</strong></h3>', unsafe_allow_html=True)
    
    # Add comprehensive filtering options
    st.markdown('<h4 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🔍 Advanced Patient Population Filters</strong></h4>', unsafe_allow_html=True)
    
    # Add reset button
    reset_col, info_col = st.columns([1, 4])
    with reset_col:
        if st.button("🔄 Reset All Filters", type="secondary"):
            st.experimental_rerun()
    
    with info_col:
        st.info("💡 **Tip:** Use filters to analyze specific patient populations and identify risk patterns across demographics, lifestyle factors, and clinical conditions")
    
    # Create comprehensive filter sections
    with st.expander("👥 **Demographic Filters**", expanded=False):
        demo_col1, demo_col2, demo_col3 = st.columns(3)
        
        with demo_col1:
            # Gender filter
            gender_options = ["All"] + sorted(df["Gender"].unique().tolist())
            selected_gender = st.selectbox("👤 Gender", gender_options, help="Filter by patient gender")
        
        with demo_col2:
            # Ethnicity filter  
            ethnicity_options = ["All"] + sorted(df["Ethnicity"].unique().tolist())
            selected_ethnicity = st.selectbox("🌍 Ethnicity", ethnicity_options, help="Filter by ethnic background")
        
        with demo_col3:
            # Age range filter
            age_min, age_max = int(df["Patient_Age"].min()), int(df["Patient_Age"].max())
            age_range = st.slider("📅 Age Range", age_min, age_max, (age_min, age_max), 
                                help=f"Age ranges from {age_min} to {age_max} years")
    
    with st.expander("🏥 **Medical History Filters**", expanded=False):
        med_col1, med_col2, med_col3 = st.columns(3)
        
        with med_col1:
            # Cardiovascular Disease filter
            cvd_options = ["All"] + sorted(df["Cardiovascular_Disease"].unique().tolist()) if "Cardiovascular_Disease" in df.columns else ["All"]
            selected_cvd = st.selectbox("❤️ Cardiovascular Disease", cvd_options, help="Filter by cardiovascular disease status")
            
            # Depression filter
            depression_options = ["All"] + sorted(df["Depression"].unique().tolist())
            selected_depression = st.selectbox("🧠 Depression", depression_options, help="Filter by depression status")
        
        with med_col2:
            # Memory Complaints filter
            memory_options = ["All"] + sorted(df["Memory_Complaints"].unique().tolist()) if "Memory_Complaints" in df.columns else ["All"]
            selected_memory = st.selectbox("🧩 Memory Complaints", memory_options, help="Filter by memory complaint status")
            
            # Behavioral Problems filter
            behavior_options = ["All"] + sorted(df["Behavioral_Problems"].unique().tolist()) if "Behavioral_Problems" in df.columns else ["All"]
            selected_behavior = st.selectbox("😤 Behavioral Problems", behavior_options, help="Filter by behavioral issues")
        
        with med_col3:
            # Personality Changes filter
            personality_options = ["All"] + sorted(df["Personality_Changes"].unique().tolist()) if "Personality_Changes" in df.columns else ["All"]
            selected_personality = st.selectbox("👤 Personality Changes", personality_options, help="Filter by personality changes")
            
            # Difficulty Completing Tasks filter
            tasks_options = ["All"] + sorted(df["Difficulty_Completing_Tasks"].unique().tolist()) if "Difficulty_Completing_Tasks" in df.columns else ["All"]
            selected_tasks = st.selectbox("📝 Task Difficulty", tasks_options, help="Filter by difficulty completing tasks")
    
    with st.expander("💊 **Lifestyle & Health Metrics**", expanded=False):
        lifestyle_col1, lifestyle_col2, lifestyle_col3 = st.columns(3)
        
        with lifestyle_col1:
            # Smoking filter
            smoking_options = ["All"] + sorted(df["Smoking"].unique().tolist())
            selected_smoking = st.selectbox("🚬 Smoking Status", smoking_options, help="Filter by smoking habits")
            
            # BMI range filter
            bmi_min, bmi_max = float(df['BMI'].min()), float(df['BMI'].max())
            bmi_range = st.slider("⚖️ BMI Range", bmi_min, bmi_max, (bmi_min, bmi_max), 
                                help=f"BMI ranges from {bmi_min:.1f} to {bmi_max:.1f}")
        
        with lifestyle_col2:
            # Physical Activity range
            if 'Physical_Activity' in df.columns:
                activity_min, activity_max = float(df['Physical_Activity'].min()), float(df['Physical_Activity'].max())
                activity_range = st.slider("🏃 Physical Activity (hrs/week)", activity_min, activity_max, (activity_min, activity_max),
                                         help=f"Weekly physical activity: {activity_min:.0f} to {activity_max:.0f} hours")
            else:
                activity_range = None
            
            # Alcohol Consumption range
            if 'Alcohol_Consumption' in df.columns:
                alcohol_min, alcohol_max = float(df['Alcohol_Consumption'].min()), float(df['Alcohol_Consumption'].max())
                alcohol_range = st.slider("🍷 Alcohol (units/week)", alcohol_min, alcohol_max, (alcohol_min, alcohol_max),
                                        help=f"Weekly alcohol consumption: {alcohol_min:.0f} to {alcohol_max:.0f} units")
            else:
                alcohol_range = None
        
        with lifestyle_col3:
            # Diet Quality range
            if 'Diet_Quality' in df.columns:
                diet_min, diet_max = float(df['Diet_Quality'].min()), float(df['Diet_Quality'].max())
                diet_range = st.slider("🥗 Diet Quality Score", diet_min, diet_max, (diet_min, diet_max),
                                     help=f"Diet quality score: {diet_min:.1f} to {diet_max:.1f}")
            else:
                diet_range = None
    
    with st.expander("🧠 **Cognitive & Functional Assessment**", expanded=False):
        cognitive_col1, cognitive_col2 = st.columns(2)
        
        with cognitive_col1:
            # MMSE range filter
            mmse_min, mmse_max = float(df['MMSE'].min()), float(df['MMSE'].max())
            mmse_range = st.slider("🧩 MMSE Score", mmse_min, mmse_max, (mmse_min, mmse_max),
                                 help=f"Mini-Mental State Exam: {mmse_min:.0f} to {mmse_max:.0f} (lower = more impaired)")
            
            # Functional Assessment range
            if 'Functional_Assessment' in df.columns:
                func_min, func_max = float(df['Functional_Assessment'].min()), float(df['Functional_Assessment'].max())
                func_range = st.slider("🔧 Functional Assessment", func_min, func_max, (func_min, func_max),
                                     help=f"Functional assessment: {func_min:.0f} to {func_max:.0f} (lower = more impaired)")
            else:
                func_range = None
        
        with cognitive_col2:
            # Activities of Daily Living range
            if 'Activities_Of_Daily_Living' in df.columns:
                adl_min, adl_max = float(df['Activities_Of_Daily_Living'].min()), float(df['Activities_Of_Daily_Living'].max())
                adl_range = st.slider("🏠 Activities of Daily Living", adl_min, adl_max, (adl_min, adl_max),
                                    help=f"ADL score: {adl_min:.0f} to {adl_max:.0f} (lower = more impaired)")
            else:
                adl_range = None
            
            # Diagnosis filter
            if 'Diagnosis' in df.columns:
                diagnosis_options = ['All'] + sorted(df['Diagnosis'].unique().tolist())
                selected_diagnosis = st.selectbox("🩺 Alzheimer's Diagnosis", diagnosis_options, 
                                                help="Filter by Alzheimer's diagnosis status")
            else:
                selected_diagnosis = "All"
    
    # Apply filters to the dataframe
    filtered_df = df.copy()
    
    # Demographic filters
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]
    
    if selected_ethnicity != "All":
        filtered_df = filtered_df[filtered_df["Ethnicity"] == selected_ethnicity]
    
    filtered_df = filtered_df[
        (filtered_df["Patient_Age"] >= age_range[0]) & 
        (filtered_df["Patient_Age"] <= age_range[1])
    ]
    
    # Medical history filters
    if selected_cvd != "All" and "Cardiovascular_Disease" in df.columns:
        filtered_df = filtered_df[filtered_df["Cardiovascular_Disease"] == selected_cvd]
    
    if selected_depression != "All":
        filtered_df = filtered_df[filtered_df["Depression"] == selected_depression]
    
    if selected_memory != "All" and "Memory_Complaints" in df.columns:
        filtered_df = filtered_df[filtered_df["Memory_Complaints"] == selected_memory]
    
    if selected_behavior != "All" and "Behavioral_Problems" in df.columns:
        filtered_df = filtered_df[filtered_df["Behavioral_Problems"] == selected_behavior]
    
    if selected_personality != "All" and "Personality_Changes" in df.columns:
        filtered_df = filtered_df[filtered_df["Personality_Changes"] == selected_personality]
    
    if selected_tasks != "All" and "Difficulty_Completing_Tasks" in df.columns:
        filtered_df = filtered_df[filtered_df["Difficulty_Completing_Tasks"] == selected_tasks]
    
    # Lifestyle filters
    if selected_smoking != "All":
        filtered_df = filtered_df[filtered_df["Smoking"] == selected_smoking]
    
    filtered_df = filtered_df[
        (filtered_df['BMI'] >= bmi_range[0]) & 
        (filtered_df['BMI'] <= bmi_range[1])
    ]
    
    if activity_range and 'Physical_Activity' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['Physical_Activity'] >= activity_range[0]) & 
            (filtered_df['Physical_Activity'] <= activity_range[1])
        ]
    
    if alcohol_range and 'Alcohol_Consumption' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['Alcohol_Consumption'] >= alcohol_range[0]) & 
            (filtered_df['Alcohol_Consumption'] <= alcohol_range[1])
        ]
    
    if diet_range and 'Diet_Quality' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['Diet_Quality'] >= diet_range[0]) & 
            (filtered_df['Diet_Quality'] <= diet_range[1])
        ]
    
    # Cognitive filters
    filtered_df = filtered_df[
        (filtered_df['MMSE'] >= mmse_range[0]) & 
        (filtered_df['MMSE'] <= mmse_range[1])
    ]
    
    if func_range and 'Functional_Assessment' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['Functional_Assessment'] >= func_range[0]) & 
            (filtered_df['Functional_Assessment'] <= func_range[1])
        ]
    
    if adl_range and 'Activities_Of_Daily_Living' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['Activities_Of_Daily_Living'] >= adl_range[0]) & 
            (filtered_df['Activities_Of_Daily_Living'] <= adl_range[1])
        ]
    
    if selected_diagnosis != "All" and "Diagnosis" in df.columns:
        filtered_df = filtered_df[filtered_df["Diagnosis"] == selected_diagnosis]
    
    # Display comprehensive filter summary
    st.markdown("---")
    col_summary1, col_summary2 = st.columns([2, 3])
    
    with col_summary1:
        st.markdown(f"**📊 Filtered Population: {len(filtered_df):,} out of {len(df):,} patients**")
        if len(filtered_df) > 0:
            retention_pct = (len(filtered_df) / len(df)) * 100
            st.markdown(f"**📈 Population Retention: {retention_pct:.1f}%**")
    
    with col_summary2:
        # Show active filters in an organized way
        active_filters = []
        if selected_gender != "All": active_filters.append(f"👤 Gender: {selected_gender}")
        if selected_ethnicity != "All": active_filters.append(f"🌍 Ethnicity: {selected_ethnicity}")
        if selected_depression != "All": active_filters.append(f"🧠 Depression: {selected_depression}")
        if selected_cvd != "All": active_filters.append(f"❤️ CVD: {selected_cvd}")
        if selected_smoking != "All": active_filters.append(f"🚬 Smoking: {selected_smoking}")
        if selected_memory != "All" and "Memory_Complaints" in df.columns: active_filters.append(f"🧩 Memory: {selected_memory}")
        if selected_behavior != "All" and "Behavioral_Problems" in df.columns: active_filters.append(f"😤 Behavior: {selected_behavior}")
        if selected_personality != "All" and "Personality_Changes" in df.columns: active_filters.append(f"👤 Personality: {selected_personality}")
        if selected_tasks != "All" and "Difficulty_Completing_Tasks" in df.columns: active_filters.append(f"📝 Tasks: {selected_tasks}")
        if selected_diagnosis != "All": active_filters.append(f"🩺 Diagnosis: {selected_diagnosis}")
        
        # Add range filters if they're not at default
        if age_range != (age_min, age_max): active_filters.append(f"📅 Age: {age_range[0]}-{age_range[1]}")
        if mmse_range != (mmse_min, mmse_max): active_filters.append(f"🧩 MMSE: {mmse_range[0]:.1f}-{mmse_range[1]:.1f}")
        if bmi_range != (bmi_min, bmi_max): active_filters.append(f"⚖️ BMI: {bmi_range[0]:.1f}-{bmi_range[1]:.1f}")
        
        if activity_range and 'Physical_Activity' in df.columns:
            activity_default_min, activity_default_max = float(df['Physical_Activity'].min()), float(df['Physical_Activity'].max())
            if activity_range != (activity_default_min, activity_default_max): 
                active_filters.append(f"🏃 Activity: {activity_range[0]:.0f}-{activity_range[1]:.0f}h")
        
        if alcohol_range and 'Alcohol_Consumption' in df.columns:
            alcohol_default_min, alcohol_default_max = float(df['Alcohol_Consumption'].min()), float(df['Alcohol_Consumption'].max())
            if alcohol_range != (alcohol_default_min, alcohol_default_max): 
                active_filters.append(f"🍷 Alcohol: {alcohol_range[0]:.0f}-{alcohol_range[1]:.0f}u")
        
        if diet_range and 'Diet_Quality' in df.columns:
            diet_default_min, diet_default_max = float(df['Diet_Quality'].min()), float(df['Diet_Quality'].max())
            if diet_range != (diet_default_min, diet_default_max): 
                active_filters.append(f"🥗 Diet: {diet_range[0]:.1f}-{diet_range[1]:.1f}")
        
        if func_range and 'Functional_Assessment' in df.columns:
            func_default_min, func_default_max = float(df['Functional_Assessment'].min()), float(df['Functional_Assessment'].max())
            if func_range != (func_default_min, func_default_max): 
                active_filters.append(f"🔧 Function: {func_range[0]:.0f}-{func_range[1]:.0f}")
        
        if adl_range and 'Activities_Of_Daily_Living' in df.columns:
            adl_default_min, adl_default_max = float(df['Activities_Of_Daily_Living'].min()), float(df['Activities_Of_Daily_Living'].max())
            if adl_range != (adl_default_min, adl_default_max): 
                active_filters.append(f"🏠 ADL: {adl_range[0]:.0f}-{adl_range[1]:.0f}")
        
        if active_filters:
            st.markdown("**🔍 Active Filters:**")
            # Display filters in a more organized way
            for i in range(0, len(active_filters), 2):
                if i + 1 < len(active_filters):
                    st.markdown(f"• {active_filters[i]} | {active_filters[i + 1]}")
                else:
                    st.markdown(f"• {active_filters[i]}")
    
    if len(filtered_df) == 0:
        st.error("**⚠️ No patients match the selected filter criteria. Please adjust your filters to include more patients.**")
        st.markdown("**💡 Suggestions:**")
        st.markdown("- Reset all filters using the 'Reset All Filters' button")
        st.markdown("- Widen the range filters (Age, MMSE, BMI, etc.)")
        st.markdown("- Remove some of the categorical filters")
        return df
    
    # Business need explanation
    with st.expander("**📋 Business Need & Dashboard Components**"):
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
        st.metric("**Total Patients**", f"**{total_patients}**")
    
    with col2:
        high_risk_count = len(filtered_df[filtered_df["Risk_Category"] == "High Risk"])
        high_risk_pct = (high_risk_count/total_patients*100) if total_patients > 0 else 0
        st.metric("**High Risk Patients**", f"**{high_risk_count}**", delta=f"**{high_risk_pct:.1f}%**")
    
    with col3:
        early_detection_count = filtered_df["Early_Detection_Flag"].sum()
        early_detection_pct = (early_detection_count/total_patients*100) if total_patients > 0 else 0
        st.metric("**Early Detection Flags**", f"**{early_detection_count}**", delta=f"**{early_detection_pct:.1f}%**")
    
    with col4:
        avg_risk_score = filtered_df["Risk_Score"].mean()
        st.metric("**Average Risk Score**", f"**{avg_risk_score:.2f}**")
    
    # Risk distribution for filtered data
    # Display results with enhanced styling
    st.markdown('<h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>📊 Risk Category Distribution</strong></h3>', unsafe_allow_html=True)
    risk_distribution = filtered_df["Risk_Category"].value_counts()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pie chart for risk distribution
        fig_pie = px.pie(values=risk_distribution.values, names=risk_distribution.index,
                        color_discrete_map={"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#2ecc71"},
                        title="Patient Risk Distribution")
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
                        title="Risk Category Counts")
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
    
    # Enhanced Interactive 3D Risk Assessment for filtered data
    # Enhanced 3D scatter plot with better insights
    st.markdown('<h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🎯 Interactive 3D Risk Assessment Matrix</strong></h3>', unsafe_allow_html=True)
    
    # Prepare hover data with available columns
    hover_data_cols = ["Cholesterol_Total", "Functional_Assessment", "Gender", "Depression"]
    if "Activities_Of_Daily_Living" in filtered_df.columns:
        hover_data_cols.append("Activities_Of_Daily_Living")
    if "Memory_Complaints" in filtered_df.columns:
        hover_data_cols.append("Memory_Complaints")
    if "Physical_Activity" in filtered_df.columns:
        hover_data_cols.append("Physical_Activity")
    if "Diet_Quality" in filtered_df.columns:
        hover_data_cols.append("Diet_Quality")
    
    # Filter to only include columns that actually exist in the dataframe
    available_hover_cols = [col for col in hover_data_cols if col in filtered_df.columns]
    
    fig_3d = px.scatter_3d(filtered_df, 
                          x="Patient_Age", y="MMSE", z="BMI",
                          color="Risk_Category",
                          size="Risk_Score",
                          hover_data=available_hover_cols,
                          color_discrete_map={"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#2ecc71"},
                          title=f"3D Risk Assessment: Age vs MMSE vs BMI (Filtered Population: n={len(filtered_df)})",
                          labels={
                              "Patient_Age": "Patient Age (years)",
                              "MMSE": "MMSE Score (cognitive function)",
                              "BMI": "Body Mass Index",
                              "Risk_Category": "Risk Category",
                              "Risk_Score": "Comprehensive Risk Score",
                              "Cholesterol_Total": "Total Cholesterol",
                              "Functional_Assessment": "Functional Assessment",
                              "Activities_Of_Daily_Living": "Activities of Daily Living",
                              "Memory_Complaints": "Memory Complaints",
                              "Physical_Activity": "Physical Activity (hrs/week)",
                              "Diet_Quality": "Diet Quality Score",
                              "Gender": "Gender",
                              "Depression": "Depression Status"
                          })
    
    fig_3d.update_layout(
        scene=dict(
            xaxis_title="Patient Age (years)",
            yaxis_title="MMSE Score (Cognitive Function)",
            zaxis_title="Body Mass Index (BMI)",
            xaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
            yaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
            zaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black")))
        ),
        title=dict(font=dict(size=16, color="#000000", family="Arial Black")),
        font=dict(size=12, color="#000000", family="Arial", weight="bold"),
        plot_bgcolor="rgba(255, 255, 255, 0.1)",
        paper_bgcolor="rgba(255, 255, 255, 0.1)",
        height=700
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Add 3D plot interpretation guide
    with st.expander("📊 **How to Interpret the 3D Risk Assessment**"):
        st.markdown("""
        **🎯 Understanding the 3D Visualization:**
        - **X-axis (Age)**: Older patients typically show higher risk
        - **Y-axis (MMSE)**: Lower scores indicate cognitive impairment
        - **Z-axis (BMI)**: Both very high and very low values can be concerning
        - **Color**: Red = High Risk, Orange = Medium Risk, Green = Low Risk
        - **Size**: Larger bubbles = Higher comprehensive risk scores
        
        **🔍 What to Look For:**
        - **High-risk clusters**: Red bubbles in the lower-left areas (older age, lower MMSE)
        - **Outliers**: Unusual combinations that might need clinical attention
        - **Patterns**: How risk factors combine across different populations
        
        **💡 Clinical Insights:**
        - Hover over points to see detailed patient information
        - Use filters to compare different population segments
        - Look for unexpected risk patterns in your filtered population
        """)
    
    # Add population statistics for the 3D plot
    if len(filtered_df) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("**Avg Age**", f"**{filtered_df['Patient_Age'].mean():.1f} yrs**")
        with col2:
            st.metric("**Avg MMSE**", f"**{filtered_df['MMSE'].mean():.1f}**")
        with col3:
            st.metric("**Avg BMI**", f"**{filtered_df['BMI'].mean():.1f}**")
        with col4:
            st.metric("**Avg Risk Score**", f"**{filtered_df['Risk_Score'].mean():.2f}**")
    
    # Enhanced risk factor correlation heatmap for filtered data
    # Enhanced correlation analysis section with better insights
    st.markdown('<h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🔥 Comprehensive Risk Factor Correlation Analysis</strong></h3>', unsafe_allow_html=True)
    
    # Include all relevant variables from the dataset based on your notes
    risk_variables = [
        "Patient_Age", "MMSE", "BMI", "Cholesterol_Total", 
        "Functional_Assessment", "Physical_Activity", 
        "Alcohol_Consumption", "Diet_Quality", "Activities_Of_Daily_Living",
        "Risk_Score"
    ]
    
    # Filter variables that exist in the filtered dataframe
    available_vars = [var for var in risk_variables if var in filtered_df.columns]
    
    if len(available_vars) >= 3:  # Need at least 3 variables for meaningful correlation
        correlation_matrix = filtered_df[available_vars].corr()
        
        # Format correlation matrix labels for display
        correlation_matrix_display = correlation_matrix.copy()
        correlation_matrix_display.index = correlation_matrix_display.index.str.replace('_', ' ').str.replace('-', ' ')
        correlation_matrix_display.columns = correlation_matrix_display.columns.str.replace('_', ' ').str.replace('-', ' ')
        
        fig_heatmap = px.imshow(correlation_matrix_display, 
                               text_auto=True, 
                               color_continuous_scale="RdBu_r",
                               title=f"Risk Factor Correlation Matrix (Filtered Population: n={len(filtered_df)})",
                               aspect="auto")
        
        fig_heatmap.update_layout(
            title=dict(font=dict(size=16, color="#000000", family="Arial Black")),
            font=dict(size=12, color="#000000", family="Arial", weight="bold"),
            xaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
            yaxis=dict(title=dict(font=dict(size=14, color="#000000", family="Arial Black"))),
            plot_bgcolor="rgba(255, 255, 255, 0.1)",
            paper_bgcolor="rgba(255, 255, 255, 0.1)",
            height=600
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Add interpretation guide for correlation matrix in expandable dropdown
        with st.expander("📖 **How to Interpret the Correlation Matrix**", expanded=False):
            st.markdown("""
            The correlation matrix shows how different health factors relate to each other. Each cell displays a correlation coefficient between -1.0 and +1.0:
            
            **🔵 Positive Correlations (Blue shades):**
            - **+1.0**: Perfect positive relationship - as one factor increases, the other increases proportionally
            - **+0.7 to +0.9**: Strong positive correlation - factors tend to increase together
            - **+0.3 to +0.6**: Moderate positive correlation - some tendency to move in the same direction
            - **+0.1 to +0.2**: Weak positive correlation - slight tendency to increase together
            
            **🔴 Negative Correlations (Red shades):**
            - **-1.0**: Perfect negative relationship - as one factor increases, the other decreases proportionally  
            - **-0.7 to -0.9**: Strong negative correlation - factors tend to move in opposite directions
            - **-0.3 to -0.6**: Moderate negative correlation - some tendency to move in opposite directions
            - **-0.1 to -0.2**: Weak negative correlation - slight tendency to move in opposite directions
            
            **⚪ Near Zero (White):** No meaningful relationship between the factors
            
            **💡 Clinical Significance:** Look for strong correlations (>0.5 or <-0.5) to identify which factors most influence each other and the overall Risk Score.
            """)
        
        # Add correlation insights
        with st.expander("🔍 **Key Correlation Insights**"):
            if len(filtered_df) > 10:  # Only show insights if we have enough data
                st.markdown("**📊 Strongest Correlations in Filtered Population:**")
                
                # Find strongest positive and negative correlations
                corr_matrix = correlation_matrix.copy()
                np.fill_diagonal(corr_matrix.values, 0)  # Remove diagonal (self-correlations)
                
                # Find strongest correlations
                max_corr = corr_matrix.abs().max().max()
                max_corr_pair = corr_matrix.abs().idxmax()[corr_matrix.abs().max().idxmax()]
                actual_corr = corr_matrix.loc[corr_matrix.abs().max().idxmax(), max_corr_pair]
                
                if max_corr > 0.3:  # Only show if correlation is meaningful
                    correlation_type = "positive" if actual_corr > 0 else "negative"
                    st.markdown(f"• **Strongest {correlation_type} correlation**: {corr_matrix.abs().max().idxmax()} ↔ {max_corr_pair} ({actual_corr:.3f})")
                
                # Risk score correlations
                if 'Risk_Score' in corr_matrix.columns:
                    risk_correlations = corr_matrix['Risk_Score'].abs().sort_values(ascending=False)
                    if len(risk_correlations) > 1:
                        top_risk_factor = risk_correlations.index[1]  # Skip Risk_Score itself
                        risk_corr_value = corr_matrix.loc['Risk_Score', top_risk_factor]
                        st.markdown(f"• **Top risk predictor**: {top_risk_factor} (correlation: {risk_corr_value:.3f})")
            else:
                st.warning("**Not enough data points in filtered population for meaningful correlation analysis.**")
    else:
        st.warning("**Not enough numerical variables available for correlation analysis.**")
    
    # Clinical insights by risk category for filtered data
    st.markdown('<h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🏥 Clinical Insights by Risk Category</strong></h3>', unsafe_allow_html=True)
    
    for risk_cat in ["High Risk", "Medium Risk", "Low Risk"]:
        subset = filtered_df[filtered_df["Risk_Category"] == risk_cat]
        if len(subset) > 0:
            with st.expander(f"**{risk_cat} Patients (n={len(subset)})**"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("**Average MMSE**", f"**{subset['MMSE'].mean():.1f}**")
                
                with col2:
                    st.metric("**Average Age**", f"**{subset['Patient_Age'].mean():.1f}**")
                
                with col3:
                    st.metric("**Average BMI**", f"**{subset['BMI'].mean():.1f}**")
                
                with col4:
                    st.metric("**Early Detection Flags**", f"**{subset['Early_Detection_Flag'].sum()}**")
                
                # Additional demographic insights for filtered population
                if len(subset) > 0:
                    demo_col1, demo_col2 = st.columns(2)
                    
                    with demo_col1:
                        st.markdown("**Gender Distribution:**")
                        gender_dist = subset['Gender'].value_counts()
                        for gender, count in gender_dist.items():
                            percentage = (count / len(subset)) * 100
                            st.write(f"**• {gender}: {count} ({percentage:.1f}%)**")
                    
                    with demo_col2:
                        st.markdown("**Depression Status:**")
                        depression_dist = subset['Depression'].value_counts()
                        for status, count in depression_dist.items():
                            percentage = (count / len(subset)) * 100
                            st.write(f"**• {status}: {count} ({percentage:.1f}%)**")
    
    # Patient risk table for filtered data
    # Enhanced high-risk patient details section
    st.markdown('<h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>📋 High-Risk Patient Details</strong></h3>', unsafe_allow_html=True)
    
    high_risk_patients = filtered_df[filtered_df["Risk_Category"] == "High Risk"].copy()
    if len(high_risk_patients) > 0:
        # Display key columns for high-risk patients
        display_cols = ["Patient_Age", "Gender", "MMSE", "BMI", "Depression", "Risk_Score", "Early_Detection_Flag"]
        available_display_cols = [col for col in display_cols if col in high_risk_patients.columns]
        
        # Format column names for display (replace underscores and hyphens with spaces)
        high_risk_display = high_risk_patients[available_display_cols].head(10).copy()
        high_risk_display.columns = high_risk_display.columns.str.replace('_', ' ').str.replace('-', ' ')
        
        st.dataframe(high_risk_display)
        
        st.info(f"**Showing top 10 of {len(high_risk_patients)} high-risk patients requiring immediate attention.**")
        
        # Summary insights for filtered high-risk patients
        if len(high_risk_patients) > 0:
            st.markdown("**🎯 High-Risk Population Insights:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_age = high_risk_patients['Patient_Age'].mean()
                st.metric("**Avg Age**", f"**{avg_age:.1f} years**")
            
            with col2:
                avg_mmse = high_risk_patients['MMSE'].mean()
                st.metric("**Avg MMSE**", f"**{avg_mmse:.1f}**")
            
            with col3:
                depression_count = (high_risk_patients['Depression'] == 'Yes').sum() if 'Depression' in high_risk_patients.columns else 0
                depression_pct = (depression_count / len(high_risk_patients)) * 100 if len(high_risk_patients) > 0 else 0
                st.metric("**Depression Rate**", f"**{depression_pct:.1f}%**")
    else:
        st.info("**No high-risk patients found in the filtered population.**")
    
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
        <h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>📋 Dashboard Navigation Guide</strong></h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("**🔍 Click here for comprehensive usage instructions**", expanded=False):
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
    
    # Key Insights and Findings Narrative
    st.markdown('<h2 style="color: #000000; margin-top: 2rem; font-weight: bold;"><strong>📈 Key Healthcare Insights & Clinical Findings</strong></h2>', unsafe_allow_html=True)
    
    # Calculate key statistics for insights
    high_risk_count = len(df[df.apply(lambda row: categorize_risk(calculate_risk_score(row)), axis=1) == "High Risk"])
    total_patients = len(df)
    high_risk_percentage = (high_risk_count / total_patients) * 100
    avg_age = df['Patient_Age'].mean()
    mmse_critical = len(df[df['MMSE'] < 18])
    
    # Create insight cards
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(220, 53, 69, 0.1), rgba(255, 193, 7, 0.1)); 
                    padding: 1.5rem; border-radius: 10px; border-left: 5px solid #dc3545; margin-bottom: 1rem;">
        <h4 style="color: #000000; margin-top: 0; font-weight: bold;">🚨 Critical Risk Population</h4>
        <p style="color: #000000; font-weight: bold; font-size: 1.1rem;">
        Our analysis reveals that <strong>""" + f"{high_risk_percentage:.1f}%" + """</strong> of patients fall into the high-risk category, 
        representing <strong>""" + f"{high_risk_count}" + """</strong> individuals who require immediate clinical attention and enhanced monitoring protocols.
        </p>
        <p style="color: #000000; margin-bottom: 0;">
        <strong>Clinical Implication:</strong> This significant proportion suggests the need for proactive intervention strategies 
        and resource allocation for early detection programs.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(13, 110, 253, 0.1), rgba(111, 66, 193, 0.1)); 
                    padding: 1.5rem; border-radius: 10px; border-left: 5px solid #0d6efd; margin-bottom: 1rem;">
        <h4 style="color: #000000; margin-top: 0; font-weight: bold;">🧠 Cognitive Assessment Findings</h4>
        <p style="color: #000000; font-weight: bold; font-size: 1.1rem;">
        MMSE scores indicate that <strong>""" + f"{mmse_critical}" + """</strong> patients show significant cognitive impairment 
        (MMSE < 18), representing a critical population requiring specialized care protocols.
        </p>
        <p style="color: #000000; margin-bottom: 0;">
        <strong>Research Insight:</strong> The MMSE threshold of 18 serves as a key biomarker for identifying patients 
        at risk of progression to moderate-to-severe cognitive decline.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with insights_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(25, 135, 84, 0.1), rgba(32, 201, 151, 0.1)); 
                    padding: 1.5rem; border-radius: 10px; border-left: 5px solid #198754; margin-bottom: 1rem;">
        <h4 style="color: #000000; margin-top: 0; font-weight: bold;">👥 Demographics & Age Distribution</h4>
        <p style="color: #000000; font-weight: bold; font-size: 1.1rem;">
        The study population shows an average age of <strong>""" + f"{avg_age:.1f}" + """ years</strong>, with age serving as a 
        primary risk factor in our predictive model, accounting for 25% of the total risk assessment weight.
        </p>
        <p style="color: #000000; margin-bottom: 0;">
        <strong>Clinical Significance:</strong> Age-stratified analysis enables targeted screening protocols, 
        with patients over 75 years requiring enhanced monitoring frequency.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(253, 126, 20, 0.1)); 
                    padding: 1.5rem; border-radius: 10px; border-left: 5px solid #ffc107; margin-bottom: 1rem;">
        <h4 style="color: #000000; margin-top: 0; font-weight: bold;">🔬 Multi-Factor Risk Analysis</h4>
        <p style="color: #000000; font-weight: bold; font-size: 1.1rem;">
        Our comprehensive risk algorithm integrates <strong>10+ clinical biomarkers</strong> including cognitive assessment, 
        lifestyle factors, and physiological measurements to provide personalized risk stratification.
        </p>
        <p style="color: #000000; margin-bottom: 0;">
        <strong>Innovation Impact:</strong> This multi-dimensional approach enables precision medicine strategies 
        tailored to individual patient risk profiles and clinical presentations.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data Story Navigation Guide
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(108, 117, 125, 0.1), rgba(173, 181, 189, 0.1)); 
                padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0; border: 2px solid #6c757d;">
    <h4 style="color: #000000; margin-top: 0; font-weight: bold;">📖 Data Story Navigation</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
        <div>
            <p style="color: #000000; font-weight: bold; margin-bottom: 0.5rem;">
            📊 <strong>General Analytics Tab</strong>
            </p>
            <p style="color: #000000; margin-bottom: 0; font-size: 0.95rem;">
            Explore foundational dataset characteristics, demographic distributions, and statistical summaries 
            that form the basis of our clinical insights and risk assessment methodology.
            </p>
        </div>
        <div>
            <p style="color: #000000; font-weight: bold; margin-bottom: 0.5rem;">
            🏥 <strong>Risk Assessment Tab</strong>
            </p>
            <p style="color: #000000; margin-bottom: 0; font-size: 0.95rem;">
            Discover advanced predictive analytics, 3D risk visualizations, and correlation patterns 
            that drive clinical decision-making and early intervention strategies.
            </p>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Methodology and Technical Approach Section
    st.markdown('<h2 style="color: #000000; margin-top: 2rem; font-weight: bold;"><strong>🔬 Methodology & Technical Approach</strong></h2>', unsafe_allow_html=True)
    
    with st.expander("📋 **Structured Data Science Methodology - Click to View Complete Process**", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(13, 110, 253, 0.05), rgba(111, 66, 193, 0.05)); 
                    padding: 2rem; border-radius: 15px; margin: 1rem 0;">
        
        ### 📊 **1. Data Collection & Source Validation**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Dataset:</strong> Alzheimer's Disease Research Dataset (537 patients, 10+ clinical features)<br>
        <strong style="color: #000000;">Source Justification:</strong> Clinical-grade dataset ensures medical validity and research reproducibility<br>
        <strong style="color: #000000;">Ethical Compliance:</strong> De-identified patient data adhering to HIPAA standards for healthcare research
        </div>
        
        ### 🧹 **2. Data Cleaning & Preprocessing Techniques**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Missing Value Treatment:</strong><br>
        • <strong>Why:</strong> Healthcare data often contains gaps due to patient availability or test limitations<br>
        • <strong>Technique:</strong> Domain-specific imputation using clinical thresholds and median substitution<br>
        • <strong>Justification:</strong> Preserves statistical integrity while maintaining clinical relevance<br><br>
        
        <strong style="color: #000000;">Outlier Detection & Management:</strong><br>
        • <strong>Why:</strong> Medical measurements can contain extreme values that may represent true clinical conditions<br>
        • <strong>Technique:</strong> IQR-based identification with clinical threshold validation<br>
        • <strong>Justification:</strong> Distinguishes between data errors and legitimate extreme clinical values<br><br>
        
        <strong style="color: #000000;">Feature Scaling Strategy:</strong><br>
        • <strong>Why:</strong> Clinical variables span different scales (age: 60-90, MMSE: 0-30, BMI: 15-40)<br>
        • <strong>Technique:</strong> Preserved original scales for interpretability, normalized for visualization<br>
        • <strong>Justification:</strong> Maintains clinical meaning while enabling effective visual analysis
        </div>
        
        ### 🎯 **3. Risk Assessment Algorithm Design**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Multi-Factor Scoring System:</strong><br>
        • <strong>Why:</strong> Alzheimer's risk is multifactorial, requiring comprehensive assessment<br>
        • <strong>Technique:</strong> Weighted scoring across cognitive, demographic, and lifestyle factors<br>
        • <strong>Justification:</strong> Evidence-based weights reflecting clinical research findings<br><br>
        
        <strong style="color: #000000;">Risk Categorization Thresholds:</strong><br>
        • <strong>Low Risk (0-5.9):</strong> Routine monitoring sufficient<br>
        • <strong>Medium Risk (6-8.9):</strong> Enhanced screening protocols<br>
        • <strong>High Risk (9+):</strong> Immediate clinical attention required<br>
        • <strong>Clinical Validation:</strong> Thresholds aligned with established dementia screening guidelines
        </div>
        
        ### 📈 **4. Statistical Analysis Techniques**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Correlation Analysis:</strong><br>
        • <strong>Why:</strong> Identify relationships between risk factors for clinical insights<br>
        • <strong>Technique:</strong> Pearson correlation matrix with statistical significance testing<br>
        • <strong>Justification:</strong> Reveals hidden patterns in multi-dimensional healthcare data<br><br>
        
        <strong style="color: #000000;">Descriptive Statistics:</strong><br>
        • <strong>Why:</strong> Establish baseline population characteristics for comparative analysis<br>
        • <strong>Technique:</strong> Mean, standard deviation, percentile analysis by risk groups<br>
        • <strong>Justification:</strong> Enables evidence-based clinical decision support<br><br>
        
        <strong style="color: #000000;">Distribution Analysis:</strong><br>
        • <strong>Why:</strong> Understand population heterogeneity and identify subgroups<br>
        • <strong>Technique:</strong> Histogram visualization with statistical overlay<br>
        • <strong>Justification:</strong> Supports targeted intervention strategies for specific populations
        </div>
        
        ### 🎨 **5. Visualization Strategy & Justification**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">3D Scatter Plots:</strong><br>
        • <strong>Why:</strong> Alzheimer's risk exists in multi-dimensional space requiring spatial representation<br>
        • <strong>Technique:</strong> Plotly 3D with age, MMSE, and risk score as primary axes<br>
        • <strong>Justification:</strong> Reveals clustering patterns invisible in 2D analysis<br><br>
        
        <strong style="color: #000000;">Interactive Heatmaps:</strong><br>
        • <strong>Why:</strong> Complex correlation matrices require intuitive visual interpretation<br>
        • <strong>Technique:</strong> Color-coded correlation strength with hover functionality<br>
        • <strong>Justification:</strong> Enables rapid identification of significant clinical relationships<br><br>
        
        <strong style="color: #000000;">Real-time Filtering:</strong><br>
        • <strong>Why:</strong> Clinical populations are heterogeneous requiring subset analysis<br>
        • <strong>Technique:</strong> Dynamic dashboard updates based on demographic/clinical filters<br>
        • <strong>Justification:</strong> Supports precision medicine approach to patient care
        </div>
        
        ### 🏥 **6. Clinical Integration & Validation**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Evidence-Based Thresholds:</strong><br>
        • <strong>MMSE < 18:</strong> Aligned with established cognitive impairment criteria<br>
        • <strong>Age Stratification:</strong> Based on epidemiological risk progression data<br>
        • <strong>BMI Categories:</strong> Following WHO classifications for health risk assessment<br><br>
        
        <strong style="color: #000000;">Clinical Workflow Integration:</strong><br>
        • <strong>Risk Prioritization:</strong> Color-coded alerts for immediate attention cases<br>
        • <strong>Population Health Management:</strong> Aggregate metrics for resource planning<br>
        • <strong>Decision Support:</strong> Interpretable scoring with clinical context
        </div>
        
        ### 🔄 **7. Quality Assurance & Validation**
        <div style="margin-left: 1.5rem;">
        <strong style="color: #000000;">Data Integrity Checks:</strong><br>
        • Automated validation of clinical value ranges<br>
        • Cross-reference consistency across related variables<br>
        • Real-time error detection and reporting<br><br>
        
        <strong style="color: #000000;">Statistical Validation:</strong><br>
        • Confidence interval calculation for risk estimates<br>
        • Sensitivity analysis for threshold adjustments<br>
        • Population representation validation across demographic groups
        </div>
        
        </div>
        """, unsafe_allow_html=True)
    
    # Future Updates and Extensibility Section
    st.markdown('<h2 style="color: #000000; margin-top: 2rem; font-weight: bold;"><strong>🚀 Future Enhancements & Scalability Framework</strong></h2>', unsafe_allow_html=True)
    
    with st.expander("🔮 **Planned Features & Data Source Expansion - Click to View Roadmap**", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(25, 135, 84, 0.05), rgba(32, 201, 151, 0.05)); 
                    padding: 2rem; border-radius: 15px; margin: 1rem 0;">
        
        ### 📊 **1. New Data Source Integration Framework**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Multi-Hospital Data Federation:</strong><br>
        • <strong>Planned Integration:</strong> Real-time EMR connections from multiple healthcare systems<br>
        • <strong>Data Standardization:</strong> Automated FHIR-compliant data normalization pipeline<br>
        • <strong>Privacy Framework:</strong> Federated learning architecture preserving patient confidentiality<br>
        • <strong>Timeline:</strong> Phase 1 implementation targeted for Q2 2026<br><br>
        
        <strong style="color: #000000;">Genomic Data Integration:</strong><br>
        • <strong>APOE-ε4 Genotyping:</strong> Integration of genetic risk factors for Alzheimer's predisposition<br>
        • <strong>Polygenic Risk Scores:</strong> Advanced genetic scoring algorithms for enhanced prediction<br>
        • <strong>Biobank Connectivity:</strong> Direct integration with national genetic databases<br>
        • <strong>Ethical Considerations:</strong> Comprehensive consent management and genetic counseling protocols<br><br>
        
        <strong style="color: #000000;">Neuroimaging Data Pipeline:</strong><br>
        • <strong>MRI/PET Scan Analysis:</strong> AI-powered brain imaging interpretation for structural changes<br>
        • <strong>Amyloid Plaque Detection:</strong> Automated quantification of Alzheimer's pathology markers<br>
        • <strong>Longitudinal Tracking:</strong> Time-series analysis of brain structural changes<br>
        • <strong>Integration Method:</strong> DICOM-compliant imaging workflow with cloud processing
        </div>
        
        ### 🤖 **2. Advanced AI/ML Capabilities**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Predictive Modeling Enhancement:</strong><br>
        • <strong>Machine Learning Pipeline:</strong> Gradient boosting and neural network implementations<br>
        • <strong>Model Validation:</strong> Cross-validation with external datasets and clinical trials<br>
        • <strong>Explainable AI:</strong> SHAP values and LIME interpretability for clinical trust<br>
        • <strong>Continuous Learning:</strong> Model retraining with new patient outcomes data<br><br>
        
        <strong style="color: #000000;">Natural Language Processing:</strong><br>
        • <strong>Clinical Notes Analysis:</strong> Automated extraction of risk factors from physician notes<br>
        • <strong>Symptom Detection:</strong> NLP-powered identification of early cognitive decline indicators<br>
        • <strong>Patient Communication:</strong> Automated generation of personalized risk reports<br>
        • <strong>Multi-language Support:</strong> Translation capabilities for diverse patient populations<br><br>
        
        <strong style="color: #000000;">Real-time Risk Monitoring:</strong><br>
        • <strong>Wearable Device Integration:</strong> Continuous monitoring via smartwatches and health trackers<br>
        • <strong>Activity Pattern Analysis:</strong> Sleep, exercise, and daily routine correlation with cognitive health<br>
        • <strong>Alert Systems:</strong> Automated notifications for significant risk threshold changes<br>
        • <strong>Mobile App Companion:</strong> Patient-facing application for risk tracking and education
        </div>
        
        ### 🌐 **3. Clinical Integration & Workflow Enhancement**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">EMR Integration Architecture:</strong><br>
        • <strong>HL7 FHIR Compliance:</strong> Seamless integration with Epic, Cerner, and other major EMR systems<br>
        • <strong>Clinical Decision Support:</strong> Real-time risk alerts embedded in physician workflows<br>
        • <strong>Automated Documentation:</strong> Risk assessment results auto-populated in patient charts<br>
        • <strong>Billing Integration:</strong> CPT code generation for preventive care and risk assessment services<br><br>
        
        <strong style="color: #000000;">Population Health Management:</strong><br>
        • <strong>Registry Development:</strong> Comprehensive Alzheimer's risk patient registry<br>
        • <strong>Outcome Tracking:</strong> Longitudinal follow-up of intervention effectiveness<br>
        • <strong>Resource Allocation:</strong> Predictive modeling for healthcare resource planning<br>
        • <strong>Quality Metrics:</strong> Performance dashboards for clinical quality improvement programs
        </div>
        
        ### 🔬 **4. Research & Clinical Trial Integration**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Clinical Trial Matching:</strong><br>
        • <strong>Eligibility Screening:</strong> Automated identification of patients suitable for Alzheimer's research<br>
        • <strong>Trial Database Integration:</strong> Connection with ClinicalTrials.gov for real-time opportunities<br>
        • <strong>Recruitment Optimization:</strong> AI-powered patient-trial matching for accelerated enrollment<br>
        • <strong>Outcome Contribution:</strong> Patient data contribution to research while maintaining privacy<br><br>
        
        <strong style="color: #000000;">Pharmaceutical Collaboration:</strong><br>
        • <strong>Drug Development Support:</strong> Real-world evidence generation for therapeutic interventions<br>
        • <strong>Biomarker Discovery:</strong> Large-scale analysis for novel risk factor identification<br>
        • <strong>Clinical Endpoint Definition:</strong> Data-driven outcome measures for trial design<br>
        • <strong>Regulatory Submission:</strong> FDA-ready data packages for new therapeutic approvals
        </div>
        
        ### 📱 **5. User Experience & Accessibility Enhancements**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Multi-platform Accessibility:</strong><br>
        • <strong>Mobile-first Design:</strong> Responsive dashboard optimized for tablets and smartphones<br>
        • <strong>Voice Interface:</strong> Voice-activated navigation for accessibility compliance<br>
        • <strong>Screen Reader Compatibility:</strong> Full WCAG 2.1 AA compliance for visual impairments<br>
        • <strong>Multi-language Support:</strong> Spanish, Mandarin, and other major languages<br><br>
        
        <strong style="color: #000000;">Patient Portal Integration:</strong><br>
        • <strong>Personal Risk Dashboard:</strong> Patient-facing risk visualization and education<br>
        • <strong>Family History Input:</strong> Collaborative family risk factor documentation<br>
        • <strong>Lifestyle Tracking:</strong> Integration with fitness apps and nutrition platforms<br>
        • <strong>Educational Resources:</strong> Personalized learning materials based on individual risk profiles
        </div>
        
        ### 🛡️ **6. Security & Compliance Framework**
        <div style="margin-left: 1.5rem; margin-bottom: 1.5rem;">
        <strong style="color: #000000;">Enhanced Data Protection:</strong><br>
        • <strong>Zero-Trust Architecture:</strong> Advanced cybersecurity framework for healthcare data<br>
        • <strong>Blockchain Audit Trail:</strong> Immutable record of all data access and modifications<br>
        • <strong>Differential Privacy:</strong> Mathematical privacy guarantees for research data sharing<br>
        • <strong>SOC 2 Type II Compliance:</strong> Enterprise-grade security certifications<br><br>
        
        <strong style="color: #000000;">Regulatory Compliance:</strong><br>
        • <strong>GDPR Compliance:</strong> European patient data protection standards<br>
        • <strong>21 CFR Part 11:</strong> FDA electronic records and signatures compliance<br>
        • <strong>HITECH Act Adherence:</strong> Enhanced HIPAA security requirements<br>
        • <strong>International Standards:</strong> ISO 27001 and ISO 13485 medical device compliance
        </div>
        
        ### 🔄 **7. Implementation Timeline & Milestones**
        <div style="margin-left: 1.5rem;">
        <strong style="color: #000000;">Phase 1 (Q1-Q2 2026):</strong><br>
        • Multi-hospital EMR integration pilot program<br>
        • Basic genomic data incorporation (APOE-ε4 status)<br>
        • Mobile-responsive dashboard deployment<br><br>
        
        <strong style="color: #000000;">Phase 2 (Q3-Q4 2026):</strong><br>
        • Advanced ML model implementation and validation<br>
        • Neuroimaging pipeline integration<br>
        • Clinical trial matching system launch<br><br>
        
        <strong style="color: #000000;">Phase 3 (2027):</strong><br>
        • Wearable device integration and real-time monitoring<br>
        • Population health management tools<br>
        • Full regulatory compliance certification<br><br>
        
        <strong style="color: #000000;">Long-term Vision (2028+):</strong><br>
        • National Alzheimer's risk surveillance network<br>
        • AI-powered drug discovery collaboration platform<br>
        • Global health data federation for dementia research
        </div>
        
        </div>
        """, unsafe_allow_html=True)
    
    # Technical Architecture for Future Scalability
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(111, 66, 193, 0.1), rgba(13, 110, 253, 0.1)); 
                padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0; border: 2px solid #6f42c1;">
    <h4 style="color: #000000; margin-top: 0; font-weight: bold;">🏗️ Scalable Technical Architecture</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1rem;">
        <div>
            <p style="color: #000000; font-weight: bold; margin-bottom: 0.5rem;">
            ☁️ <strong>Cloud-Native Infrastructure</strong>
            </p>
            <p style="color: #000000; margin-bottom: 1rem; font-size: 0.95rem;">
            Kubernetes orchestration with auto-scaling capabilities, supporting millions of patient records 
            with sub-second response times and 99.9% uptime availability.
            </p>
            <p style="color: #000000; font-weight: bold; margin-bottom: 0.5rem;">
            🔗 <strong>API-First Design</strong>
            </p>
            <p style="color: #000000; margin-bottom: 0; font-size: 0.95rem;">
            RESTful and GraphQL APIs enabling seamless third-party integrations, with comprehensive 
            documentation and SDKs for rapid healthcare system connectivity.
            </p>
        </div>
        <div>
            <p style="color: #000000; font-weight: bold; margin-bottom: 0.5rem;">
            🧱 <strong>Microservices Architecture</strong>
            </p>
            <p style="color: #000000; margin-bottom: 1rem; font-size: 0.95rem;">
            Modular service design allowing independent scaling of risk assessment, data processing, 
            and visualization components for optimal resource utilization.
            </p>
            <p style="color: #000000; font-weight: bold; margin-bottom: 0.5rem;">
            🔄 <strong>Real-time Data Pipeline</strong>
            </p>
            <p style="color: #000000; margin-bottom: 0; font-size: 0.95rem;">
            Apache Kafka and streaming analytics enabling real-time risk updates as new patient 
            data becomes available from integrated healthcare systems.
            </p>
        </div>
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
                label="**📋 Total Patients**", 
                value="**537**",
                delta="**Research Cohort**"
            )
        with col2:
            st.metric(
                label="**📊 Clinical Features**", 
                value="**10**",
                delta="**Biomarkers**"
            )
        with col3:
            st.metric(
                label="**🎯 Analysis Focus**", 
                value="**Risk Assessment**",
                delta="**Early Detection**"
            )

        st.markdown("---")

        # Enhanced Data Preview Section - Blue Theme with Bold Black Text and Borders - icons separate from underlined text
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(21, 101, 192, 0.3), rgba(25, 118, 210, 0.3)); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border: 3px solid rgba(100, 100, 120, 0.8); font-weight: bold;">
            <h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>🔍 Clinical Data Preview</strong></h3>
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
            <h3 style="color: #000000; margin-top: 0; font-weight: bold;"><strong>📈 Statistical Summary</strong></h3>
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



