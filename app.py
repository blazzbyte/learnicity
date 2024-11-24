import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

import pdfplumber, docx2txt
from src.core.config import config, logger

from src.llm.chains.search import SearchChain
from src.llm.chains.flashcard import FlashcardChain

from src.ui.components.st_init import st_init
from src.ui.components.st_states import init_session_states

from src.ui.components.sidebar import sidebar
from src.ui.components.header import header

from src.ui.components.search import search
from src.ui.components.flashcard import render_flashcards

def main():    
    # Initialize Streamlit components
    st_init()
    init_session_states()
    
    # Setup sidebar
    sidebar()
    
    # Setup header
    header()
    
    # Main content
    if st.session_state.get("input_text") is None:
        # Reset flashcards when returning to search
        if "generated_flashcards" in st.session_state:
            del st.session_state.generated_flashcards
        search()
    else:
        
        # Only generate flashcards if they haven't been generated yet
        if "flashcards" not in st.session_state:
            if st.session_state.get("input_text") is not None:
                query = st.session_state.get("input_text")
                search_chain = SearchChain()
                results = search_chain.process_queries(query)
                
                # Generate flashcards from search results
                flashcard_chain = FlashcardChain()
                flashcards = flashcard_chain.process_search_results(results)
                logger.parser(f"Generated Flashcards: {flashcards}")
                
                # Store flashcards in session state
                st.session_state.flashcards = flashcards
            # Handle file uploads
            elif st.session_state.get("uploaded_files") is not None:
                file: UploadedFile = st.session_state.get("uploaded_files")
                search_chain = SearchChain()
                all_content = {}

                try:
                    # Determine file type and read content accordingly
                    if file.type == 'text/plain':
                        all_content = {
                            "content": file.read().decode('utf-8'),
                            "metadata": {'file_name': file.name, 'file_type': file.type[:4]}
                        }
                    elif file.type == 'application/pdf':
                        with pdfplumber.open(file) as pdf:
                            text = ""
                            for page in pdf.pages:
                                text += page.extract_text()
                            all_content = {
                                "content": text,
                                "metadata": {'file_name': file.name, 'file_type': file.type[11:]}
                            }
                    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        all_content = {
                            "content": docx2txt.process(file),
                            "metadata": {'file_name': file.name, 'file_type': 'docx'}
                        }
                    elif file.type == "text/markdown":
                        all_content = {
                            "content": file.read().decode('utf-8'),
                            "metadata": {'file_name': file.name, 'file_type': file.type}
                        }
                except Exception as e:
                    logger.error(f"Error reading file {file.name}: {str(e)}")

                # Summarize content
                combined_content = all_content.get("content", "")
                summarized_content = search_chain.summarize_content(combined_content)

                # Format summarized content for flashcard generation
                formatted_results = [{
                    "query": "file_upload",  # Placeholder query
                    "type": "text",
                    "result": {
                        "content": summarized_content,
                        "title": all_content["metadata"]["file_name"],
                        "link": all_content["metadata"]["file_type"]  # No link for file content
                    }
                }]

                # Generate flashcards from formatted results
                flashcard_chain = FlashcardChain()
                flashcards = flashcard_chain.process_search_results(formatted_results)
                logger.info(f"Generated flashcards from files: {flashcards}")

                # Store flashcards in session state
                st.session_state.flashcards = flashcards

        # Render the stored flashcards
        render_flashcards(st.session_state.flashcards)

if __name__ == "__main__":
    main()
