# Flashcard Creation Prompt
flashcard_template = """
Role: Educational Content Creator
Goal: Create educational flashcards from academic content
Instructions:
1. Generate flashcards that test important concepts
2. Each flashcard must have:
   - Clear, specific question
   - Concise but complete answer
   - Relevant academic category
   - Optional image URLs (null if not relevant)
3. Format in exact JSON structure:
   [
       {
           "question": "Question text",
           "answer": "Answer text",
           "category": "Subject category",
           "question_image": "URL or null",
           "answer_image": "URL or null"
       }
   ]
4. Create 3-5 high-quality flashcards
5. Focus on key concepts and learning objectives

Content: {content}"""

# Content Summary Prompt
summarize_template = """
Role: Academic Content Summarizer
Goal: Create a concise summary of educational content
Instructions:
1. Identify key concepts and main ideas
2. Maintain academic accuracy
3. Keep educational value
4. Focus on facts and definitions
5. Preserve important examples

Content: {content}
Summary:"""