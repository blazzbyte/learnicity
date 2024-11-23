import streamlit as st
import asyncio

from src.core.config import logger
from src.data.db import init_db

def st_init():
    # Set page config
    st.set_page_config(
        page_title="Learnicity",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize database
    if 'db_initialized' not in st.session_state:
        asyncio.run(init_db())
        st.session_state.db_initialized = True

    # Styles
    st.markdown(
        """<style>.eczjsme4 {
            padding: 4rem 1rem;
            }
            .css-w770g5{
            width: 100%;}
            .css-b3z5c9{
            width: 100%;}
            .stButton>button{
            width: 100%;}
            .stDownloadButton>button{
            width: 100%;}
            button[data-testid="baseButton-primary"]{
            border-color: #505050;
            background-color: #1E1E1E;
            }
            button[data-testid="baseButton-primary"]:hover {
            border-color: #FC625F;
            background-color: #1E1E1E;
            color: #FC625F;
            }
            </style>""",
        unsafe_allow_html=True
    )