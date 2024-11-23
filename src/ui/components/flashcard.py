import streamlit as st
from typing import List, Dict, Any

def render_card_content(text, image_url=None):
    content = f'<div class="content">'
    if text:
        content += f'<div>{text}</div>'
    if image_url:
        content += f'<img src="{image_url}" alt="{text}">'
    content += '</div>'
    return content

def render_flashcards(flashcards: List[Dict[str, Any]]):
    """Render flashcards with navigation controls
    
    Args:
        flashcards (List[Dict[str, Any]]): List of flashcard dictionaries. Each flashcard should have:
            - question (str): The question text
            - answer (str): The answer text
            - category (str): The category of the flashcard
            - question_image (str, optional): URL of the question image
            - answer_image (str, optional): URL of the answer image
    """
    if not flashcards:
        st.warning("No hay tarjetas para mostrar.")
        return
    
    if 'current_card' not in st.session_state:
        st.session_state.current_card = 0
    
    if 'is_flipped' not in st.session_state:
        st.session_state.is_flipped = False
    
    card = flashcards[st.session_state.current_card]
    
    # Render the flashcard
    st.markdown(f'''
        <div class="flashcard-container" onclick="this.querySelector('.flashcard').classList.toggle('flipped')">
            <div class="flashcard {'flipped' if st.session_state.is_flipped else ''}">
                <div class="flashcard-front">
                    <div class="category">{card['category']}</div>
                    {render_card_content(card['question'], card.get('question_image'))}
                </div>
                <div class="flashcard-back">
                    <div class="category">{card['category']}</div>
                    {render_card_content(card['answer'], card.get('answer_image'))}
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Show progress
    st.markdown(f'<p style="text-align: center">Tarjeta {st.session_state.current_card + 1} de {len(flashcards)}</p>', unsafe_allow_html=True)
    
    # Navigation buttons below the card
    st.markdown('<div class="navigation-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button('← Anterior', use_container_width=True):
            st.session_state.current_card = (st.session_state.current_card - 1) % len(flashcards)
            st.session_state.is_flipped = False
            st.rerun()
    
    with col2:
        if st.button('Voltear', use_container_width=True):
            st.session_state.is_flipped = not st.session_state.is_flipped
            st.rerun()
    
    with col3:
        if st.button('Siguiente →', use_container_width=True):
            st.session_state.current_card = (st.session_state.current_card + 1) % len(flashcards)
            st.session_state.is_flipped = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Example usage
if __name__ == "__main__":
    example_flashcards = [
        {
            'question': '¿Cuál es la capital de Francia?',
            'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
            'answer': 'París',
            'answer_image': None,
            'category': 'Geografía'
        }
    ]
    render_flashcards(example_flashcards)