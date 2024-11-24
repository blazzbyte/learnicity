import streamlit as st


def search():
    col1, col2 = st.columns([14, 1], vertical_alignment="bottom")
    st.markdown('<style>.stColumn .stButton{text-align: end;}</style>', unsafe_allow_html=True)
    with col1:
        input_text = st.text_input("Search for topic you want to learn:", key="query_input")
    with col2:
        if st.button("Buscar", key="search_button"):
            st.session_state["input_text"] = input_text
            st.rerun()

    uploaded_files = st.file_uploader(
        "Or upload your own file:", accept_multiple_files=False, type=["pdf", "docx", "txt", "md"], key="file_uploader", help="Load your own file to convert them into Flashcards. Supported formats: PDF, DOCX, TXT, MD"
    )

    if uploaded_files:
        st.session_state["uploaded_files"] = uploaded_files
        st.rerun()