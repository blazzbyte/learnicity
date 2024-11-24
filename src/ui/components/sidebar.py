import os
import streamlit as st

def sidebar():
    with st.sidebar:
        st.header("Settings")

        # Display the base URL for API calls
        base_url = st.text_input("Base_Url", value="https://fast-api.snova.ai/v1", disabled=True, help="Base URL for API calls.")
        st.session_state["base_url"] = base_url or st.secrets.get("OPENAI_BASE_URL")

        # Initialize session variables if not already set
        if 'use_custom_key' not in st.session_state:
            st.session_state['use_custom_key'] = False

        # Retrieve the default API key
        api_key_default = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        
        if st.session_state['use_custom_key']:
            # Input field for user's custom API key
            user_api_key = st.text_input("API Key", value=st.session_state.get('api_key', ''), type="password", help="Enter your own API key to override the default.")
            # Save button with logic to switch back to default
            if st.button("Save &/or Use Default Key", help="Save your custom API key and/or switch back to using the default key."):

                if user_api_key:
                    st.session_state['api_key'] = user_api_key
                    st.success("Custom API key saved!", icon="🎉")
                    # Reset toggle and clear user API key when switching to default
                    st.session_state['use_custom_key'] = False
                    st.rerun()
                else:
                    st.warning("You must enter a valid API key.", icon="⚠️")
                    st.info(body="If you want to use the default api key then reload the page", icon="ℹ️")

        else:
            # Inform the user about the use of the default key and offer switching
            if api_key_default and 'api_key' not in st.session_state:
                st.success("Using default API key.", icon="✅")
                st.session_state['api_key'] = api_key_default
            elif 'api_key' in st.session_state:
                st.success("Using saved API key.", icon="ℹ️")
            else:
                st.warning("Default API key is not available!", icon="⚠️")

            # Button to switch to entering a custom key
            if st.button("Enter Custom API Key", help="Switch to entering your own API key."):
                st.session_state['use_custom_key'] = True
                # Clear any stored API key if switching to custom input
                if 'api_key' in st.session_state:
                    del st.session_state['api_key']
                st.rerun()
