"""Quiz parser for handling LLM responses"""

import re
import json
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

def parse_quiz(text: str) -> List[Dict[str, Any]]:
    """
    Parse quiz from LLM response text.
    
    Args:
        text (str): Input text that may contain quiz JSON
        
    Returns:
        List[Dict[str, Any]]: List of quiz questions
    """
    try:
        # Try to find JSON objects in the text
        matches = re.finditer(r'(\{(?:[^{}]|{[^{}]*})*\})', text)
        
        for match in matches:
            try:
                json_str = match.group(0)
                result = json.loads(json_str)
                
                # Check if it's a quiz object
                if isinstance(result, dict) and "quiz" in result:
                    quiz = result["quiz"]
                    if isinstance(quiz, list):
                        # Validate each question has required fields
                        for question in quiz:
                            if not all(key in question for key in ["question", "options", "correct_answer", "explanation"]):
                                logger.warning("Question missing required fields")
                                continue
                            if not isinstance(question["options"], list) or len(question["options"]) != 4:
                                logger.warning("Question has invalid options")
                                continue
                            if not isinstance(question["correct_answer"], int) or question["correct_answer"] not in range(4):
                                logger.warning("Question has invalid correct_answer")
                                continue
                        return quiz
                        
            except json.JSONDecodeError:
                continue
        
        logger.warning("No valid quiz JSON found in response")
        return []
        
    except Exception as e:
        logger.error(f"Error parsing quiz: {str(e)}")
        return []
