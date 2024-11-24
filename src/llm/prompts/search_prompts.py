# Query Refinement Prompt
refine_query_template = """
Role: Educational Content Expert
Goal: Refine a learning query to make it more specific and educational
Instructions:
1. Create a more detailed and focused search query
2. Keep the core learning intent
3. Focus on educational and factual content
4. Make it suitable for academic sources

Original query: {query}
Refined query:"""

# Multiple Queries Generation Prompt
generate_queries_template = """
Role: Educational Content Researcher
Goal: Generate diverse search queries to explore a topic thoroughly
Instructions:
1. Generate {num_queries} search queries that follow a pedagogical progression:
   - Start with fundamental definitions and basic concepts
   - Progress to intermediate understanding and relationships
   - End with advanced applications and deeper insights
2. Each query should build upon the previous one
3. Focus on creating a logical learning sequence
4. Make queries accessible and educational
5. Ensure queries are suitable for creating a comprehensive lesson
6. Only use text or image types
7. Return the queries in the following JSON format:
   {{
       "queries": [
           {{
               "query": "first query",
               "type": "text"
           }},
           {{
               "query": "second query",
               "type": "text"
           }},
           {{
               "query": "third query",
               "type": "image"
           }},
           ...
       ]
   }}

Example:
   {{
       "queries": [
           {{
               "query": "What is Vector Store?",
               "type": "text"
           }},
           {{
               "query": "Fundamental concepts of Vector Store",
               "type": "text"
           }},
           {{
               "query": "Representation of Similarity Search",
               "type": "image"
           }},
       ]
   }}

Visual Search Tip:
- Use terms like "diagram", "labeled diagram", "anatomical illustration", "equation", "formula", "mathematical representation", "process diagram", "step-by-step illustration", "visual explanation", "labeled parts", "component diagram", "structural breakdown"

Topic: {query}
{num_queries} Generated Queries:"""

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

queries_generator_template = """
        Role: 
        Generate {num_queries} different search queries to learn about this topic from different angles:
        Topic: {query}
        Focus on educational and factual content. Make queries specific and varied.
        Queries:"""
