"""Configuration class to manage environment variables"""

import os
import streamlit as st
from typing import Optional
from dotenv import load_dotenv

def get_translation(text)->str:
    if st.session_state.get("current_language") == "es":
        # Return the key if no translation is available
        return text
    else:
        # English is the default; look for a translation
        return st.session_state["translations"].get(text, text)

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
        
        # API KEYS
        self.serpapi_api_key = os.getenv('SERPAPI_API_KEY')
        self.openai_api_key = st.session_state.get("api_key", os.getenv('OPENAI_API_KEY'))
        
        # API ENDPOINTS
        self.openai_base_url = st.session_state.get("base_url", os.getenv('OPENAI_BASE_URL'))

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
    
    def get_google_credentials(self) -> tuple[Optional[str]]:
        """Get Google Search API credentials"""
        return (self.google_search_engine_id,)
    
    def get_serpapi_credentials(self) -> Optional[str]:
        """Get SerpAPI API key"""
        return self.serpapi_api_key
    
    def get_openai_credentials(self) -> tuple[Optional[str], Optional[str]]:
        """Get OpenAI API credentials and base URL"""
        return self.openai_api_key, self.openai_base_url
    
    def get_tavily_credentials(self) -> Optional[str]:
        """Get Tavily API key"""
        return self.tavily_api_key
    
    def get_jina_credentials(self) -> Optional[str]:
        """Get Jina API key"""
        return self.jina_api_key
    
    def get_google_endpoint(self) -> Optional[str]:
        """Get Google Search API endpoint"""
        return self.google_search_api_endpoint

# Create a singleton instance
config = Config()