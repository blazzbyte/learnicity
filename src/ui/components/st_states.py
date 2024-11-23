import streamlit as st
import asyncio

from src.core.config import logger
from src.data.services.user_service import UserService

def init_session_states():
    if 'user_id' not in st.session_state:
        user_service = UserService()
        user = user_service.create_user()
        st.session_state['user_id'] = user.id