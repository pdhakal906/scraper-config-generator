import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
from langchain_openai import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_categories_from_url(url: str) -> dict:
    """
    Extract categories from a news website URL.

    Args:
        url (str): The URL of the news website to analyze

    Returns:
        dict: A dictionary containing the categories and their URLs
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=OPENAI_API_KEY,
    )

    res = requests.get(url)
    html = res.text

    # Define the response schema
    urls_schema = ResponseSchema(
        name="categories",
        description="List of categories with their urls",
    )

    output_parser = StructuredOutputParser.from_response_schemas([urls_schema])
    format_instructions = output_parser.get_format_instructions()

    messages = [
        (
            "system",
            f"""
            You are a helpful assistant that analyzes HTML content. I want you to analyze this HTML and return the list of the urls of the categories of the news articles available in the page. The categories are generally found in the navbar or the sidebar of the page.
            Please skip the {url} from the list of categories. If the category url is relative, join the base url to the category url. The base url is {url}.

            {format_instructions}
            """,
        ),
        ("human", html),
    ]

    ai_msg = llm.invoke(messages)
    parsed_output = output_parser.parse(ai_msg.content)

    return parsed_output


def save_categories_to_file(
    categories: dict, filename: str = "categories.json"
) -> None:
    """
    Save categories to a JSON file.

    Args:
        categories (dict): The categories dictionary to save
        filename (str): The name of the file to save to (default: "categories.json")
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)


# Example usage
if __name__ == "__main__":
    categories = get_categories_from_url()
    save_categories_to_file(categories)
