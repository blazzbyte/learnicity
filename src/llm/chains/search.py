from typing import List, Dict, Any, Optional
from src.core.config import config, logger
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


from langchain.chains import LLMChain
from langchain_community.utilities import SerpAPIWrapper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import requests
# from bs4 import BeautifulSoup
from src.llm.providers.llama import get_openai_chat_model
from src.llm.prompts.search_prompts import generate_queries_template
import json

from src.llm.parsers.json_parser import get_json_from_text

class SearchChain:
    def __init__(self):
        self.setup_llm()
        self.setup_search()
        self.content_cache = {}
    
    def setup_llm(self):
        """Initialize LLM with OpenAI configuration"""
        self.llm = get_openai_chat_model("llama3.1-8b")
    
    def setup_search(self):
        """Initialize search wrapper with default parameters"""
        self.search = SerpAPIWrapper(
            params={
                "engine": "google",
                "google_domain": "google.com",
                "num": 1,
                "hl": "en"
            }
        )
        
        self.image_search = SerpAPIWrapper(
            params={
                "engine": "google_images",
                "google_domain": "google.com",
                "hl": "en",
                "safe": "active"
            }
        )
    
    def generate_search_queries(self, query: str, num_queries: int = 3) -> List[str]:
        """Generate multiple search queries to cover different aspects of the topic"""
        prompt = ChatPromptTemplate.from_template(generate_queries_template)
        chain = prompt | self.llm | StrOutputParser()
        
        max_retries = 2
        current_try = 0
        
        while current_try < max_retries:
            try:
                result = chain.invoke({"query": query, "num_queries": num_queries})
                data = get_json_from_text(result)
                queries = data.get("queries", [])
                if queries:
                    logger.info(f"Successfully generated {len(queries)} queries on attempt {current_try + 1}")
                    return queries
                else:
                    logger.warning(f"Generated empty queries list on attempt {current_try + 1}")
            except Exception as e:
                logger.error(f"Error generating queries (attempt {current_try + 1}): {str(e)}")
                if current_try == max_retries - 1:
                    logger.error("Max retries reached, returning empty list")
                    return []
            current_try += 1
            
        return []
    
    def search_image(self, query: str) -> dict:
        """Perform image search and return image result"""
        try:
            search_results = self.image_search.results(query)
            images_results = search_results.get("images_results", [])
            
            if not images_results:
                logger.warning(f"No images found for query: {query}")
                return None
            
            first_image = images_results[0]
            return {
                "title": first_image.get("title", ""),
                "content": first_image.get("original"),
                "link": first_image.get("original"),
                "source": first_image.get("source", "")
            }
            
        except Exception as e:
            logger.error(f"Error in image search for query '{query}': {str(e)}")
            return None

    def search_and_fetch(self, query: str, query_type: str = "text") -> dict:
        """Perform search and fetch content from URLs"""
        try:
            if query_type == "image":
                return self.search_image(query)
                
            search_results = self.search.results(query)
            organic_results = search_results.get("organic_results", [])
            
            if not organic_results:
                logger.warning(f"No organic results found for query: {query}")
                return None
                
            first_result = organic_results[0]
            return {
                "title": first_result.get("title", ""),
                "content": first_result.get("snippet", ""),
                "link": first_result.get("link", ""),
                "source": first_result.get("source", first_result.get("displayed_link", ""))
            }
            
        except Exception as e:
            logger.error(f"Error in search for query '{query}': {str(e)}")
            return None

    def process_queries(self, topic: str) -> List[dict]:
        """Process multiple queries and aggregate results"""
        queries = self.generate_search_queries(topic)
        all_results = []
        
        for query_data in queries:
            query = query_data.get("query", "")
            query_type = query_data.get("type", "text")
            
            try:
                result = self.search_and_fetch(query, query_type)
                if result:
                    result_data = {
                        "query": query,
                        "type": query_type,
                        "result": result
                    }
                    all_results.append(result_data)
                    logger.info(f"Successfully processed query: {query} ({query_type})")
            except Exception as e:
                logger.error(f"Error processing query '{query}': {str(e)}")
                continue
        
        return all_results
    
    def create_flashcards(self, content: str) -> List[Dict[str, Any]]:
        """Generate flashcards from the content"""
        flashcard_template = """Create educational flashcards from the following content. Each flashcard should have:
        1. A clear, specific question
        2. A concise but complete answer
        3. A relevant category
        4. Optional image URLs for both question and answer (leave as null if not relevant)

        Content: {content}

        Generate the flashcards in this exact format:
        [
            {
                "question": "Question text",
                "answer": "Answer text",
                "category": "Subject category",
                "question_image": "URL or null",
                "answer_image": "URL or null"
            }
        ]

        Create 3-5 high-quality flashcards that test important concepts from the content."""
        
        flashcard_prompt = PromptTemplate(template=flashcard_template, input_variables=["content"])
        flashcard_chain = LLMChain(llm=self.llm, prompt=flashcard_prompt)
        
        # Split content if too long
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(content)
        
        all_flashcards = []
        for chunk in chunks:
            try:
                result = flashcard_chain.run(content=chunk)
                # Parse the result and append flashcards
                # Note: You might need to add proper JSON parsing here
                flashcards = eval(result)  # Be careful with eval, consider using json.loads with proper error handling
                all_flashcards.extend(flashcards)
            except Exception as e:
                logger.error(f"Error creating flashcards: {str(e)}")
                continue
        
        return all_flashcards
    
    def search_chain(self, query: str) -> List[Dict[str, Any]]:
        """Main chain that coordinates the entire search and flashcard creation process"""
        # Refine the original query
        refined_query = self.refine_query(query)
        
        # Generate multiple search queries
        search_queries = self.generate_search_queries(refined_query)
        
        # Collect content from all queries
        all_content = []
        for query in search_queries:
            content = self.search_and_fetch(query)
            all_content.extend(content)
        
        # Combine and summarize content if too long
        combined_content = " ".join(all_content)
        if len(combined_content) > 8000:
            summarize_chain = load_summarize_chain(self.llm, chain_type="map_reduce")
            docs = text_splitter.create_documents([combined_content])
            combined_content = summarize_chain.run(docs)
        
        # Create flashcards from the processed content
        flashcards = self.create_flashcards(combined_content)
        
        logger.info(f"Generated {len(flashcards)} flashcards")
        return flashcards

# For backwards compatibility
def search_chain():
    search = SearchChain()
    return search.search_chain("General knowledge flashcards")
    return example_flashcards