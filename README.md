# Learnicity

A multimodal AI learning assistant powered by LLAMA models and intelligent web content analysis.

## Overview

Learnicity is an advanced learning platform that combines multimodal AI with web search to create an interactive learning experience:

- **Content Extraction**: Automatically extracts and analyzes content from web searches
- **Smart Learning Flow**: 
  1. Content Analysis & Summarization
  2. Interactive Flashcard Generation
  3. Knowledge Assessment through Quizzes
- **Multimodal Understanding**: Processes both text and visual content for comprehensive learning

## Core Features

- **Intelligent Web Analysis**:
  - Smart web content extraction
  - YouTube video understanding
  - Multimodal content processing (text + visual)

- **Learning Tools**:
  - Auto-generated flashcards from web content
  - Interactive study sessions
  - Progress tracking
  - Knowledge assessment quizzes

- **AI-Powered Features**:
  - Content summarization
  - Key concept extraction
  - Dynamic quiz generation
  - Learning progress analysis

## Tech Stack

- Python 3.11+
- Poetry for dependency management
- Prisma ORM
- Streamlit for UI
- LLAMA 3.2 and 3.1 Models
- ChromaDB for vector Store
- SQLite for user data

## Getting Started

### Installation

1. Clone the repository and navigate to the project directory:
```bash
git clone <repository-url>
cd learnicity
```

2. Install dependencies with Poetry:
```bash
poetry install
```

3. Set up environment variables:
```bash
# Create .env file with necessary API keys
cp .env.example .env
```

### Database Setup

1. Generate Prisma client:
```bash
prisma generate --schema src/data/db/schema.prisma
```

2. Push database schema:
```bash
prisma db push --schema src/data/db/schema.prisma
```

### Running the Application

1. Activate Poetry shell:
```bash
poetry shell
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Learning Flow

1. **Content Discovery**
   - Enter your learning topic
   - AI-powered web search extracts relevant content
   - Multimodal analysis of text and visual content

2. **Study Phase**
   - Review AI-generated summaries
   - Practice with interactive flashcards
   - Track your understanding

3. **Assessment**
   - Take dynamically generated quizzes
   - Get instant feedback
   - Identify areas for review

## Contributing

See [TODO.md](TODO.md) for planned improvements and features.