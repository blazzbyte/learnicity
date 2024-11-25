import os
from langchain_openai import ChatOpenAI
from src.core.config import config

def get_openai_chat_model(model_name: str, max_tokens : int = 1024) -> ChatOpenAI:
    """
    Initializes and returns a ChatOpenAI language model.

    This function gets the OpenAI API key and base URL from the application's
    configuration. The configuration is managed through the core.config module.

    Args:
        model_name (str): Name of the model to use (e.g., "Meta-Llama-3.1-8B-Instruct")

    Returns:
        ChatOpenAI: An initialized ChatOpenAI object ready for use.

    Raises:
        ValueError: If the OpenAI credentials are not properly configured.
    """
    
    # Get credentials from config
    config.reload()
    api_key, base_url = config.get_openai_credentials()

    if not api_key:
        raise ValueError("OpenAI API key is not configured in the application settings.")

    # Initialize ChatOpenAI with parameters
    llm = ChatOpenAI(
        name=model_name,
        model_name=model_name,
        temperature=0.3,
        max_tokens=max_tokens,
        timeout=config.get_inference_timeout(),
        max_retries=3,
        openai_api_key=api_key,
        base_url=base_url if base_url else None,
    )

    return llm

if __name__ == "__main__":
    # Example usage:
    model = get_openai_chat_model("Meta-Llama-3.1-8B-Instruct")
    response = model.predict("Tell me about Llama models.")
    print(response)
