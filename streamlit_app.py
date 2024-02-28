import streamlit as st
import requests
import logging
from config import (
    MINIMUM_FUN_FACTS,
    MAXIMUM_FUN_FACTS,
    DEFAULT_FUN_FACTS,
    RESPONSE_PERSONAS,
    FLASK_PORT,
)


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def update_current_topic():
    """Update current_topic by checking if related topic was clicked, which triggers app refresh"""
    for related_topic, clicked in st.session_state.items():
        if clicked is True:
            st.session_state["current_topic"] = related_topic.split(". ")[1]
            break


def fetch_random_topic():
    """Fetch a random topic from the server."""
    try:
        response = requests.post(f"http://localhost:{FLASK_PORT}/get_random_topic")
        response.raise_for_status()
        return response.json().get("random_topic", "")
    except requests.RequestException as e:
        logging.error(f"Error fetching random topic: {e}")
        st.error(
            "Failed to fetch a random topic. Please check your connection and try again."
        )
        return ""


def fetch_facts(topic, num_facts, selected_persona):
    """Fetch fun facts for a given topic."""
    try:
        request_json = {
            "topic": topic,
            "num_fun_facts": num_facts,
            "persona": selected_persona,
        }
        logging.debug(f"request_json = {request_json}")
        response = requests.post(
            f"http://localhost:{FLASK_PORT}/get_facts", json=request_json
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching facts for topic {topic}: {e}")
        st.error("Failed to fetch facts. Please check your connection and try again.")
        return None


def display_facts(data, topic):
    """Display fun facts about the given topic."""
    st.subheader(f"{topic.title()}")
    for fact in data.get("facts", []):
        st.write(fact)


def get_random_topic():
    random_topic = fetch_random_topic()
    if random_topic:
        st.session_state["current_topic"] = random_topic


def display_related_topics(data):
    """Display buttons for related topics."""
    st.subheader("Explore fun facts on related topics:")
    cols = st.columns(len(data.get("related_topics", [])))
    for idx, related_topic in enumerate(data.get("related_topics", [])):
        with cols[idx]:
            if st.button(related_topic.title(), key=related_topic):
                st.rerun()


def main():
    setup_logging()
    update_current_topic()

    # Centering the title using columns
    _, col2, _ = st.columns([1, 6, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center;'>Fun Fact Finder!</h1>",
            unsafe_allow_html=True,
        )

    # Use markdown for slider label with custom font size and bold
    st.markdown("### **Choose how many fun facts:**")
    num_fun_facts = st.slider(
        "num_fun_facts",
        MINIMUM_FUN_FACTS,
        MAXIMUM_FUN_FACTS,
        DEFAULT_FUN_FACTS,
        label_visibility="hidden",
    )

    # Select a persona
    st.markdown("### **Choose a persona:**")
    selected_persona = st.selectbox(
        "selected_persona", RESPONSE_PERSONAS, index=0, label_visibility="hidden"
    )

    # Use markdown for text input label with custom font size and bold
    st.markdown("### **Enter a topic:**")
    current_topic = st.session_state.get("current_topic", "").title()
    search_topic = st.text_input(
        "search_topic",
        key="search_topic",
        value=current_topic,
        label_visibility="hidden",
    )

    if st.button("Search"):
        st.session_state["current_topic"] = search_topic

    st.button("Can't Decide? Get a Random Topic!", on_click=get_random_topic)

    # Fetch and display fun facts for the current topic
    if st.session_state.get("current_topic"):
        data = fetch_facts(
            st.session_state.current_topic, num_fun_facts, selected_persona
        )
        if data:
            display_facts(data, st.session_state.current_topic)
            display_related_topics(data)


if __name__ == "__main__":
    main()
