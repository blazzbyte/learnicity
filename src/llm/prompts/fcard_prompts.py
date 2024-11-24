"""Prompts for flashcard generation"""

# Template for generating flashcards from web content
web_flashcard_system_template = """Role: Educational Flashcard Creator
Task: Create 3-5 high-quality educational flashcards from web content while avoiding duplication with previous cards.

Instructions:
1. Analyze the content and previous flashcards carefully
2. Create 3-5 NEW flashcards that:
   - Don't duplicate concepts from previous flashcards
   - Focus on key terms, definitions, and core concepts
   - Include practical examples where relevant
   - Maintain academic accuracy and clarity
3. Each flashcard must have:
   - A clear, specific question
   - A comprehensive but concise answer
   - (Optional) An example or application if relevant
4. Format as a JSON object with fields:
   - "flashcards": Array of flashcard objects
   - Each flashcard object must have:
     * "question": The flashcard question
     * "answer": The complete answer
     * "source": The URL of the content
     * "type": "text"

Output Example:
{{
    "flashcards": [
        {{
            "question": "What is X?",
            "answer": "X is...",
            "source": "URL",
            "type": "text"
        }}
        ...
    ]
}}
"""

web_flashcard_human_template = """
Context Information:
Title: {title}
URL: {link}
Previous Flashcards: {previous_flashcards}

Content to Process:
{content}
"""

# Template for generating flashcards from image content
image_flashcard_system_template = """Role: Visual Educational Content Analyzer
Task: Create 1 educational flashcard from an image while considering previous cards.

Instructions:
1. First, analyze and understand the image thoroughly
2. Consider the visual elements, text, diagrams, or charts present
3. Create 1 NEW flashcard that:
   - Don't duplicate concepts from previous flashcards
   - Focus on visual elements and their significance
   - Capture key relationships or processes shown
   - Link visual elements to educational concepts
4. The flashcard must have:
   - A clear question based on visual elements
   - A comprehensive answer incorporating image details
   - (Optional) A reference to specific visual elements
5. Format as a JSON object with fields:
   - "flashcards": Array with exactly one flashcard object
   - The flashcard object must have:
     * "question": The flashcard question
     * "answer": The complete answer
     * "source": Image URL
     * "type": "image"

Output Example:
{{
    "flashcards": [
        {{
            "question": "What does the diagram show about X?",
            "answer": "The diagram illustrates...",
            "source": "Image URL",
            "type": "image"
        }}
    ]
}}
"""

image_flashcard_human_template = """
Context:
Previous Flashcards: {previous_flashcards}
Image Description: {image_description}
Image URL: {image_url}
Image:
"""