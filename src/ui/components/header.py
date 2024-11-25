import streamlit as st

def header():
    # Add a title
    st.title('Learn Faster with Learnicity:books:')
    st.markdown(
        '<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
    if 'input_text' not in st.session_state:
        st.subheader(
            'Turn any topic into flashcards, quizzes, and personalized resources to master it effortlessly.')
        st.markdown(
            '<style>h3{text-align: center;}</style>', unsafe_allow_html=True)
