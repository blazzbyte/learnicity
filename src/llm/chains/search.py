import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

from dotenv import load_dotenv

# Set up OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


# We define the chatprompt template with the input variable "topic"
chat_prompt = ChatPromptTemplate.from_messages(
     [
      SystemMessage(content="You are a helpful assistant that generates queries based on a given topic."), 
      HumanMessage(content="Generate a JSON list object of five similar queries based on the following topic: {topic}"),
      ])


# Set up the JSON output parser
parser = JsonOutputParser()

# Instantiate the ChatOpenAI model
model = ChatOpenAI(
    model="Meta-Llama-3.1-8B-Instruct",
    api_key=api_key,
    base_url=base_url,
    temperature=0)

# Create the chain
chain = chat_prompt | model | parser

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    # Invoke the chain with user input
    user_input = "Artificial Intelligence"  # Example user input
    result = chain.invoke({"topic": user_input})
    print(result)
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