import streamlit as st
from app_pages.shared_styles import apply_shared_css


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
    
    st.header("📋 Project Overview")
    
    # Custom info card for project overview
    st.markdown("""
    <div style="background: rgba(52, 98, 171, 0.85); padding: 1.5rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); margin: 1rem 0; border: 3px solid rgba(100, 100, 120, 0.8); font-weight: bold;">
        <h3 style="color: #000000; font-weight: bold;"><strong>🎯 Mission Statement</strong></h3>
        <p style="color: #000000; font-weight: bold;">This Healthcare and Public Health Analytics project aims to provide 
        comprehensive insights into health data patterns and trends, specifically 
        focusing on Alzheimer's disease risk assessment and early detection.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #000000; font-weight: bold;"><strong>🔑 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Key Features</span></strong></h3>', unsafe_allow_html=True)
    
    # Use a single container with inline styling - most reliable approach
    with st.container():
        st.markdown("""
        <div style="background: rgba(52, 98, 171, 0.85); padding: 1.5rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); margin: 1rem 0; border: 3px solid rgba(100, 100, 120, 0.8); color: white;">
            <h4 style="color: white; margin-top: 0; font-weight: bold;"><strong>🔍 Data Exploration</strong></h4>
            <p style="color: white;">Interactive visualizations of health data with advanced statistical analysis</p>
            <h4 style="color: white; font-weight: bold;"><strong>📈 Statistical Analysis</strong></h4>
            <p style="color: white;">Comprehensive statistical insights including normality tests, t-tests, and correlation analysis</p>
            <h4 style="color: white; font-weight: bold;"><strong>🤖 Machine Learning</strong></h4>
            <p style="color: white;">Predictive modeling for health outcomes with risk assessment algorithms</p>
            <h4 style="color: white; font-weight: bold;"><strong>📊 Interactive Dashboard</strong></h4>
            <p style="color: white;">Real-time monitoring and reporting with 3D visualizations and clinical insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #000000; font-weight: bold;"><strong>💻 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Technology Stack</span></strong></h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(52, 98, 171, 0.85); padding: 1.5rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); margin: 1rem 0; border: 3px solid rgba(100, 100, 120, 0.8); font-weight: bold;">
            <h4 style="color: #000000; font-weight: bold;"><strong>🎨 Frontend Technologies</strong></h4>
            <ul style="color: #000000; font-weight: bold;">
                <li><strong>Streamlit</strong> - Interactive web application framework</li>
                <li><strong>Plotly</strong> - Interactive 3D visualizations</li>
                <li><strong>Matplotlib/Seaborn</strong> - Statistical plotting and analysis</li>
                <li><strong>Custom CSS</strong> - Professional healthcare-themed styling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background: rgba(52, 98, 171, 0.85); padding: 1.5rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); margin: 1rem 0; border: 3px solid rgba(100, 100, 120, 0.8); font-weight: bold;">
            <h4 style="color: #000000; font-weight: bold;"><strong>⚙️ Backend & Analytics</strong></h4>
            <ul style="color: #000000; font-weight: bold;">
                <li><strong>Pandas</strong> - Data manipulation and analysis</li>
                <li><strong>Scikit-learn</strong> - Machine learning algorithms</li>
                <li><strong>NumPy</strong> - Numerical computing</li>
                <li><strong>SciPy</strong> - Statistical testing and analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #000000; font-weight: bold;"><strong>🚀 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 2px;">Getting Started</span></strong></h3>', unsafe_allow_html=True)
    
    # Use Streamlit columns with colored backgrounds
    col1, col2 = st.columns(2)
    
    with col1:
        # Create a styled container using CSS classes
        st.markdown("""
        <style>
        .blue-box {
            background-color: rgba(52, 98, 171, 0.85);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            color: black;
        }
        .blue-box h4 {
            color: black !important;
            margin-top: 0;
            font-weight: bold;
        }
        .blue-box p, .blue-box li {
            color: black !important;
        }
        </style>
        
        <div class="blue-box">
            <h4><strong>📚 How to Use This Application</strong></h4>
            <ol>
                <li>Navigate through different pages using the sidebar menu</li>
                <li>Explore the interactive dashboard with risk assessment tools</li>
                <li>Analyze statistical insights and visualizations</li>
                <li>Review comprehensive data analysis in the Jupyter notebook</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="blue-box">
            <h4><strong>🏥 Clinical Applications</strong></h4>
            <ul>
                <li><strong>Risk Assessment:</strong> Multi-factor scoring for Alzheimer's disease</li>
                <li><strong>Early Detection:</strong> Advanced warning systems for at-risk patients</li>
                <li><strong>Patient Monitoring:</strong> Real-time tracking of health metrics</li>
                <li><strong>Clinical Insights:</strong> Data-driven recommendations for healthcare professionals</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
