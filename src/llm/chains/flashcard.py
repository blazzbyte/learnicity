from typing import List, Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.core.config import config, logger
from src.llm.providers.llama import get_openai_chat_model
from src.llm.parsers.flashcard_parser import parse_flashcards

from src.llm.prompts.fcard_prompts import (
    web_flashcard_system_template,
    web_flashcard_human_template,
    image_flashcard_system_template,
    image_flashcard_human_template
)

class FlashcardChain():
    """Chain for generating educational flashcards from web content and images."""

    def __init__(self):
        """Initialize the FlashcardChain with necessary components."""
        super().__init__()
        self.setup_llm()
        self.setup_chains()

    def setup_llm(self):
        """Initialize LLM with OpenAI configuration"""
        self.llm = get_openai_chat_model("Meta-Llama-3.1-8B-Instruct")
        self.image_llm = get_openai_chat_model("Llama-3.2-11B-Vision-Instruct")

    def setup_chains(self):
        """Setup the web and image flashcard generation chains."""
        # Web content flashcard chain
        prompt_web_chain = ChatPromptTemplate.from_messages([
            ("system", web_flashcard_system_template),
            ("human", web_flashcard_human_template)
        ])

        self.web_chain = prompt_web_chain | self.llm | StrOutputParser()

        # Image content flashcard chain
        prompt_image_chain = ChatPromptTemplate.from_messages([
            ("system", image_flashcard_system_template),
            ("human", image_flashcard_human_template)
        ])

        self.image_chain = prompt_image_chain | self.image_llm | StrOutputParser()

    def create_web_flashcards(
        self,
        content: str,
        title: str,
        link: str,
        previous_flashcards: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate flashcards from web content.

        Args:
            content: The web content to create flashcards from
            title: The title of the web page
            link: The URL of the web page
            previous_flashcards: List of previously generated flashcards to avoid duplication

        Returns:
            List of flashcard dictionaries
        """
        try:
            # Format previous flashcards for prompt
            prev_cards_str = str(
                previous_flashcards) if previous_flashcards else "[]"

            # Generate flashcards using the messages
            result = self.web_chain.invoke({
                "title": title,
                "link": link,
                "previous_flashcards": prev_cards_str,
                "content": content
            })

            # Parse the JSON response
            flashcards = parse_flashcards(result)
            if not flashcards:
                logger.error("Failed to parse flashcards from response")
                return []

            return flashcards

        except Exception as e:
            logger.error(f"Error creating web flashcards: {str(e)}")
            return []

    def create_image_flashcards(
        self,
        image_url: str,
        image_description: str,
        previous_flashcards: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate flashcards from image content.

        Args:
            image_url: The URL of the image to analyze
            image_description: A description of the image
            previous_flashcards: List of previously generated flashcards to avoid duplication

        Returns:
            List of flashcard dictionaries
        """
        try:
            # Format previous flashcards for prompt
            prev_cards_str = str(
                previous_flashcards) if previous_flashcards else "[]"

            # Generate flashcards using the vision model
            result = self.image_chain.invoke({
                "previous_flashcards": prev_cards_str,
                "image_description": image_description,
                "image_url": image_url
            })
            print(result)

            # Parse the JSON response
            flashcards = parse_flashcards(result, is_image=True)
            if not flashcards:
                logger.error("Failed to parse flashcards from response")
                return []

            return flashcards

        except Exception as e:
            logger.error(f"Error creating image flashcards: {str(e)}")
            return []

    def validate_flashcard(self, flashcard: Dict[str, Any]) -> bool:
        """
        Validate a flashcard has all required fields.

        Args:
            flashcard: The flashcard dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = {"question", "answer", "source", "type"}
        return all(field in flashcard for field in required_fields)

    def process_search_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process search results and generate appropriate flashcards.

        Args:
            results: List of search results from SearchChain

        Returns:
            List of all generated flashcards
        """
        all_flashcards = []

        try:
            for result in results:
                query_type = result.get("type")
                result_data = result.get("result", {})

                if not result_data:
                    continue

                if query_type == "text":
                    # Generate flashcards from web content
                    flashcards = self.create_web_flashcards(
                        content=result_data.get("content", ""),
                        title=result_data.get("title", ""),
                        link=result_data.get("link", ""),
                        previous_flashcards=all_flashcards
                    )
                    all_flashcards.extend(flashcards)

                elif query_type == "image":
                    # Generate flashcards from image content
                    # Assuming image URL is in link field
                    image_url = result_data.get("link")
                    if image_url:
                        flashcards = self.create_image_flashcards(
                            image_url=image_url,
                            image_description=result_data.get("title", ""),
                            previous_flashcards=[]
                        )
                        all_flashcards.extend(flashcards)

            return all_flashcards

        except Exception as e:
            logger.error(f"Error processing search results: {str(e)}")
            return all_flashcards
