import os
import streamlit as st

def sidebar():
    with st.sidebar:
        st.header("Settings")

        # # First input field for the model name
        # model_name = st.text_input("Model Name", "Meta-Llama-3.1-8B-Instruct", help=("Enter the model name. "
        #                                                               "For example: Meta-Llama-3.1-8B-Instruct, llama3.1-70b, "
        #                                                               "llama-3.2-11b-vision-preview, llama-3.2-90b-vision-preview"))
        # st.selectbox()
        # # Check if the 'OPENAI_BASE_URL' is set in either st.secrets or environment variables
        # base_url_default = os.getenv("OPENAI_BASE_URL", st.secrets.get("OPENAI_BASE_URL", ""))
        # base_url = st.text_input("Base_Url", value=base_url_default, disabled=True if base_url_default else False)

        # # Check if the 'OPENAI_API_KEY' is set in either st.secrets or environment variables
        # api_key_default = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
        # if api_key_default:
        #     st.success(body="API key detected!", icon="✅")
        #     api_key = api_key_default
        # else:
        #     st.warning(body="API key not detected!", icon="⚠️")
        #     # Input field for the API key
        #     api_key = st.text_input("Api_Key", placeholder="Enter your API key here", type="password")
