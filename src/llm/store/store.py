import os
from pathlib import Path
from typing import List, Dict, Optional
from uuid import uuid4

from langchain_community.embeddings import JinaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from chromadb.config import Settings
from dotenv import load_dotenv


def create_chroma_instance(collection_name: str, user_id: str="test_user") -> Chroma:


    """Creates a Chroma vectorstore instance with default parameters."""

    persist_directory = os.path.join(os.getcwd(), "src", "llm", "Temp", user_id)
    Path(persist_directory).mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    embeddings = JinaEmbeddings()  # Or any other embedding model

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )
    return vector_store


def add_documents(
    vector_store: Chroma, documents: List[Document], ids: Optional[List[str]] = None
) -> List[str]:
    """Adds documents to the vectorstore."""
    if ids is None:
        ids = [str(uuid4()) for _ in range(len(documents))]

    return vector_store.add_documents(documents=documents, ids=ids)


def update_documents(
    vector_store: Chroma,
    ids: List[str],
    documents: List[Document],
) -> None:
    """Updates documents in the vectorstore."""
    vector_store.update_documents(ids=ids, documents=documents)


def delete_documents(vector_store: Chroma, ids: List[str]) -> None:
    """Deletes documents from the vectorstore."""

    vector_store.delete(ids=ids)


# def get_documents(vector_store: Chroma, ids: List[str]) -> List[Document]:
#     """Gets documents from the vectorstore by IDs."""
    
#     return vector_store.get_by_ids(ids)



def similarity_search(
    vector_store: Chroma, query: str, k: int = 4, filter: Optional[Dict[str, str]] = None  # Add filter parameter
) -> List[Document]:  # Updated return type hint
    """Performs a similarity search."""

    return vector_store.similarity_search(query=query, k=k, filter=filter) # Use filter in the search

if __name__ == "__main__":

    load_dotenv()
    # Example Usage:
    collection_name = "my_documents"
    vector_store = create_chroma_instance(collection_name)

    # Sample Documents
    document1 = Document(page_content="This is document 1", metadata={"source": "wiki"})
    document2 = Document(page_content="This is another document", metadata={"source": "blog"})


    # Add documents
    added_ids = add_documents(vector_store, [document1, document2])
    print(f"Added document IDs: {added_ids}")


    # # Get Documents
    # retrieved_docs = get_documents(vector_store, added_ids)
    # print(f"Retrieved Documents: {retrieved_docs}")

    # Update a document
    updated_document1 = Document(
        page_content="This is document 1, updated", metadata={"source": "wiki"}
    )

    update_documents(vector_store, [added_ids[0]], [updated_document1])


    # Similarity Search
    search_results = similarity_search(vector_store, "document", k=2)
    print(f"Search Results: {search_results}")

    # Similarity Search with filter
    search_results_filtered = similarity_search(vector_store, "document", k=2, filter={"source":"wiki"})
    print(f"Filtered Search Results: {search_results_filtered}")


    # Delete a document
    delete_documents(vector_store, [added_ids[1]])