import os
import asyncio
import aiohttp
import json
from typing import List, Dict, Any

async def fetch_url(url: str, headers: Dict[str, str] = None, session: aiohttp.ClientSession = None) -> Dict[str, Any]:
    """Fetches data from a single URL asynchronously."""
    if headers is None:
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv('JINA_API_kEY')}",  # Replace with actual token if needed
            "X-Retain-Images": "none"
        }
    async with session.get(url, headers=headers) as response:
        try:
            response.raise_for_status()
            if response.headers['Content-Type'] == 'application/json':
                data = await response.json()
            else:
                data = await response.text()
            return {"url": url, "data": data}
        except aiohttp.ClientError as e:
            return {"url": url, "error": str(e)}
        except json.JSONDecodeError as e:
            return {"url": url, "error": f"JSON decoding error: {e}"}
        except KeyError as e:
            return {"url": url, "error": f"Missing key in response headers: {e}"}
        except Exception as e:
            return {"url": url, "error": f"An unexpected error occurred: {e}"}

def fetch_urls(urls: List[str], headers: Dict[str, str] = None) -> List[Dict[str, Any]]:
    """
    Fetches data from a list of URLs synchronously, using asynchronous requests internally.

    Args:
        urls: A list of URLs to fetch data from.
        headers: A dictionary of HTTP headers to include in the requests.

    Returns:
        A list of dictionaries, where each dictionary contains the response data for a URL.
        If an error occurs for a URL, the dictionary will contain an 'error' key with the error message.
    """
    if not isinstance(urls, list):
        raise TypeError("urls must be a list")
    if not urls:
        raise ValueError("urls cannot be empty")
    links = ["https://r.jina.ai/" + url for url in urls]
    async def run_async():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(url, headers, session) for url in links]
            results = await asyncio.gather(*tasks)
            return results

    return asyncio.run(run_async())

def main(urls: List[str]):
    """
    Main function to fetch data from a list of URLs synchronously.

    Args:
        urls: A list of URLs to fetch data from.

    Prints:
        The response data or error for each URL.
    """
    try:
        results = fetch_urls(urls)
        print("\033[32;1m" + str(type(results)) + "\033[0m")
        for result in results:
            if 'error' in result:
                print(f"Error fetching {result['url']}: {result['error']}")
            else:
                print("\033[31;1m" + str(type(result)) + "\033[0m")
                print(f"Data from {result['url']}:\n\n {result['data']}")
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()

    # Example usage
    urls_to_fetch = [
        "https://example.com",
        "https://docs.cohere.com/docs/multimodal-embeddings",
        # "https://python.langchain.com/docs/integrations/document_loaders/"  # Add more URLs as needed
    ]
    main(urls_to_fetch)