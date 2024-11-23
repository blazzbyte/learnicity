from src.ui.components.flashcard import render_flashcards
from src.llm.chains.search import search_chain
import streamlit as st
import uuid

from src.core.config import logger

from src.ui.components.st_init import st_init
from src.ui.components.st_states import init_session_states
from src.ui.components.sidebar import sidebar
from src.ui.components.header import header
from src.ui.components.search import search

# Example flashcards data with images
example_flashcards = [
    {
        'question': '¿Cuál es la capital de Francia?',
        'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
        'answer': 'París',
        'answer_image': None,
        'category': 'Geografía'
    },
    {
        'question': '¿Qué es H2O?',
        'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/H2O_2D_labelled.svg/1200px-H2O_2D_labelled.svg.png',
        'answer': 'Agua (dos átomos de hidrógeno y uno de oxígeno)',
        'answer_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Water_molecule_3D.svg/1200px-Water_molecule_3D.svg.png',
        'category': 'Química'
    },
    {
        'question': '¿Quién escribió "Cien años de soledad"?',
        'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
        'answer': 'Gabriel García Márquez',
        'answer_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
        'category': 'Literatura'
    },
    {
        'question': '¿Cuál es el planeta más grande del sistema solar?',
        'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Jupiter_and_its_shrunken_Great_Red_Spot.jpg/1200px-Jupiter_and_its_shrunken_Great_Red_Spot.jpg',
        'answer': 'Júpiter',
        'answer_image': None,
        'category': 'Astronomía'
    }
]

def main():
    # Initialize Streamlit Configuration
    st_init()

    # Initialize session states
    init_session_states()

    # Sidebar
    sidebar()

    header()

    # Search
    if st.session_state.get("input_text") is None:
        search()
    else:
        query = st.session_state.get("input_text")
        flashcards = search_chain()
        render_flashcards(example_flashcards)

    # # Add a button
    # if st.button("Haz click aquí"):
    #     try:
    #         st.balloons()
    #         st.success("¡Gracias por hacer click!")
    #         logger.info("Usuario hizo click en el botón principal")
    #     except Exception as e:
    #         logger.error(f"Error al procesar el click del botón: {str(e)}")


if __name__ == "__main__":
    main()
