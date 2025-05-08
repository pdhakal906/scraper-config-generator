import streamlit as st
import json
from modules.step_one import (
    get_categories_from_url,
    save_categories_to_file,
)

from modules.step_two import get_all_urls
from urllib.parse import urljoin

from modules.step_three import create_regular_expression

# Set page configuration
st.set_page_config(
    page_title="News Portal Config Generator", page_icon="📝", layout="centered"
)

final_config = []

# Add a title
st.title("News Portal Config Generator")

# Initialize session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "urls" not in st.session_state:
    st.session_state.urls = []
if "selected_urls" not in st.session_state:
    st.session_state.selected_urls = []

# Input field
user_input = st.text_input(
    "Enter the base url of the news portal:", value=st.session_state.user_input
)
BASE_URL = user_input

# Submit URL button
if st.button("Submit URL"):
    if user_input:
        st.session_state.user_input = user_input
        st.success(f"You entered: {user_input}")
        categories = get_categories_from_url(user_input)
        save_categories_to_file(categories, "data/categories.json")
        st.success("Categories are saved")
        st.info("Getting all urls from categories")
        urls = get_all_urls("data/categories.json")
        st.session_state.urls = urls
    else:
        st.warning("Please enter some text before submitting!")

# Display URLs with checkboxes
if st.session_state.urls:
    st.subheader("Select at least 5 Article URLs from EACH Category to Process")

    selected_urls = {}
    all_valid = True  # Will be used to ensure each category has at least 5 URLs

    for category, urls in st.session_state.urls.items():
        st.markdown(f"### {category}")
        selected_in_category = []

        for i, url in enumerate(urls):
            checkbox_key = f"{category}_url_{i}"
            if st.checkbox(f"{url}", key=checkbox_key):
                selected_in_category.append(url)

        selected_urls[category] = selected_in_category

        # Validation: Check if at least 5 URLs are selected in this category
        if len(selected_in_category) < 5:
            st.warning(f"Please select at least 5 URLs in {category}.")
            all_valid = False

    # Store all selected URLs in session
    st.session_state.selected_urls = selected_urls

    # Submit Button
    if st.button("Submit Selected URLs"):
        if not all_valid:
            st.warning("Make sure you have selected at least 5 URLs in each category.")
        else:
            st.success("URLs submitted successfully!")
            st.write("Submitted URLs by category:")
            st.json(st.session_state.selected_urls)

        # create a new variable from st.session_state.selected_urls
        with open("data/urls_to_process.json", "w") as f:
            json.dump({"urls": st.session_state.selected_urls}, f, indent=2)

        st.success("URLs are saved")

        st.info("Generating Regex. This may take a while...")

        with open("data/urls_to_process.json", "r") as f:
            urls = json.load(f)
            valid_urls_all_categories = urls["urls"]

        with open("data/categories.json", "r") as f:
            categories = json.load(f)
            categories = categories["categories"]

        for indv_category in categories:
            regex = create_regular_expression(
                indv_category, valid_urls_all_categories[indv_category]
            )
            st.write(regex)
            final_config.append(
                {
                    "url": indv_category,
                    "regex": regex.get("regular_expression"),
                }
            )


with open("config.json", "w") as f:
    json.dump(final_config, f, indent=2)

st.success("All regexes generated and saved to config.json")
