import streamlit as st
from src.core.config import get_translation

def header():
    # Add a title
    st.title(get_translation('Learn Faster with Learnicity:books:'))
    st.markdown(
        '<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
    if 'input_text' not in st.session_state and 'file_content' not in st.session_state:
        st.subheader(
            get_translation('Turn any topic into flashcards, quizzes, and personalized resources to master it effortlessly.'))
        st.markdown('<style>h3{text-align: center;}</style>', unsafe_allow_html=True)
    else:
        st.markdown("""<style>.ea3mdgi5{padding: 2rem 5rem;}</style>""", unsafe_allow_html=True)
