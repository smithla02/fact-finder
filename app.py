import os
from flask import Flask, request, jsonify
import sqlite3
import json
import logging
from openai import OpenAI

LOG_LEVEL = logging.DEBUG
PORT = 8000

TOPIC_ASSOCIATIONS_FILE = "topic_associations.json"
DATABASE_NAME = "facts.db"

NUM_FUN_FACTS = 3
NUM_RELATED_TOPICS = 5

# Setup logging
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.debug("Logging is configured correctly.")

app = Flask(__name__)

# Setup database connection
conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
c = conn.cursor()

# Create table for caching fun facts and related topics
c.execute(
    """CREATE TABLE IF NOT EXISTS facts
             (topic TEXT PRIMARY KEY, facts TEXT, related_topics TEXT)"""
)
conn.commit()


@app.route("/get_facts", methods=["POST"])
def get_facts():
    data = request.json
    topic = data["topic"]
    logging.debug(f"Logging: Received request for topic: {topic}")

    # TODO: Add caching layer to retrieve topic from databse if it already exists

    # Fetch data from OpenAI if not cached
    facts, related_topics = fetch_openai_data(topic)

    # Check if the topic is in the database
    c.execute("SELECT * FROM facts WHERE topic=?", (topic,))
    row = c.fetchone()

    if row:
        # Update the existing record
        c.execute(
            "UPDATE facts SET facts=?, related_topics=? WHERE topic=?",
            (json.dumps(facts), json.dumps(related_topics), topic),
        )
    else:
        # Insert a new record
        c.execute(
            "INSERT INTO facts VALUES (?, ?, ?)",
            (topic, json.dumps(facts), json.dumps(related_topics)),
        )

    conn.commit()

    return jsonify({"topic": topic, "facts": facts, "related_topics": related_topics})


def get_topic_associations():
    with open("topic_associations.json", "r") as f:
        return json.load(f)


def create_related_topics_prompt(source_topic):
    output = "I will provide some examples of an original topic and related topics."
    for topic, related_topics in get_topic_associations().items():
        output += f"Original topic: {topic}, Related topics: {related_topics}"

    output += (
        f"Please note the structure of the original topic and related topics. "
        f"The length of each related topic is typically only 1-4 words long. "
        f"Now please give me {NUM_RELATED_TOPICS} interesting topics that are related "
        f"to the original topic of {source_topic}. Each related topic should only be 1-4 words long. "
        f"Do not give any introduction in your response, "
        f"please directly just give me the related topics in numbered format."
    )
    return output


def fetch_openai_data(topic):
    try:
        client = OpenAI()
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")

        if not OpenAI.api_key:
            raise ValueError(
                "No OpenAI API key set. Please set the OPENAI_API_KEY environment variable."
            )

        prompt = f"Give me {NUM_FUN_FACTS} fun fact(s) about {topic}."

        logging.debug("--Sending request to OPENAI--")
        logging.debug(f"prompt = {prompt}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides fun facts.",
                },
                {"role": "user", "content": f"{prompt}"},
            ],
        )
        logging.debug("--Fun Facts Response--")
        logging.debug(f"{response}")

        # Directly access the response object
        if response.choices:
            facts_text = response.choices[0].message.content
            facts = facts_text.strip().split("\n")

            prompt = create_related_topics_prompt(topic)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides related topics similar to a reference topic.",
                    },
                    {"role": "user", "content": f"{prompt}"},
                ],
            )
            logging.debug("--Related Topics Response--")
            logging.debug(f"{response}")
            related_topics_text = response.choices[0].message.content
            related_topics = related_topics_text.strip().split("\n")
        else:
            facts = ["No facts were retrieved."]
            related_topics = ["No related topics were retrieved."]

    except Exception as e:
        logging.error(f"Error fetching data from OpenAI: {e}")
        facts = ["An exception occurred while fetching fun facts."]
        related_topics = ["An exception occurred while fetching related topics."]

    return facts, related_topics


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
