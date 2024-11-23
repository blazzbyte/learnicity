from dotenv import load_dotenv
from langchain_community.embeddings import JinaEmbeddings

def initialize_embeddings(model_name: str = "jina-embeddings-v2-base-en") -> JinaEmbeddings:
    """
    Initialize Jina embeddings with the specified model name.
    All other parameters are set with default values.
    
    Args:
        model_name: Name of Jina model to use (default is "jina-embeddings-v2-base-en")
    
    Returns:
        JinaEmbeddings: Configured embeddings instance
    """
    
    # Initialize embeddings with all parameters explicitly set
    embeddings = JinaEmbeddings(
                    model_name=model_name,
                    # dimensions=None,
                    # api_key=SecretStr(api_key) if api_key else None,
                    # max_retries=2,
                    # timeout=None,
                    # show_progress_bar=False,
                    # chunk_size=1000,
                    # embedding_ctx_length=8191,
                    # retry_min_seconds=4,
                    # retry_max_seconds=20
                )
    
    return embeddings

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Test with a different model
    custom_embeddings = initialize_embeddings("jina-clip-v2")
    print(f"Initialized embeddings with custom model: {custom_embeddings.model_name}")
    text = "LangChain is the framework for building context-aware reasoning applications"
    single_vector = custom_embeddings.embed_query(text)
    print(str(single_vector)[:100])  # Show the first 100 characters of the vector