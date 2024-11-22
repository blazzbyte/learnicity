import streamlit as st

def main():
    # Set page config
    st.set_page_config(
        page_title="Learnicity",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add a title
    st.title("Bienvenido a mi aplicación Streamlit")
    
    # Add some text
    st.write("Esta es una aplicación base de Streamlit.")
    
    # Add a sidebar
    with st.sidebar:
        st.header("Sidebar")
        st.write("Puedes agregar controles aquí")
    
    # Main content
    st.header("Contenido Principal")
    
    # Example of some basic Streamlit components
    nombre = st.text_input("Ingresa tu nombre:")
    if nombre:
        st.write(f"¡Hola, {nombre}!")
    
    # Add a button
    if st.button("Haz click aquí"):
        st.balloons()
        st.success("¡Gracias por hacer click!")

if __name__ == "__main__":
    main()
