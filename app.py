import streamlit as st
from src.core.config import logger, get_translation

from src.llm.chains.search import SearchChain
from src.llm.chains.flashcard import FlashcardChain
from src.llm.chains.quiz import QuizChain

from src.ui.components.st_init import st_init
from src.ui.components.st_states import init_session_states

from src.ui.components.sidebar import sidebar
from src.ui.components.header import header

from src.ui.components.search import search
from src.ui.components.flashcard import render_flashcards
from src.ui.components.quiz import render_quiz

def main():    
    # Initialize Streamlit components
    st_init()
    init_session_states()
    
    # Setup sidebar and header
    sidebar()
    header()

    # Main content
    if "input_text" not in st.session_state and "file_content" not in st.session_state:
        # Reset flashcards when returning to search
        if "generated_flashcards" in st.session_state:
            del st.session_state.generated_flashcards
        search()
    else:
        # Generate flashcards if needed
        if "generated_flashcards" not in st.session_state:
            search_chain = SearchChain()
            
            if "file_content" in st.session_state and st.session_state.file_content:
                # Process uploaded file content
                content = st.session_state.file_content
                summarized_content = search_chain.summarize_content(content["content"])
                
                # Format summarized content for flashcard generation
                formatted_results = [{
                    "query": "file_upload",
                    "type": "text",
                    "result": {
                        "content": summarized_content,
                        "title": content["metadata"]["file_name"],
                        "link": content["metadata"]["file_type"]
                    }
                }]
            else:
                # Process search query
                query = st.session_state.input_text
                formatted_results = search_chain.process_queries(query)
            
            # Generate flashcards
            flashcard_chain = FlashcardChain()
            flashcards = flashcard_chain.process_search_results(formatted_results)
            logger.parser(f"Generated Flashcards: {flashcards}")
            
            # Store flashcards in session state
            st.session_state.generated_flashcards = flashcards
        
        # Render content based on state
        if "start_quiz" in st.session_state and st.session_state.start_quiz:
            # Generate quiz if starting
            if "generated_quiz" not in st.session_state:
                if st.session_state.generated_flashcards:
                    quiz_chain = QuizChain()
                    quiz = quiz_chain.create_quiz(st.session_state.generated_flashcards)
                    logger.parser(f"Generated Quiz: {quiz}")
                    st.session_state.generated_quiz = quiz
                    st.rerun()
                else:
                    st.error(get_translation("No flashcards available to generate the quiz."))
                    st.session_state.start_quiz = False
                    st.rerun()
            
            # Render quiz
            if "generated_quiz" in st.session_state and st.session_state.generated_quiz:
                render_quiz(st.session_state.generated_quiz)
            else:
                st.error(get_translation("Unable to generate the quiz. Please try again."))
                st.session_state.start_quiz = False
                st.rerun()
        else:
            # Render flashcards and quiz button
            render_flashcards(st.session_state.generated_flashcards)
            
            # Quiz Initial Options
            if st.session_state.generated_flashcards:
                st.markdown("---")
                st.markdown(get_translation("### Ready to test your knowledge?"))
                st.markdown("<style>h3{text-align: center;}</style>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    if st.button(get_translation("Start Quiz 🎯"), use_container_width=True):
                        st.session_state.start_quiz = True
                        st.rerun()

if __name__ == "__main__":
    main()
