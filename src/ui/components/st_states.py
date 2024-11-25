import streamlit as st
import json

from src.core.config import logger
from src.data.services.user_service import UserService

def init_session_states():
    if 'user_id' not in st.session_state:
        user_service = UserService()
        user = user_service.create_user()
        st.session_state['user_id'] = user.id
    if 'translations' not in st.session_state:
        # Load translations
        with open('translations.json', 'r', encoding="utf-8") as file:
            st.session_state['translations'] =  json.load(file)
    if 'current_language' not in st.session_state:
        st.session_state['current_language'] = 'en'