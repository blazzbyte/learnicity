import streamlit as st
from typing import List, Dict, Any, Optional
from src.core.config import get_translation

def render_card_content(text: str, image_url: str = None, card_type: str = "text") -> str:
    """Render the content of a flashcard side
    
    Args:
        text (str): The text content
        image_url (str, optional): URL of an image
        card_type (str): Type of card ("text" or "image")
    """
    content = []
    
    # For image cards, show image only on question side
    if card_type == "image" and image_url:
        content.append(f'<img src="{image_url}" alt="{text}" style="max-width: 100%; height: auto;">')
    
    # Always show the text
    if text:
        content.append(f'<div style="margin-top: 10px;">{text}</div>')
    
    # Join all content and wrap in content div
    return f'<div class="content">{"".join(content)}</div>'

def render_source(source: Optional[str]) -> str:
    """Render the source link if it's a valid HTTPS URL
    
    Args:
        source (Optional[str]): The source URL
        
    Returns:
        str: HTML for the source link or empty string if invalid
    """
    if source and source.startswith('https://'):
        return f'<div class="flashcard-source"><a href="{source}" target="_blank">{get_translation("Reference")}</a></div>'
    return ""

def render_flashcards(flashcards: List[Dict[str, Any]]):
    """Render flashcards with navigation controls
    
    Args:
        flashcards (List[Dict[str, Any]]): List of flashcard dictionaries. Each flashcard should have:
            - question (str): The question text
            - answer (str): The answer text
            - source (str): The source URL (used as image URL for image cards)
            - type (str): Type of flashcard ("text" or "image")
    """
    if not flashcards:
        st.warning(get_translation("Could not generate cards to display."))
        return
    
    if 'current_card' not in st.session_state:
        st.session_state.current_card = 0
    
    if 'is_flipped' not in st.session_state:
        st.session_state.is_flipped = False
    
    card = flashcards[st.session_state.current_card]
    card_type = card.get('type', 'text')

    # Render the flashcard
    st.markdown(f'''
        <div class="flashcard-container">
            <div class="flashcard {'flipped' if st.session_state.is_flipped else ''}">
                <div class="flashcard-front">
                    {render_card_content(
                        card['question'],
                        card['source'] if card_type == 'image' else None,
                        card_type
                    )}
                    {render_source(card.get('source'))}
                </div>
                <div class="flashcard-back">
                    {render_card_content(card['answer'])}
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Show progress
    st.markdown(
        f'<p style="text-align: center">{get_translation("Tarjeta {current_card} de {all_cards}").format(current_card=st.session_state.current_card + 1, all_cards=len(flashcards))}</p>', 
        unsafe_allow_html=True
    )
    
    # Navigation buttons
    st.markdown('<div class="navigation-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button(get_translation('← Previous'), use_container_width=True):
            st.session_state.current_card = (st.session_state.current_card - 1) % len(flashcards)
            st.session_state.is_flipped = False
            st.rerun()
    
    with col2:
        if st.button(get_translation('Flip card'), use_container_width=True):
            st.session_state.is_flipped = not st.session_state.is_flipped
            st.rerun()
    
    with col3:
        if st.button(get_translation('Next →'), use_container_width=True):
            st.session_state.current_card = (st.session_state.current_card + 1) % len(flashcards)
            st.session_state.is_flipped = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Example usage
if __name__ == "__main__":
    example_flashcards = [
        {
            'question': '¿Qué muestra el diagrama sobre la indexación vectorial?',
            'answer': 'El diagrama ilustra el proceso de indexación vectorial, que implica crear una representación vectorial de datos y almacenarla en una base de datos para una recuperación eficiente.',
            'source': 'https://miro.medium.com/v2/resize:fit:1200/0*naaZxK2f3qQ2hiDp.png',
            'type': 'image'
        }
    ]
    render_flashcards(example_flashcards)