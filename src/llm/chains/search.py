from typing import List, Dict, Any, Optional
from src.core.config import config, logger
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


from langchain.chains import LLMChain
from langchain.utilities import SerpAPIWrapper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import requests
# from bs4 import BeautifulSoup
from src.llm.providers.llama import get_openai_chat_model
from src.llm.prompts.search_prompts import generate_queries_template
import json

class SearchChain:
    def __init__(self):
        self.setup_llm()
        self.setup_search()
        self.content_cache = {}
    
    def setup_llm(self):
        """Initialize LLM with OpenAI configuration"""
        self.llm = get_openai_chat_model("llama3.1-8b")
    
    def setup_search(self):
        """Initialize SerpAPI wrapper for web search"""
        serpapi_key = config.get_serpapi_credentials()
        self.search = SerpAPIWrapper(
            serpapi_api_key=serpapi_key,
            search_engine="google",
            params={
                "num": 2,
                "hl": "es"
            }
        )
    
    def refine_query(self, query: str) -> str:
        """Refine the user's query to make it more specific and searchable"""
        refine_template = """Given the user's learning query, create a more specific and detailed search query that will help find accurate information.
        Original query: {query}
        Make it more specific and detailed while keeping the core intent. Focus on educational content.
        Refined query:"""
        
        refine_prompt = PromptTemplate(template=refine_template, input_variables=["query"])
        refine_chain = LLMChain(llm=self.llm, prompt=refine_prompt)
        
        refined_query = refine_chain.run(query)
        logger.info(f"Refined query: {refined_query}")
        return refined_query.strip()
    
    def generate_search_queries(self, query: str, num_queries: int = 5) -> List[str]:
        """Generate multiple search queries to cover different aspects of the topic"""
        prompt = ChatPromptTemplate.from_template(generate_queries_template)

        chain = prompt | self.llm | JsonOutputParser()
        
        result = chain.invoke({"query":query, "num_queries":num_queries})
        print(result)
        # Parse JSON response
        # queries_data = json.loads(result)
        # logger.info(f"Generated queries: {queries_data.get('queries', [])}")
        # return queries_data.get("queries", [])
        #     queries = queries_data.get("queries", [])
            
        #     # Ensure we have the requested number of queries
        #     queries = queries[:num_queries]
            
        #     logger.info(f"Generated queries: {queries}")
        #     return queries
            
        # except json.JSONDecodeError as e:
        #     logger.error(f"Error parsing generated queries JSON: {e}")
        #     # Fallback: try to extract queries using simple string splitting
        #     queries = [q.strip() for q in result.split('\n') if q.strip() and not q.startswith('{') and not q.endswith('}')]
        #     return queries[:num_queries]
        # except Exception as e:
        #     logger.error(f"Error generating queries: {e}")
        #     # Return the original query as fallback
        #     return [query]
    
    def search_and_fetch(self, query: str) -> List[str]:
        """Perform search and fetch content from URLs"""
        search_results = self.search.results(query, num_results=5)
        contents = []
        
        for result in search_results:
            url = result.get("link")
            if url in self.content_cache:
                contents.append(self.content_cache[url])
                continue
                
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                # Normalize whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                self.content_cache[url] = text
                contents.append(text)
                
            except Exception as e:
                logger.error(f"Error fetching content from {url}: {str(e)}")
                continue
        
        return contents
    
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


# import os
# from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.messages import SystemMessage, HumanMessage

# from dotenv import load_dotenv

# # Set up OpenAI API key
# api_key = os.getenv("OPENAI_API_KEY")
# base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


# # We define the chatprompt template with the input variable "topic"
# chat_prompt = ChatPromptTemplate.from_messages(
#      [
#       SystemMessage(content="You are a helpful assistant that generates queries based on a given topic."), 
#       HumanMessage(content="Generate a JSON list object of five similar queries based on the following topic: {topic}"),
#       ])


# # Set up the JSON output parser
# parser = JsonOutputParser()

# # Instantiate the ChatOpenAI model
# model = ChatOpenAI(
#     model="Meta-Llama-3.1-8B-Instruct",
#     api_key=api_key,
#     base_url=base_url,
#     temperature=0)

# # Create the chain
# chain = chat_prompt | model | parser

# if __name__ == "__main__":
#     # Load environment variables from .env file
#     load_dotenv()
#     # Invoke the chain with user input
#     user_input = "Artificial Intelligence"  # Example user input
#     result = chain.invoke({"topic": user_input})
#     print(result)
# def search_chain():
#     example_flashcards = [
#         {
#             'question': '¿Cuál es la capital de Francia?',
#             'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
#             'answer': 'París',
#             'answer_image': None,
#             'category': 'Geografía'
#         },
#         {
#             'question': '¿Qué es H2O?',
#             'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/H2O_2D_labelled.svg/1200px-H2O_2D_labelled.svg.png',
#             'answer': 'Agua (dos átomos de hidrógeno y uno de oxígeno)',
#             'answer_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Water_molecule_3D.svg/1200px-Water_molecule_3D.svg.png',
#             'category': 'Química'
#         },
#         {
#             'question': '¿Quién escribió "Cien años de soledad"?',
#             'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
#             'answer': 'Gabriel García Márquez',
#             'answer_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
#             'category': 'Literatura'
#         },
#         {
#             'question': '¿Cuál es el planeta más grande del sistema solar?',
#             'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Jupiter_and_its_shrunken_Great_Red_Spot.jpg/1200px-Jupiter_and_its_shrunken_Great_Red_Spot.jpg',
#             'answer': 'Júpiter',
#             'answer_image': None,
#             'category': 'Astronomía'
#         }
#     ]
#     return example_flashcards