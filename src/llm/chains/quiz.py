"""Quiz generation chain for creating quizzes from flashcards"""

from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.core.config import config, logger
from src.llm.providers.llama import get_openai_chat_model
from src.llm.parsers.quiz_parser import parse_quiz

from src.llm.prompts.quiz_prompts import (
    quiz_system_template,
    quiz_human_template
)

class QuizChain:
    """Chain for generating quizzes from flashcards"""
    
    def __init__(self):
        """Initialize the quiz generation chain"""
        self.setup_llm()
        self.setup_chain()
        
    def setup_llm(self):
        """Initialize LLM with configuration"""
        self.llm = get_openai_chat_model("Meta-Llama-3.1-8B-Instruct", max_tokens=4096)
        
    def setup_chain(self):
        """Setup the quiz generation chain"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", quiz_system_template),
            ("human", quiz_human_template)
        ])
        
        self.chain = prompt | self.llm | StrOutputParser()
        
    def create_quiz(self, flashcards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate a quiz from flashcards
        
        Args:
            flashcards (List[Dict[str, Any]]): List of flashcard dictionaries
            
        Returns:
            List[Dict[str, Any]]: List of quiz questions. Each question has:
                - question: str
                - options: List[str]
                - correct_answer: int
                - explanation: str
                - image_url: Optional[str]
        """
        try:
            # Convert flashcards to string representation
            flashcards_str = str(flashcards)
            
            # Generate quiz using LLM
            result = self.chain.invoke({
                "flashcards": flashcards_str
            })
            
            # Parse the quiz using dedicated parser
            quiz = parse_quiz(result)
            if not quiz:
                logger.error("Failed to parse quiz from response")
                return []
                
            return quiz
            
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            return []
