import streamlit as st


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
        # Create sidebar for page navigation
        st.sidebar.title('Navigation')
        page = st.sidebar.selectbox(
            'Select a page:',
            self.pages,
            format_func=lambda page: page['title']
        )
        
        # Run the selected page function
        page['function']()