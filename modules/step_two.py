import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
from langchain_openai import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_all_urls(json_file_path):
    """
    Scrapes URLs from the categories defined in the specified JSON file

    Args:
        json_file_path (str): Path to the JSON file containing categories

    Returns:
        list: A list of all URLs found in the categories
    """
    with open(json_file_path, "r", encoding="utf-8") as f:
        categories = json.load(f)
        categories = categories["categories"]

    all_urls = {}

    for idx, indv_category in enumerate(categories, start=1):
        url = indv_category
        res = requests.get(url)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        a_tags = soup.find_all("a")
        urls = [a_tag.get("href") for a_tag in a_tags if a_tag.get("href")]

        all_urls[url] = urls

    return all_urls


if __name__ == "__main__":
    # This will only run if the script is executed directly
    get_all_urls()  # Uses default path
