import streamlit as st
import requests
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.debug("Logging is configured correctly.")

# Check if a "related topic" button has been clicked already
for related_topic, clicked in st.session_state.items():
    if clicked is True:
        # Remove numbering
        related_topic = related_topic.split(". ")[1]
        st.session_state["current_topic"] = related_topic
        break

# Initialize session state for storing the current topic if not already present
if "current_topic" not in st.session_state:
    st.session_state["current_topic"] = ""

st.title("Fun Fact Finder!")

# Pre-populate the search query with the current topic if it's already been set.
# If a user clicks "Get Fun Facts!" the typed entry will be used as the topic for the fun facts.
topic_input = st.text_input(
    "Enter a topic:", value=st.session_state.get("current_topic", "")
)


# Fetch facts for the current topic or the new input
def fetch_facts(topic):
    url = "http://localhost:8000/get_facts"
    response = requests.post(url, json={"topic": topic})
    if response.status_code == 200:
        return response.json()
    else:
        logging.debug(f"Topic = {topic}")
        logging.debug(f"url = {url}")
        logging.debug(f"response = {response}")
        st.error("Failed to fetch data. Please try again.")
        return None


# Display facts for the given topic
def display_facts(data, topic):
    st.subheader(f"{topic.title()}")
    for fact in data["facts"]:
        st.write(f"{fact}")


# Display related topics as buttons for further exploration
def display_related_topics(data):
    st.subheader("Find out more fun facts on related topics!")
    for idx, related_topic in enumerate(data["related_topics"]):
        # Use the related topic itself as a unique key for the button
        related_topic = related_topic.title()
        if st.button(related_topic, key=related_topic):
            st.rerun()


# When the 'Get Fun Facts!' button is clicked or a topic is already set, fetch and display facts
if st.button("Get Fun Facts!") or topic_input:
    # Update the current topic in session state in the scenario where a user searches a new topic
    if topic_input != st.session_state["current_topic"]:
        st.session_state["current_topic"] = topic_input

    data = fetch_facts(topic_input)
    if data:
        display_facts(data, topic_input)
        display_related_topics(data)
