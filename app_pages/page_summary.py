import streamlit     st.header("📋 Project Overview")
    
    # Custom info card for project overview
    st.markdown("""
    <div class="custom-card">
        <h3>🎯 Mission Statement</h3>
        <p>This Healthcare and Public Health Analytics project aims to provide 
        comprehensive insights into health data patterns and trends, specifically 
        focusing on Alzheimer's disease risk assessment and early detection.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 🔑 Key Features")
    st.markdown("""
    <div class="custom-card">
        <h4><strong>🔍 Data Exploration</strong></h4>
        <p>Interactive visualizations of health data with advanced statistical analysis</p>
        
        <h4><strong>📈 Statistical Analysis</strong></h4>
        <p>Comprehensive statistical insights including normality tests, t-tests, and correlation analysis</p>
        
        <h4><strong>🤖 Machine Learning</strong></h4>
        <p>Predictive modeling for health outcomes with risk assessment algorithms</p>
        
        <h4><strong>📊 Interactive Dashboard</strong></h4>
        <p>Real-time monitoring and reporting with 3D visualizations and clinical insights</p>
    </div>
    """, unsafe_allow_html=True)_pages.shared_styles import apply_shared_css


def page_summary_body():
    # Apply consistent styling across all pages
    apply_shared_css()
    
    # Enhanced title with styling consistent with dashboard
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #000000; font-size: 3rem; margin-bottom: 0.5rem; font-weight: 900;">📊 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 3px;">Project Summary</span></h1>
        <p style="font-size: 1.2rem; color: #000000; margin-top: 0; font-weight: bold;">
            Healthcare Analytics & Alzheimer's Disease Research Overview
        </p>
    </div>
    """, unsafe_allow_html=True)
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
    
    st.write("### 💻 Technology Stack")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4><strong>🎨 Frontend Technologies</strong></h4>
            <ul>
                <li><strong>Streamlit</strong> - Interactive web application framework</li>
                <li><strong>Plotly</strong> - Interactive 3D visualizations</li>
                <li><strong>Matplotlib/Seaborn</strong> - Statistical plotting and analysis</li>
                <li><strong>Custom CSS</strong> - Professional healthcare-themed styling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4><strong>⚙️ Backend & Analytics</strong></h4>
            <ul>
                <li><strong>Pandas</strong> - Data manipulation and analysis</li>
                <li><strong>Scikit-learn</strong> - Machine learning algorithms</li>
                <li><strong>NumPy</strong> - Numerical computing</li>
                <li><strong>SciPy</strong> - Statistical testing and analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### 🚀 Getting Started")
    st.markdown("""
    <div class="custom-card">
        <h4><strong>📚 How to Use This Application</strong></h4>
        <ol>
            <li><strong>Navigate</strong> through different pages using the sidebar menu</li>
            <li><strong>Explore</strong> the interactive dashboard with risk assessment tools</li>
            <li><strong>Analyze</strong> statistical insights and visualizations</li>
            <li><strong>Review</strong> comprehensive data analysis in the Jupyter notebook</li>
        </ol>
        
        <h4><strong>🏥 Clinical Applications</strong></h4>
        <ul>
            <li><strong>Risk Assessment:</strong> Multi-factor scoring for Alzheimer's disease</li>
            <li><strong>Early Detection:</strong> Advanced warning systems for at-risk patients</li>
            <li><strong>Patient Monitoring:</strong> Real-time tracking of health metrics</li>
            <li><strong>Clinical Insights:</strong> Data-driven recommendations for healthcare professionals</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)