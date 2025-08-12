import streamlit as st
from app_pages.shared_styles import apply_shared_css


class MultiPage:
    """
    Framework for combining multiple streamlit applications.
    """

    def __init__(self) -> None:
        """
        Constructor for the MultiPage class.
        """
        self.pages = []

    def add_page(self, title, func) -> None:
        """
        Add pages to the project
        
        Args:
            title: The title of page which we are adding to the list of apps
            func: Python function to render this page in Streamlit
        """
        self.pages.append({
            "title": title,
            "function": func
        })

    def run(self):
        """
        Dropdown to select the page to run
        """
        # Apply consistent styling
        apply_shared_css()
        
        # Create sidebar for page navigation
        st.sidebar.title('🏥 Navigation')
        st.sidebar.markdown("""
        <div style="background: rgba(52, 98, 171, 0.85); padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 2px solid rgba(100, 100, 120, 0.8);">
            <p style="color: #000000; font-weight: bold; text-align: center; margin: 0;">
                Healthcare Analytics Platform
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.sidebar.selectbox(
            '📋 Select a page:',
            self.pages,
            format_func=lambda page: page['title']
        )
        
        # Run the selected page function
        page['function']()