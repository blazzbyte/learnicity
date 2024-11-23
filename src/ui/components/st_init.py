import streamlit as st
import os
from src.data.db import init_db
from src.core.config import logger

def init_database():
    """Initialize database if not already initialized"""
    if 'db_initialized' not in st.session_state:
        try:
            init_db()
            st.session_state['db_initialized'] = True
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            st.error("Failed to initialize database. Please check the logs.")

def load_css():
    """Load custom CSS styles"""
    css_path = os.path.join(os.path.dirname(__file__), 'styles.css')
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def st_init():
    """Initialize Streamlit configuration and resources"""
    # Set page config
    st.set_page_config(
        page_title="Learnicity",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize database
    init_database()

    # Load CSS styles
    load_css()
