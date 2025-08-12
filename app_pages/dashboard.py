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
            gender_options = ['All'] + sorted(df['Gender'].unique().tolist())
            selected_gender = st.selectbox("👤 Gender", gender_options, help="Filter by patient gender")
        
        with demo_col2:
            # Ethnicity filter  
            ethnicity_options = ['All'] + sorted(df['Ethnicity'].unique().tolist())
            selected_ethnicity = st.selectbox("🌍 Ethnicity", ethnicity_options, help="Filter by ethnic background")
        
        with demo_col3:
            # Age range filter
            age_min, age_max = int(df['Patient_Age'].min()), int(df['Patient_Age'].max())
            age_range = st.slider("📅 Age Range", age_min, age_max, (age_min, age_max), 
                                help=f"Age ranges from {age_min} to {age_max} years")
    
    with st.expander("🏥 **Medical History Filters**", expanded=False):
        med_col1, med_col2, med_col3 = st.columns(3)
        
        with med_col1:
            # Cardiovascular Disease filter
            cvd_options = ['All'] + sorted(df['Cardiovascular_Disease'].unique().tolist()) if 'Cardiovascular_Disease' in df.columns else ['All']
            selected_cvd = st.selectbox("❤️ Cardiovascular Disease", cvd_options, help="Filter by cardiovascular disease status")
            
            # Depression filter
            depression_options = ['All'] + sorted(df['Depression'].unique().tolist())
            selected_depression = st.selectbox("🧠 Depression", depression_options, help="Filter by depression status")
        
        with med_col2:
            # Memory Complaints filter
            memory_options = ['All'] + sorted(df['Memory_Complaints'].unique().tolist()) if 'Memory_Complaints' in df.columns else ['All']
            selected_memory = st.selectbox("🧩 Memory Complaints", memory_options, help="Filter by memory complaint status")
            
            # Behavioral Problems filter
            behavior_options = ['All'] + sorted(df['Behavioral_Problems'].unique().tolist()) if 'Behavioral_Problems' in df.columns else ['All']
            selected_behavior = st.selectbox("😤 Behavioral Problems", behavior_options, help="Filter by behavioral issues")
        
        with med_col3:
            # Personality Changes filter
            personality_options = ['All'] + sorted(df['Personality_Changes'].unique().tolist()) if 'Personality_Changes' in df.columns else ['All']
            selected_personality = st.selectbox("👤 Personality Changes", personality_options, help="Filter by personality changes")
            
            # Difficulty Completing Tasks filter
            tasks_options = ['All'] + sorted(df['Difficulty_Completing_Tasks'].unique().tolist()) if 'Difficulty_Completing_Tasks' in df.columns else ['All']
            selected_tasks = st.selectbox("📝 Task Difficulty", tasks_options, help="Filter by difficulty completing tasks")
    
    with st.expander("💊 **Lifestyle & Health Metrics**", expanded=False):
        lifestyle_col1, lifestyle_col2, lifestyle_col3 = st.columns(3)
        
        with lifestyle_col1:
            # Smoking filter
            smoking_options = ['All'] + sorted(df['Smoking'].unique().tolist())
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
                selected_diagnosis = 'All'
    
    # Apply filters to the dataframe
    filtered_df = df.copy()
    
    # Demographic filters
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    if selected_ethnicity != 'All':
        filtered_df = filtered_df[filtered_df['Ethnicity'] == selected_ethnicity]
    
    filtered_df = filtered_df[
        (filtered_df['Patient_Age'] >= age_range[0]) & 
        (filtered_df['Patient_Age'] <= age_range[1])
    ]
    
    # Medical history filters
    if selected_cvd != 'All' and 'Cardiovascular_Disease' in df.columns:
        filtered_df = filtered_df[filtered_df['Cardiovascular_Disease'] == selected_cvd]
    
    if selected_depression != 'All':
        filtered_df = filtered_df[filtered_df['Depression'] == selected_depression]
    
    if selected_memory != 'All' and 'Memory_Complaints' in df.columns:
        filtered_df = filtered_df[filtered_df['Memory_Complaints'] == selected_memory]
    
    if selected_behavior != 'All' and 'Behavioral_Problems' in df.columns:
        filtered_df = filtered_df[filtered_df['Behavioral_Problems'] == selected_behavior]
    
    if selected_personality != 'All' and 'Personality_Changes' in df.columns:
        filtered_df = filtered_df[filtered_df['Personality_Changes'] == selected_personality]
    
    if selected_tasks != 'All' and 'Difficulty_Completing_Tasks' in df.columns:
        filtered_df = filtered_df[filtered_df['Difficulty_Completing_Tasks'] == selected_tasks]
    
    # Lifestyle filters
    if selected_smoking != 'All':
        filtered_df = filtered_df[filtered_df['Smoking'] == selected_smoking]
    
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
    
    if selected_diagnosis != 'All' and 'Diagnosis' in df.columns:
        filtered_df = filtered_df[filtered_df['Diagnosis'] == selected_diagnosis]
    
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
        if selected_gender != 'All': active_filters.append(f"👤 Gender: {selected_gender}")
        if selected_ethnicity != 'All': active_filters.append(f"🌍 Ethnicity: {selected_ethnicity}")
        if selected_depression != 'All': active_filters.append(f"🧠 Depression: {selected_depression}")
        if selected_cvd != 'All': active_filters.append(f"❤️ CVD: {selected_cvd}")
        if selected_smoking != 'All': active_filters.append(f"🚬 Smoking: {selected_smoking}")
        if selected_memory != 'All' and 'Memory_Complaints' in df.columns: active_filters.append(f"🧩 Memory: {selected_memory}")
        if selected_behavior != 'All' and 'Behavioral_Problems' in df.columns: active_filters.append(f"😤 Behavior: {selected_behavior}")
        if selected_personality != 'All' and 'Personality_Changes' in df.columns: active_filters.append(f"👤 Personality: {selected_personality}")
        if selected_tasks != 'All' and 'Difficulty_Completing_Tasks' in df.columns: active_filters.append(f"📝 Tasks: {selected_tasks}")
        if selected_diagnosis != 'All': active_filters.append(f"🩺 Diagnosis: {selected_diagnosis}")
        
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



