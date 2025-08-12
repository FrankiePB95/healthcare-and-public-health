# Import streamlit libray and multipage class
import streamlit as st
from app_pages.multi_page import MultiPage
from app_pages.shared_styles import apply_shared_css

# Import your page functions here
from app_pages.page_summary import page_summary_body
from app_pages.dashboard import dashboard_body

# Configure the Streamlit page with enhanced session management
st.set_page_config(
    page_title="Healthcare and Public Health Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for enhanced page persistence
if "app_initialized" not in st.session_state:
    st.session_state.app_initialized = True
    # Check for URL parameters to restore page state
    query_params = st.query_params
    if "page" in query_params:
        try:
            # st.query_params returns strings directly, not lists
            page_index = int(query_params["page"])
            if 0 <= page_index < 4:  # We have 4 pages total
                st.session_state.current_page_index = page_index
        except (ValueError, TypeError):
            pass  # Use default if invalid parameter

# Create instance of the app
app = MultiPage()

# Create functions for the generation of a home page and a conclusion page
def home_page():
    apply_shared_css()
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #000000; font-size: 3rem; margin-bottom: 0.5rem; font-weight: 900;">🏥 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 3px;">Healthcare Analytics Platform</span></h1>
        <p style="font-size: 1.2rem; color: #000000; margin-top: 0; font-weight: bold;">
            Advanced Alzheimer's Disease Research & Clinical Decision Support
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create custom styled container using columns
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col2:
        # Use Streamlit container with simplified HTML structure
        with st.container():
            st.markdown("""
            <div class="custom-card">
                <h3 style="color: #000000; font-weight: bold;">🎯 Welcome to the Healthcare Analytics Dashboard</h3>
                <p style="color: #000000; font-weight: bold;">This comprehensive platform provides advanced analytics and insights for healthcare professionals and researchers working in the field of Alzheimer's disease and cognitive health.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #000000; font-weight: bold;">🔍 Key Features:</h4>
                <p style="color: #000000; font-weight: bold;">
                • <strong>Risk Assessment Tools:</strong> Multi-factor scoring algorithms for early detection<br>
                • <strong>Interactive Visualizations:</strong> 3D charts and comprehensive statistical analysis<br>
                • <strong>Clinical Insights:</strong> Evidence-based recommendations and patient monitoring<br>
                • <strong>Data Analytics:</strong> Advanced statistical testing and machine learning integration
                </p>
                <p style="color: #000000; font-weight: bold;"><strong>Navigate using the sidebar to explore different sections of the dashboard.</strong></p>
            </div>
            """, unsafe_allow_html=True)

def conclusion_page():
    apply_shared_css()
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #000000; font-size: 3rem; margin-bottom: 0.5rem; font-weight: 900;">📋 <span style="text-decoration: underline; text-decoration-color: #000000; text-decoration-thickness: 3px;">Project Conclusion</span></h1>
        <p style="font-size: 1.2rem; color: #000000; margin-top: 0; font-weight: bold;">
            Healthcare Analytics Outcomes & Future Directions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create custom styled container using columns
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col2:
        # Use Streamlit container with simplified HTML structure
        with st.container():
            st.markdown("""
            <div class="custom-card">
                <h3 style="color: #000000; font-weight: bold;">📊 Project Achievements</h3>
                <p style="color: #000000; font-weight: bold;">This healthcare analytics project has successfully demonstrated the power of data-driven approaches in understanding and predicting Alzheimer's disease risk factors.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #000000; font-weight: bold;">🔬 Key Findings:</h4>
                <p style="color: #000000; font-weight: bold;">
                • <strong>Statistical Analysis:</strong> Comprehensive normality testing and correlation analysis revealed significant patterns<br>
                • <strong>Risk Assessment:</strong> Developed multi-factor scoring system for early detection<br>
                • <strong>Data Insights:</strong> Identified critical health metrics for patient monitoring<br>
                • <strong>Visualization Impact:</strong> Created interactive tools for clinical decision support
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #000000; font-weight: bold;">🚀 Future Applications:</h4>
                <p style="color: #000000; font-weight: bold;">
                • <strong>Clinical Integration:</strong> Implementation in healthcare systems for patient screening<br>
                • <strong>Research Expansion:</strong> Extension to other neurodegenerative conditions<br>
                • <strong>Machine Learning:</strong> Advanced predictive modeling for personalized medicine
                </p>
            </div>
            """, unsafe_allow_html=True)
   
# Add your app pages here
app.add_page("Home", home_page)
app.add_page("Project Summary", page_summary_body)
app.add_page("Alzheimer's Disease Dashboard", dashboard_body)
app.add_page("Conclusion", conclusion_page)

# Run the app
app.run()
