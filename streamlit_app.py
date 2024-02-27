import streamlit as st
import requests
import logging
from app import FLASK_PORT

MINIMUM_FUN_FACTS = 1
MAXIMUM_FUN_FACTS = 10
DEFAULT_FUN_FACTS = 3


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.debug("Logging is configured correctly.")


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


@st.cache_data
def fetch_facts(topic, num_facts):
    """Fetch fun facts for a given topic."""
    try:
        request_json = {"topic": topic, "num_fun_facts": num_facts}
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


def display_related_topics(data):
    """Display buttons for related topics."""
    st.subheader("Explore related topics:")
    cols = st.columns(len(data.get("related_topics", [])))
    for idx, related_topic in enumerate(data.get("related_topics", [])):
        with cols[idx]:
            if st.button(related_topic.title(), key=related_topic):
                st.session_state.current_topic = related_topic.split(". ")[1].title()
                st.experimental_rerun()


def set_random_topic():
    random_topic = fetch_random_topic()
    if random_topic:
        st.session_state["search_topic"] = random_topic
        st.session_state["current_topic"] = random_topic


def main():
    setup_logging()

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
        "", MINIMUM_FUN_FACTS, MAXIMUM_FUN_FACTS, DEFAULT_FUN_FACTS
    )

    # Use markdown for text input label with custom font size and bold
    st.markdown("### **Enter a topic:**")
    search_topic = st.text_input("", key="search_topic")

    if st.button("Search"):
        st.session_state.current_topic = search_topic

    if st.button("Can't Decide? Get a Random Topic!", on_click=set_random_topic):
        pass

    # Fetch and display fun facts for the current topic
    if st.session_state.get("current_topic"):
        data = fetch_facts(st.session_state.current_topic, num_fun_facts)
        if data:
            display_facts(data, st.session_state.current_topic)
            display_related_topics(data)


if __name__ == "__main__":
    main()
