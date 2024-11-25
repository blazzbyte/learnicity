import streamlit as st
import json
import os

from src.core.config import logger
from src.data.services.user_service import UserService

def load_translations():
    """Load translations from JSON file with error handling"""
    try:
        translation_path = os.path.join('translations.json')
        if not os.path.exists(translation_path):
            logger.error(f"Translation file not found at {translation_path}")
            return {}
            
        with open(translation_path, 'r', encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding translations file: {str(e)}")
        return {}
    except Exception as e:
        logger.error(f"Error loading translations: {str(e)}")
        return {}

def init_session_states():
    """Initialize all session state variables"""
    # Initialize user ID if not present
    if 'user_id' not in st.session_state:
        user_service = UserService()
        user = user_service.create_user()
        st.session_state['user_id'] = user.id
    
    # Load translations
    if 'translations' not in st.session_state:
        translations = load_translations()
        if not translations:
            logger.warning("Using empty translations dictionary")
        st.session_state['translations'] = translations
    
    # Initialize language preference
    if 'current_language' not in st.session_state:
        # Default to Spanish for now, later can add browser language detection
        st.session_state['current_language'] = 'es'
    
    # Initialize other states if needed
    if 'use_custom_key' not in st.session_state:
        st.session_state['use_custom_key'] = False