import streamlit as st

# Example flashcards data with images
example_flashcards = [
    {
        'question': '¿Cuál es la capital de Francia?',
        'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
        'answer': 'París',
        'answer_image': None,
        'category': 'Geografía'
    },
    {
        'question': '¿Qué es H2O?',
        'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/H2O_2D_labelled.svg/1200px-H2O_2D_labelled.svg.png',
        'answer': 'Agua (dos átomos de hidrógeno y uno de oxígeno)',
        'answer_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Water_molecule_3D.svg/1200px-Water_molecule_3D.svg.png',
        'category': 'Química'
    },
    {
        'question': '¿Quién escribió "Cien años de soledad"?',
        'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
        'answer': 'Gabriel García Márquez',
        'answer_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/1200px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg',
        'category': 'Literatura'
    },
    {
        'question': '¿Cuál es el planeta más grande del sistema solar?',
        'question_image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Jupiter_and_its_shrunken_Great_Red_Spot.jpg/1200px-Jupiter_and_its_shrunken_Great_Red_Spot.jpg',
        'answer': 'Júpiter',
        'answer_image': None,
        'category': 'Astronomía'
    }
]

def render_card_content(text, image_url=None):
    content = f'<div class="content">'
    if text:
        content += f'<div>{text}</div>'
    if image_url:
        content += f'<img src="{image_url}" alt="{text}">'
    content += '</div>'
    return content

def render_flashcards():
    
    if 'current_card' not in st.session_state:
        st.session_state.current_card = 0
    
    if 'is_flipped' not in st.session_state:
        st.session_state.is_flipped = False
    
    card = example_flashcards[st.session_state.current_card]
    
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
    
    # Navigation buttons below the card
    st.markdown('<div class="navigation-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button('← Anterior', use_container_width=True):
            st.session_state.current_card = (st.session_state.current_card - 1) % len(example_flashcards)
            st.session_state.is_flipped = False
            st.rerun()
    
    with col2:
        if st.button('Voltear', use_container_width=True):
            st.session_state.is_flipped = not st.session_state.is_flipped
            st.rerun()
    
    with col3:
        if st.button('Siguiente →', use_container_width=True):
            st.session_state.current_card = (st.session_state.current_card + 1) % len(example_flashcards)
            st.session_state.is_flipped = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show progress
    st.markdown(f'<p style="text-align: center">Tarjeta {st.session_state.current_card + 1} de {len(example_flashcards)}</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_flashcards()
