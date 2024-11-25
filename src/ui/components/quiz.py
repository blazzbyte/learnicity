"""Quiz component for rendering and handling quiz interactions"""

import streamlit as st
from typing import List, Dict, Any

def init_quiz_states():
    """Initialize quiz-related session states"""
    if "start_quiz" not in st.session_state:
        st.session_state.start_quiz = False
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_results" not in st.session_state:
        st.session_state.quiz_results = []

def render_quiz(quiz_data: List[Dict[str, Any]]):
    """
    Render quiz interface with questions, options, and results
    
    Args:
        quiz_data (List[Dict[str, Any]]): List of quiz questions with options and answers
    """
    init_quiz_states()
    
    # Quiz container
    with st.container():
        if not st.session_state.quiz_completed:
            # Create placeholders for each question
            for i, question in enumerate(quiz_data):
                with st.container():
                    st.markdown(f"**Pregunta {i+1}**")
                    st.markdown(question['question'])
                    
                    # Display image if available
                    if 'image_url' in question:
                        try:
                            st.image(question['image_url'], caption="Imagen de referencia", width=500)
                        except Exception as e:
                            st.warning("No se pudo cargar la imagen de referencia.")
                    
                    # Radio buttons for options
                    answer_key = f"Q{i+1}"
                    if answer_key not in st.session_state:
                        st.session_state[answer_key] = None
                    
                    selected = st.radio(
                        "Selecciona tu respuesta:",
                        options=question['options'],
                        key=answer_key,
                        index=None
                    )
                    st.markdown("---")
            
            # Submit button
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("Enviar Respuestas ✨", use_container_width=True):
                    score = 0
                    results = []
                    all_answered = True
                    
                    for i, question in enumerate(quiz_data):
                        answer_key = f"Q{i+1}"
                        if answer_key in st.session_state:
                            user_answer = st.session_state[answer_key]
                            if user_answer is None:
                                all_answered = False
                                break
                            selected_index = question['options'].index(user_answer)
                            is_correct = selected_index == question['correct_answer']
                            if is_correct:
                                score += 1
                            results.append(is_correct)
                    
                    if not all_answered:
                        st.error("Por favor, responde todas las preguntas antes de enviar.")
                        return
                    
                    st.session_state.quiz_score = score
                    st.session_state.quiz_results = results
                    st.session_state.quiz_completed = True
                    
                    # Launch balloons for perfect score
                    if score == len(quiz_data):
                        st.balloons()
                    
                    st.rerun()
        
        else:            
            # Center the score with columns
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                score_percentage = (st.session_state.quiz_score / len(quiz_data)) * 100
                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 1rem; border-radius: 0.5rem; 
                    background-color: rgba(255, 140, 0, 0.1); margin: 1rem 0;'>
                        <h2 style='color: rgb(255, 140, 0); margin: 0;'>
                            Puntuación Final
                        </h2>
                        <div style='font-size: 2.5rem; font-weight: bold; color: rgb(255, 140, 0);'>
                            {st.session_state.quiz_score} / {len(quiz_data)}
                        </div>
                        <div style='font-size: 1.2rem; color: rgb(255, 140, 0);'>
                            {score_percentage:.0f}%
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Launch balloons for perfect score
                if score_percentage == 100:
                    st.balloons()

            # Show detailed feedback
            for i, (question, is_correct) in enumerate(zip(quiz_data, st.session_state.quiz_results)):
                with st.container():
                    st.markdown(f"**Pregunta {i+1}**")
                    st.markdown(question['question'])
                    
                    answer_key = f"Q{i+1}"
                    if answer_key in st.session_state:
                        user_answer = st.session_state[answer_key]
                        if is_correct:
                            st.success(f"✅ Tu respuesta: {user_answer}")
                        else:
                            st.error(f"❌ Tu respuesta: {user_answer}")
                            st.success(f"Respuesta correcta: {question['options'][question['correct_answer']]}")
                    
                    with st.expander("Ver explicación"):
                        st.markdown(question['explanation'])
                    
                    st.markdown("---")
            
            # Restart button
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("Return to Flashcards 📖", use_container_width=True):
                    # Clean up session state
                    for key in list(st.session_state.keys()):
                        if key.startswith("Q"):
                            del st.session_state[key]
                    
                    st.session_state.start_quiz = False
                    st.session_state.quiz_completed = False
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_results = []
                    st.rerun()
