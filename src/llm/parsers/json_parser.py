import re
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def get_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract and parse JSON from text that may contain explanatory content before and after.
    Designed to handle cases where JSON is embedded within explanatory text.
    
    Args:
        text (str): Input text that may contain JSON
        
    Returns:
        Optional[Dict[str, Any]]: Parsed JSON object or None if no valid JSON found
    """
    try:
        # Buscar el JSON más completo que contenga "queries"
        matches = re.finditer(r'(\{(?:[^{}]|{[^{}]*})*\})', text)
        
        for match in matches:
            try:
                json_str = match.group(0)
                # Intentar parsear el JSON
                result = json.loads(json_str)
                # Verificar si tiene la estructura esperada
                if isinstance(result, dict) and "queries" in result:
                    return result
            except json.JSONDecodeError:
                continue
        
        logger.warning("No valid JSON object found with queries structure")
        return None
        
    except Exception as e:
        logger.error(f"Error in JSON extraction: {str(e)}")
        return None