"""Configuration class to manage environment variables"""

import os
import streamlit as st
from typing import Optional
from dotenv import load_dotenv

def get_translation(text)->str:
    if st.session_state.get("current_language") == "en":
        # Return the key if no translation is available
        return text
    else:
        # English is the default; look for a translation
        return st.session_state["translations"].get(text, text)

def get_api_key(key_name: str) -> Optional[str]:
    """
    Get API key with the following priority:
    1. API key from Streamlit secrets
    2. API key from environment variables
    """
    try:
        # Try to get from Streamlit secrets first
        api_key = st.secrets.get(key_name)
        if api_key and api_key.strip():
            return api_key.strip()
    except Exception:
        pass
    
    # Then try environment variable
    api_key = os.environ.get(key_name, "").strip()
    return api_key if api_key else None

def get_openai_api_key() -> Optional[str]:
    """
    Get OpenAI API key with the following priority:
    1. Custom API key from session state
    2. API key from Streamlit secrets
    3. API key from environment variables
    """
    # Check for custom key first
    if st.session_state.get('use_custom_key'):
        return st.session_state.get('api_key')
    
    # Try to get from Streamlit secrets
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
        if api_key and api_key.strip():
            return api_key.strip()
    except Exception:
        pass
    
    # Finally, try environment variable
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    return api_key if api_key else None

class Config:
    """Configuration class to manage environment variables"""
    
    def __init__(self):
        """Initialize configuration by loading environment variables"""
        self.load_config()
        
    def load_config(self):
        """Load or reload environment variables"""
        load_dotenv(override=True)  # Force reload of .env file
        
        # STORAGE
        self.logs_dir = os.getenv('LOGS_DIR', 'src/data/logs')
        
        # API KEYS - Using priority system for all keys
        self.serpapi_api_key = get_api_key('SERPAPI_API_KEY')
        self.openai_api_key = get_openai_api_key()
        
        # API ENDPOINTS
        self.openai_base_url = st.secrets.get("OPENAI_BASE_URL", os.getenv('OPENAI_BASE_URL'))
        
        # TIMEOUT
        self.inference_timeout = int(os.getenv('INFERENCE', '30'))
    
    def reload(self):
        """Reload all environment variables"""
        self.load_config()
    
    def get_inference_timeout(self) -> int:
        """Get inference timeout value"""
        return self.inference_timeout
    
    def get_logs_dir(self) -> Optional[str]:
        """Get the logs directory path"""
        return self.logs_dir
    
    def get_serpapi_credentials(self) -> Optional[str]:
        """Get SerpAPI API key"""
        return self.serpapi_api_key
    
    def get_openai_credentials(self) -> tuple[Optional[str], Optional[str]]:
        """Get OpenAI API credentials and base URL"""
        return self.openai_api_key, self.openai_base_url

# Create a singleton instance
config = Config()