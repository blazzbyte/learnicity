import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()


def get_openai_chat_model(model_name: str) -> ChatOpenAI:
    """
    Initializes and returns a ChatOpenAI language model.

    This function reads the OpenAI API key and base URL from environment
    variables. It's recommended to set these environment variables for
    secure access to the OpenAI API.

    Environment Variables:
        OPENAI_API_KEY: Your OpenAI API key.
        OPENAI_BASE_URL: (Optional) The base URL for the OpenAI API
                         if you're using a proxy or custom endpoint.
        OPENAI_ORG_ID: (Optional) Your OpenAI organization ID.

    Returns:
        ChatOpenAI: An initialized ChatOpenAI object ready for use.

    Raises:
        ValueError: If the OPENAI_API_KEY environment variable is not set.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        raise ValueError("The OPENAI_API_KEY environment variable must be set.")

    # Initialize ChatOpenAI with parameters
    llm = ChatOpenAI(
        name=model_name,
        model_name=model_name,
        temperature=0.3,  # Example value
        max_tokens=256,  # Example value
        timeout=30,  # Example value
        max_retries=3,  # Example value
        openai_api_key=api_key,
        base_url=base_url,
    )

    return llm

if __name__ == "__main__":
# Example usage:
    model_name = "llama3.1-8b"  # Replace with your actual model name
    model = get_openai_chat_model(model_name)
    response = model.invoke("Hello, how are you?")
    print(response)
