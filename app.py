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
        render_flashcards()

    # Add flashcards section
    # st.header("Flashcards")
    # render_flashcards()

    # # Main content
    # st.header("Contenido Principal")

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
