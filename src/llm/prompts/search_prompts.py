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
