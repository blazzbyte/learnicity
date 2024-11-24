import os
import streamlit as st

def sidebar():
    with st.sidebar:
        st.header("Settings")

        # Check if the 'OPENAI_BASE_URL' is set in either st.secrets or environment variables
        base_url = st.text_input("Base_Url", value="https://fast-api.snova.ai/v1", disabled=True, help="Base URL for the API calls. restricted use for the hackathon. to this provider.")

        # Check if the 'OPENAI_API_KEY' is set in either st.secrets or environment variables
        api_key_default = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
        if api_key_default:
            st.success(body="API key detected!", icon="✅")
            api_key = api_key_default
        else:
            st.warning(body="API key not detected!", icon="⚠️")
            # Input field for the API key
            api_key = st.text_input("Api_Key", placeholder="Enter your API key here", type="password")
