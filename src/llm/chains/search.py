from typing import List, Dict, Any, Optional

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SerpAPIWrapper
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader

from langchain.chains.llm import LLMChain
from langchain.chains.summarize import load_summarize_chain

from src.core.config import config, logger
from src.llm.providers.llama import get_openai_chat_model
from src.llm.prompts.search_prompts import generate_queries_template
from src.llm.parsers.json_parser import get_json_from_text

class SearchChain:
    def __init__(self):
        self.setup_llm()
        self.setup_search()
        self.content_cache = {}
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)

    
    def setup_llm(self):
        """Initialize LLM with OpenAI configuration"""
        self.llm = get_openai_chat_model("llama3.1-8b")
    
    def setup_search(self):
        """Initialize search wrapper with default parameters"""
        self.search = SerpAPIWrapper(
            params={
                "engine": "google",
                "google_domain": "google.com",
                "num": 2,
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
                    logger.action(f"Successfully generated {len(queries)} queries on attempt {current_try + 1}")
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

    def searcher(self, query: str, query_type: str = "text") -> dict:
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
            url = first_result.get("link", "")
            
            # Fetch content using WebBaseLoader
            try:
                loader = WebBaseLoader(url)
                docs = loader.load()
                # Combine all page content
                content = "".join(doc.page_content for doc in docs)
                
                return {
                    "title": first_result.get("title", ""),
                    "content": content,
                    "link": url,
                    "source": first_result.get("source", first_result.get("displayed_link", ""))
                }
                
            except Exception as e:
                logger.error(f"Error fetching content from URL {url}: {str(e)}")
                return {
                    "title": first_result.get("title", ""),
                    "content": first_result.get("snippet", ""),
                    "link": url,
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
                result = self.searcher(query, query_type)
                if result:
                    content = result.get("content", "")
                    if content and query_type == "text":
                        summarized_content = self.summarize_content(content)
                        result["content"] = summarized_content
                    
                    all_results.append({
                        "query": query,
                        "type": query_type,
                        "result": result
                    })
                    logger.info(f"Successfully processed query: {query} ({query_type})")
            except Exception as e:
                logger.error(f"Error processing query '{query}': {str(e)}")
                continue
        
        return all_results

    def summarize_content(self, content: str, token_usage: Optional[int]=None) -> str:
        """Summarize content using LLM with focus on key concepts for flashcard creation"""
        try:
            # Define the reduce template for content summarization
            reduce_template = """
            Role: Educational Content Synthesizer
            Goal: Create a comprehensive summary optimized for flashcard generation
            
            Instructions:
            1. IGNORE all website metadata, navigation elements, and non-content related text
            2. Focus ONLY on the main content of the article/document
            3. Create a summary that preserves:
               - Key terms and their precise definitions
               - Core concepts and principles
               - Important relationships between ideas
               - Significant examples and applications
               - Essential technical details
               - Relevant numerical data
            4. Structure the information to facilitate flashcard creation
            5. Maintain academic accuracy and terminology
            
            Content to summarize:
            {text}
            
            Educational summary (focus on key concepts):
            """
            
            # Create the reduce prompt and chain
            reduce_prompt = ChatPromptTemplate.from_template(reduce_template)
            reduce_chain = reduce_prompt | self.llm | StrOutputParser()
            
            # Check content length and split if necessary
            if len(content) > 4000:  # Conservative limit to account for prompt
                docs = self.text_splitter.create_documents([content])
                summaries = []
                
                # Process each chunk
                for doc in docs:
                    chunk_summary = reduce_chain.invoke({"text": doc.page_content})
                    summaries.append(chunk_summary)
                
                # Combine summaries if multiple chunks were processed
                if len(summaries) > 1:
                    combined_summary = "\n\n".join(summaries)
                    # Process combined summary if it's still too long
                    if len(combined_summary) > 6000:
                        return reduce_chain.invoke({"text": combined_summary[:6000]})
                    return combined_summary
                return summaries[0]
            else:
                return reduce_chain.invoke({"text": content})
            
        except Exception as e:
            logger.error(f"Error summarizing content: {str(e)}")
            return content[:4000]  # Return truncated content as fallback

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
            docs = self.text_splitter.create_documents([combined_content])
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