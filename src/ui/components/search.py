import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import pdfplumber
import docx2txt
from src.core.config import logger, get_translation

def process_file_content(file: UploadedFile) -> dict:
    """Process uploaded file content based on file type"""
    try:
        if file.type == 'text/plain':
            return {
                "content": file.read().decode('utf-8'),
                "metadata": {'file_name': file.name, 'file_type': file.type[:4]}
            }
        elif file.type == 'application/pdf':
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                return {
                    "content": text,
                    "metadata": {'file_name': file.name, 'file_type': file.type[11:]}
                }
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return {
                "content": docx2txt.process(file),
                "metadata": {'file_name': file.name, 'file_type': 'docx'}
            }
        elif file.type == "text/markdown":
            return {
                "content": file.read().decode('utf-8'),
                "metadata": {'file_name': file.name, 'file_type': file.type}
            }
    except Exception as e:
        logger.error(f"Error reading file {file.name}: {str(e)}")
        return None
    return None

def search():
    col1, col2 = st.columns([9, 1], vertical_alignment="bottom")
    st.markdown('<style>.stColumn .stButton{text-align: end;}</style>', unsafe_allow_html=True)
    
    with col1:
        input_text = st.text_input(get_translation("Search for topic you want to learn:"), key="query_input")
    with col2:
        if st.button(get_translation("Search"), key="search_button", use_container_width=True):
            st.session_state["input_text"] = input_text
            st.rerun()

    uploaded_file = st.file_uploader(
        get_translation("Or upload your own file:"),
        accept_multiple_files=False, 
        type=["pdf", "docx", "txt", "md"], 
        key="file_uploader", 
        help=get_translation("Load your own file to convert them into Flashcards. Supported formats: PDF, DOCX, TXT, MD")
    )

    if uploaded_file:
        st.session_state["uploaded_file"] = uploaded_file
        st.session_state["file_content"] = process_file_content(uploaded_file)
        st.rerun()