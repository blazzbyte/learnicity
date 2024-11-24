"""Flashcard parser for handling LLM responses"""

import re
import json
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

def parse_flashcards(text: str, is_image: bool = False) -> List[Dict[str, Any]]:
    """
    Parse flashcards from LLM response text.
    
    Args:
        text (str): Input text that may contain flashcard JSON
        is_image (bool): If True, validates that only one flashcard is returned for images
        
    Returns:
        List[Dict[str, Any]]: List of flashcard dictionaries
    """
    try:
        # Try to find JSON objects in the text
        matches = re.finditer(r'(\{(?:[^{}]|{[^{}]*})*\})', text)
        
        for match in matches:
            try:
                json_str = match.group(0)
                result = json.loads(json_str)
                
                # Check if it's a flashcards object
                if isinstance(result, dict) and "flashcards" in result:
                    flashcards = result["flashcards"]
                    if isinstance(flashcards, list):
                        # For images, validate only one flashcard
                        if is_image and len(flashcards) > 1:
                            logger.warning("More than one flashcard found for image. Using only the first one.")
                            return [flashcards[0]]
                        return flashcards
                        
            except json.JSONDecodeError:
                continue
        
        logger.warning("No valid flashcard JSON found in response")
        return []
        
    except Exception as e:
        logger.error(f"Error parsing flashcards: {str(e)}")
        return []
