import streamlit as st
import asyncio
from src.core.config import logger
from src.data.db import db

async def init_db():
    """Initialize database connection"""
    try:
        await db.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        st.error("Failed to connect to database")

def main():
    # Set page config
    st.set_page_config(
        page_title="Learnicity",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    logger.info("Aplicación iniciada correctamente")
    
    # Add a title
    st.title("Bienvenido a mi aplicación Streamlit")
    
    # Add some text
    st.write("Esta es una aplicación base de Streamlit.")
    
    # Add a sidebar
    with st.sidebar:
        st.header("Sidebar")
        st.write("Puedes agregar controles aquí")
        logger.debug("Sidebar renderizado")
    
    # Main content
    st.header("Contenido Principal")
    
    # Example of some basic Streamlit components
    nombre = st.text_input("Ingresa tu nombre:")
    if nombre:
        logger.info(f"Usuario ingresó el nombre: {nombre}")
        st.write(f"¡Hola, {nombre}!")
    
    # Add a button
    if st.button("Haz click aquí"):
        try:
            st.balloons()
            st.success("¡Gracias por hacer click!")
            logger.info("Usuario hizo click en el botón principal")
        except Exception as e:
            logger.error(f"Error al procesar el click del botón: {str(e)}")

if __name__ == "__main__":
    logger.info("Iniciando aplicación Learnicity")
    asyncio.run(init_db())
    main()
