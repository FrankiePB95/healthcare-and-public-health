import streamlit as st


def page_summary_body():
    """
    Contents of the Project Summary page
    """
    st.header("Project Summary")
    
    st.write("### Project Overview")
    st.info(
        "This Healthcare and Public Health Analytics project aims to provide "
        "insights into health data patterns and trends."
    )
    
    st.write("### Key Features")
    st.write("""
    - **Data Exploration**: Interactive visualizations of health data
    - **Statistical Analysis**: Comprehensive statistical insights
    - **Machine Learning**: Predictive modeling for health outcomes
    - **Dashboard**: Real-time monitoring and reporting
    """)
    
    st.write("### Technology Stack")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Frontend:**")
        st.write("- Streamlit")
        st.write("- Plotly")
        st.write("- Matplotlib/Seaborn")
        
    with col2:
        st.write("**Backend/ML:**")
        st.write("- Pandas")
        st.write("- Scikit-learn")
        st.write("- XGBoost")
        st.write("- NumPy")
    
    st.write("### Getting Started")
    st.write("""
    1. Navigate through the different pages using the sidebar
    2. Upload your healthcare data for analysis
    3. Explore visualizations and insights
    4. Generate reports and predictions
    """)