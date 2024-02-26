import streamlit as st
import requests
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.debug("Logging is configured correctly.")


def update_current_topic():
    for related_topic, clicked in st.session_state.items():
        if clicked is True:
            st.session_state["current_topic"] = related_topic.split(". ")[1]
            break


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


def display_facts(data, topic):
    st.subheader(f"{topic.title()}")
    for fact in data["facts"]:
        st.write(f"{fact}")


def display_related_topics(data):
    st.subheader("Find out more fun facts on related topics!")
    for idx, related_topic in enumerate(data["related_topics"]):
        related_topic = related_topic.title()
        if st.button(related_topic, key=related_topic):
            st.rerun()


def main():
    setup_logging()
    update_current_topic()

    if "current_topic" not in st.session_state:
        st.session_state["current_topic"] = ""

    st.title("Fun Fact Finder!")

    topic_input = st.text_input(
        "Enter a topic:", value=st.session_state.get("current_topic", "")
    )

    if st.button("Get Fun Facts!") or topic_input:
        if topic_input != st.session_state["current_topic"]:
            st.session_state["current_topic"] = topic_input

        data = fetch_facts(topic_input)
        if data:
            display_facts(data, topic_input)
            display_related_topics(data)


if __name__ == "__main__":
    main()
