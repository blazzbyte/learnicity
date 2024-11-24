import streamlit as st
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
            query = st.session_state.get("input_text")
            search_chain = SearchChain()
            results = search_chain.process_queries(query)
            
            # Generate flashcards from search results
            flashcard_chain = FlashcardChain()
            flashcards = flashcard_chain.process_search_results(results)
            logger.parser(f"Generated Flashcards: {flashcards}")
            
            # Store flashcards in session state
            st.session_state.flashcards = flashcards
        
        # Render the stored flashcards
        render_flashcards(st.session_state.flashcards)

if __name__ == "__main__":
    main()
