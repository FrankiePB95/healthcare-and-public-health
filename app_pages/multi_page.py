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
        Dropdown to select the page to run with session state persistence
        """
        # Apply consistent styling
        apply_shared_css()
        
        # Initialize session state for page persistence
        if 'current_page_index' not in st.session_state:
            st.session_state.current_page_index = 0  # Default to first page (Home)
        
        # Create sidebar for page navigation
        st.sidebar.title('🏥 Navigation')
        st.sidebar.markdown("""
        <div style="background: rgba(52, 98, 171, 0.85); padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 2px solid rgba(100, 100, 120, 0.8);">
            <p style="color: #000000; font-weight: bold; text-align: center; margin: 0;">
                Healthcare Analytics Platform
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add page persistence info
        st.sidebar.markdown("""
        <div style="background: rgba(25, 135, 84, 0.1); padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem; border-left: 3px solid #198754;">
            <p style="color: #000000; font-size: 0.8rem; margin: 0; font-weight: bold;">
                💾 Your current page selection is preserved across reloads
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create selectbox with session state persistence
        selected_page = st.sidebar.selectbox(
            '📋 Select a page:',
            self.pages,
            index=st.session_state.current_page_index,
            format_func=lambda page: page['title'],
            key='page_selector'
        )
        
        # Update session state when page changes
        for i, page in enumerate(self.pages):
            if page['title'] == selected_page['title']:
                if st.session_state.current_page_index != i:
                    st.session_state.current_page_index = i
                    # Update URL parameters for bookmarking and sharing
                    st.experimental_set_query_params(page=str(i))
                break
        
        # Add current page indicator in sidebar
        st.sidebar.markdown(f"""
        <div style="background: rgba(13, 110, 253, 0.1); padding: 0.8rem; border-radius: 8px; margin: 1rem 0; border: 2px solid #0d6efd;">
            <p style="color: #000000; font-weight: bold; text-align: center; margin: 0; font-size: 0.9rem;">
                📍 Current Page:<br>
                <strong>{selected_page['title']}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Run the selected page function
        selected_page['function']()