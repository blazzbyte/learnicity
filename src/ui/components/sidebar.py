import os
import streamlit as st
from src.core.config import get_translation
from src.core.config.config import get_openai_api_key

def clear_api_keys():
    """Clear all API keys from session state"""
    keys_to_clear = ['api_key', 'openai_api_key']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def sidebar():
    with st.sidebar:
        st.header(get_translation("Settings"))

        # Language selection
        current_language = st.session_state.get("current_language", "en")
        language_options = {
            "en": "English",
            "es": "Español"
        }
        
        selected_language = st.selectbox(
            get_translation("Language"),
            options=list(language_options.values()),
            index=1 if current_language == "es" else 0,
            help=get_translation("Select the language for the user interface.")
        )
        
        # Update language if changed
        new_language = "es" if selected_language == "Español" else "en"
        if current_language != new_language:
            st.session_state["current_language"] = new_language
            st.rerun()

        # API Configuration
        base_url = st.text_input(
            get_translation("Base_Url"),
            value="https://fast-api.snova.ai/v1", 
            disabled=True, 
            help=get_translation("Base URL for API calls. Cannot be changed .cause of the hakathon rules.")
        )
        st.session_state["base_url"] = base_url

        # API Key Management
        if 'use_custom_key' not in st.session_state:
            st.session_state['use_custom_key'] = False

        # Get current API key using priority system
        current_api_key = get_openai_api_key()
        
        # Toggle for custom API key
        use_custom = st.toggle(
            get_translation("Enter Custom API Key"),
            value=st.session_state['use_custom_key'],
            help=get_translation("Switch to entering your own API key.")
        )
        
        if use_custom != st.session_state['use_custom_key']:
            st.session_state['use_custom_key'] = use_custom
            clear_api_keys()
            st.rerun()

        if st.session_state['use_custom_key']:
            user_api_key = st.text_input(
                get_translation("API Key"),
                value=st.session_state.get('api_key', ''),
                type="password",
                help=get_translation("Enter your own API key to override the default.")
            )
            
            if st.button(get_translation("Save 💾")):
                if user_api_key and user_api_key.strip():
                    clear_api_keys()
                    st.session_state['api_key'] = user_api_key.strip()
                    st.success(get_translation("Custom API key saved!"))
                else:
                    st.error(get_translation("You must enter a valid API key."))
                st.rerun()
        else:
            if current_api_key:
                st.success(get_translation("Using default API key."))
            else:
                st.error(get_translation("Default API key is not available!"))
