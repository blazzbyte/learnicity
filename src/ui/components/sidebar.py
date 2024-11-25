import os
import streamlit as st
from src.core.config import get_translation

def sidebar():
    with st.sidebar:
        st.header(get_translation("Settings"))

        # Define the available languages
        languages = {"en": ["English", "Spanish"], "es": ["Ingles", "Español"]}
        # Get the current language from session state
        current_language = st.session_state.get("current_language", "en")
        
        # Display the selectbox for language selection
        language_ui = st.selectbox(get_translation("Language"), languages[current_language], index=0,
                                   help=get_translation("Select the language for the user interface."))

        # Determine the selected language code based on the UI language
        selected_language_code = "es" if language_ui in ["Español", "Spanish"] else "en"

        # Check if the language has changed
        if st.session_state["current_language"] != selected_language_code:
            print("Language changed to:", selected_language_code)
            # Update the session state with the new language
            st.session_state["current_language"] = selected_language_code
            # Rerun the app
            # st.rerun()

        # Display the base URL for API calls
        base_url = st.text_input(get_translation("Base_Url"), value="https://fast-api.snova.ai/v1", disabled=True, help=get_translation("Base URL for API calls. Cannot be changed 🔒.'cause of the hakathon rules."))
        st.session_state["base_url"] = base_url or st.secrets.get("OPENAI_BASE_URL")

        # Initialize session variables if not already set
        if 'use_custom_key' not in st.session_state:
            st.session_state['use_custom_key'] = False

        # Retrieve the default API key
        api_key_default = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        
        if st.session_state['use_custom_key']:
            # Input field for user's custom API key
            user_api_key = st.text_input(get_translation("API Key"), value=st.session_state.get('api_key', ''), type="password", help=get_translation("Enter your own API key to override the default."))
            # Save button with logic to switch back to default
            if st.button(get_translation("Save &/or Use Default Key"), help=get_translation("Save your custom API key and/or switch back to using the default key.")):

                if user_api_key:
                    st.session_state['api_key'] = user_api_key
                    st.success(get_translation("Custom API key saved!"), icon="🎉")
                    # Reset toggle and clear user API key when switching to default
                    st.session_state['use_custom_key'] = False
                    st.rerun()
                else:
                    st.warning(get_translation("You must enter a valid API key."), icon="⚠️")
                    st.info(body=get_translation("If you want to use the default api key then reload the page"), icon="ℹ️")

        else:
            # Inform the user about the use of the default key and offer switching
            if api_key_default and 'api_key' not in st.session_state:
                st.success(get_translation("Using default API key."), icon="✅")
                st.session_state['api_key'] = api_key_default
            elif 'api_key' in st.session_state:
                st.success(get_translation("Using saved API key."), icon="ℹ️")
            else:
                st.warning(get_translation("Default API key is not available!"), icon="⚠️")

            # Button to switch to entering a custom key
            if st.button(get_translation("Enter Custom API Key"), help=get_translation("Switch to entering your own API key.")):
                st.session_state['use_custom_key'] = True
                # Clear any stored API key if switching to custom input
                if 'api_key' in st.session_state:
                    del st.session_state['api_key']
                st.rerun()
