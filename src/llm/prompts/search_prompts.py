# Multiple Queries Generation Prompt
queries_system_template = """
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
6. Only two types are allowed: "text" or "image"
7. Return the queries in the following JSON format:
   {{
       "queries": [
           {{
               "query": "first query",
               "type": "text"
           }},
           {{
               "query": "second query",
               "type": "image"
           }},
           ...
       ]
   }}

Output Example:
   {{
       "queries": [
           {{
               "query": "A query about X",
               "type": "text"
           }},
           {{
               "query": "A query related to X that needs an image",
               "type": "image"
           }},
           ...
       ]
   }}

Visual Search Tip:
- Use terms like "diagram", "labeled diagram", "anatomical illustration", "equation", "formula", "mathematical representation", "process diagram", "step-by-step illustration", "visual explanation", "labeled parts", "component diagram", "structural breakdown"
"""

queries_human_template = """
Topic: {query}
{num_queries} Generated Queries:"""
