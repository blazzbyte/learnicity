import os
from typing import Optional
from dotenv import load_dotenv

class Config:
    """Configuration class to manage environment variables"""
    
    def __init__(self):
        """Initialize configuration by loading environment variables"""
        load_dotenv()
        
        # STORAGE
        self.logs_dir = os.getenv('LOGS_DIR', 'data/logs')
        
        # API KEYS
        self.google_search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        
        # API ENDPOINTS
        self.google_search_api_endpoint = os.getenv('GOOGLE_SEARCH_API_ENDPOINT')
        
        # TIMEOUT
        self.inference_timeout = int(os.getenv('INFERENCE', '30'))
    
    def get_logs_dir(self) -> Optional[str]:
        """Get the logs directory path"""
        return self.logs_dir
    
    def get_google_credentials(self) -> tuple[Optional[str], Optional[str]]:
        """Get Google Search API credentials"""
        return self.google_search_engine_id, self.google_api_key
    
    def get_google_endpoint(self) -> Optional[str]:
        """Get Google Search API endpoint"""
        return self.google_search_api_endpoint
    
    def get_inference_timeout(self) -> int:
        """Get inference timeout in seconds"""
        return self.inference_timeout