import requests
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def create_regular_expression(url: str, valid_article_links: list) -> str:
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
        name="regular_expression",
        description="Python regular expression to extract valid article links from the html content",
    )

    output_parser = StructuredOutputParser.from_response_schemas([urls_schema])
    format_instructions = output_parser.get_format_instructions()

    messages = [
        (
            "system",
            f"""
            You are a helpful assistant that analyzes HTML content. I want you to analyze this HTML and return the regular expression to extract valid article links from the html content.
            here is a list of some valid article links:
            {valid_article_links}

            ONLY return a valid JSON object — do not use Python syntax like r"" for strings.
            All backslashes must be properly escaped according to JSON rules.

            {format_instructions}
            """,
        ),
        ("human", html),
    ]

    ai_msg = llm.invoke(messages)
    print("AI Message:")
    print(ai_msg.content)
    parsed_output = output_parser.parse(ai_msg.content)
    print("Parsed Output:")
    print(parsed_output)

    return parsed_output


# Example usage
if __name__ == "__main__":
    create_regular_expression()
