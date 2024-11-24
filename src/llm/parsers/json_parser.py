import re
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def get_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract and parse JSON from text that may contain markdown or other content.
    
    Args:
        text (str): Input text that may contain JSON
        
    Returns:
        Optional[Dict[str, Any]]: Parsed JSON object or None if no valid JSON found
    """
    # Try to find JSON block in markdown code block
    markdown_pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
    markdown_matches = re.findall(markdown_pattern, text, re.DOTALL)
    
    if markdown_matches:
        # Try each markdown block
        for match in markdown_matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
    
    # If no markdown blocks found or none were valid JSON,
    # try to find raw JSON object
    json_pattern = r"(\{(?:[^{}]|{(?:[^{}]|{[^{}]*})*})*\})"
    json_matches = re.findall(json_pattern, text, re.DOTALL)
    
    if json_matches:
        # Try each potential JSON block
        for match in json_matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
    
    # If still no valid JSON found, try cleaning the text
    cleaned_text = text.strip()
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        logger.warning("No valid JSON found in text")
        return None