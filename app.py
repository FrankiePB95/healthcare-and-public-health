import streamlit as st
from app_pages.multi_page import MultiPage

# Import your page functions here
from app_pages.page_summary import page_summary_body
from app_pages.dashboard import dashboard_body
# from app_pages.pages.page_data_exploration import page_data_exploration_body
# from app_pages.pages.page_analysis import page_analysis_body

# Configure the Streamlit page
st.set_page_config(
    page_title="Healthcare and Public Health Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create instance of the app
app = MultiPage(app_name="Dashboard App")

# Title of the main page
st.title("Healthcare and Public Health Analytics")
st.write("Navigate using the sidebar to explore different sections of the dashboard.")

# Add your app pages here
app.add_page("Project Summary", page_summary_body)
app.add_page("Alzheimer's Disease", dashboard_body)
# app.add_page("Data Exploration", page_data_exploration_body)
# app.add_page("Analysis Results", page_analysis_body)

# For demonstration, let's add a simple home page
def home_page():
    st.header("Welcome to the Healthcare Analytics Dashboard")
    st.write("This is the home page of your healthcare and public health analytics application.")
    st.info("Add your page functions and uncomment the app.add_page() calls above to enable navigation.")

app.add_page("Home", home_page)






# Run the app
app.run()
