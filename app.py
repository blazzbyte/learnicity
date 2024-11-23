import streamlit as st
import uuid

from src.core.config import logger

from src.ui.components.st_init import st_init
from src.ui.components.sidebar import sidebar

def main():
    # Initialize Streamlit Configuration
    st_init()
    
    # Sidebar
    sidebar()
    
    # Add a title
    st.title(f"Bienvenido a mi aplicación Streamlit")
    
    # Add flashcards section
    st.header("Flashcards")
    from src.ui.components.flashcard import render_flashcards
    render_flashcards()
    
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
