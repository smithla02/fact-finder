"""
streamlit_app.py: Main application file for the Streamlit app.
"""

import streamlit as st
import json
import logging
from config import (
    MINIMUM_FUN_FACTS,
    MAXIMUM_FUN_FACTS,
    DEFAULT_FUN_FACTS,
    RESPONSE_PERSONAS,
    TOPICS_FILE,
    LOG_LEVEL,
)
from database import save_facts_to_db, get_facts_from_db

from openai_retrieval import fetch_openai_data
import random
import re
from typing import Dict, Optional

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def update_current_topic() -> None:
    """
    Updates the current topic based on user interaction.
    """
    logger.debug(f"Update current topic, st.session_state: {st.session_state}")
    for related_topic, clicked in st.session_state.items():
        if related_topic not in ("search_topic", "current_topic") and clicked:
            # Use a regular expression to find the first occurrence of an alphabetical character and extract the substring from that point to the end
            match = re.search(r"[a-zA-Z].*", related_topic)
            if match:
                st.session_state["current_topic"] = match.group(0)


def fetch_facts(
    topic: str, selected_persona: str, num_facts: int
) -> Dict[str, Optional[list]]:
    """
    Fetches fun facts for a given topic and persona, either from cache or by querying OpenAI.
    """
    # Check if the facts are already in the database
    cached_facts, cached_related_topics = get_facts_from_db(
        topic, selected_persona, num_facts
    )
    if cached_facts and cached_related_topics:
        logger.debug(f"Retrieved cached facts for topic: {topic}")
        return {
            "topic": topic,
            "facts": cached_facts,
            "related_topics": cached_related_topics,
        }

    # If not in the database, fetch from OpenAI and save to the database
    facts, related_topics = fetch_openai_data(topic, selected_persona, num_facts)
    save_facts_to_db(topic, selected_persona, facts, related_topics, num_facts)
    return {"topic": topic, "facts": facts, "related_topics": related_topics}


def display_facts(data: Dict[str, list], topic: str) -> None:
    """
    Displays fun facts for a given topic.
    """
    st.subheader(f"{topic.title()}")
    for fact in data.get("facts", []):
        st.write(fact)


def fetch_random_topic() -> None:
    """
    Fetches a random topic from the topics file.
    """
    try:
        with open(TOPICS_FILE, "r") as f:
            topics = json.load(f)["topics"]
        random_topic = random.choice(topics)
        st.session_state["current_topic"] = random_topic
        return
    except Exception as e:
        logger.error(f"Error fetching random topic: {e}")
        st.error(
            "Failed to fetch a random topic. Please check your connection and try again."
        )


def display_related_topics(data: Dict[str, list]) -> None:
    """
    Displays buttons for related topics.
    """
    st.subheader("Explore fun facts on related topics:")
    cols = st.columns(len(data.get("related_topics", [])))
    for idx, related_topic in enumerate(data.get("related_topics", [])):
        with cols[idx]:
            if st.button(related_topic.title(), key=related_topic):
                st.rerun()


def save_search_topic(search_topic: str) -> None:
    """
    Saves the searched topic to session state.
    """
    st.session_state["current_topic"] = search_topic


def main() -> None:
    """
    Main function to run the Streamlit app.
    """
    update_current_topic()

    _, col2, _ = st.columns([1, 6, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center;'>Fun Fact Finder!</h1>",
            unsafe_allow_html=True,
        )

    st.markdown("### **Choose how many fun facts:**")
    num_facts = st.slider(
        "num_facts",
        MINIMUM_FUN_FACTS,
        MAXIMUM_FUN_FACTS,
        DEFAULT_FUN_FACTS,
        label_visibility="hidden",
    )

    st.markdown("### **Choose a persona:**")
    selected_persona = st.selectbox(
        "selected_persona", RESPONSE_PERSONAS, index=0, label_visibility="hidden"
    )

    st.markdown("### **Enter a topic:**")
    current_topic = st.session_state.get("current_topic", "").title()
    search_topic = st.text_input(
        "search_topic",
        key="search_topic",
        value=current_topic,
        label_visibility="hidden",
    )

    # Adjust the layout to separate the Search and Random Topic buttons
    st.button("Search", on_click=save_search_topic(search_topic))

    st.button(
        "**🎲 Can't Decide? Get a Random Topic!**",
        help="Click to get a random fun fact topic",
        on_click=fetch_random_topic,
    )

    if st.session_state.get("current_topic"):
        data = fetch_facts(st.session_state.current_topic, selected_persona, num_facts)
        if data:
            display_facts(data, st.session_state.current_topic)
            display_related_topics(data)


if __name__ == "__main__":
    main()
