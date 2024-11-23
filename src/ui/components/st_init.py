import streamlit as st
import asyncio

from src.core.config import logger
from src.data.services.user_service import UserService

def init_data():
    if 'event_loop' not in st.session_state:
        st.session_state.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(st.session_state.event_loop)

    # Use event loop from streamlit
    loop = st.session_state.event_loop

    # Load user
    user_service = UserService()
    loop.run_until_complete(user_service.load_from_storage())

def st_init():
    """Initialize Streamlit configuration and resources"""
    # Set page config
    st.set_page_config(
        page_title="Learnicity",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.cache_resource(init_data())

    # Styles
    st.markdown(
        """<style>.eczjsme4 {
            padding: 4rem 1rem;
        }</style>""",
        unsafe_allow_html=True,
    )