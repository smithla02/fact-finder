import json
import logging
import sqlite3
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from prompts import (
    create_fun_facts_prompt,
    create_related_topics_prompt,
    create_persona_prompt,
)
import random
from config import (
    LOG_LEVEL,
    DATABASE_NAME,
    OPENAI_API_KEY,
    TOPICS_FILE,
    FLASK_PORT,
    GPT_MODEL,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.debug("Logging is configured correctly.")

app = Flask(__name__)


def get_db_connection():
    """
    Establishes a connection to the SQLite database.

    Returns:
    - sqlite3.Connection: A connection object to the SQLite database.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table_if_not_exists(conn):
    """
    Establishes a connection to the SQLite database.

    Returns:
    - sqlite3.Connection: A connection object to the SQLite database.
    """
    conn.execute(
        """CREATE TABLE IF NOT EXISTS facts (topic TEXT PRIMARY KEY, facts TEXT, related_topics TEXT)"""
    )
    conn.commit()


def fetch_openai_data(topic, num_fun_facts, persona):
    """
    Fetch fun facts and related topics for a given topic from OpenAI.

    Parameters:
    - topic (str): The topic for which fun facts are to be fetched.
    - num_fun_facts (int): The number of fun facts to fetch.
    - persona (str): The persona to use for generating fun facts.

    Returns:
    - tuple: A tuple containing two lists, the first list contains fun facts, and the second list contains related topics.
    """
    try:
        client = OpenAI()
        OpenAI.api_key = OPENAI_API_KEY

        if not OpenAI.api_key:
            raise ValueError(
                "No OpenAI API key set. Please set the OPENAI_API_KEY environment variable."
            )

        persona_prompt = create_persona_prompt(persona)
        user_prompt = create_fun_facts_prompt(topic, num_fun_facts)

        logging.debug("--Sending request to OPENAI--")
        logging.debug(f"user_prompt = {user_prompt}")
        logging.debug(f"persona_prompt = {persona_prompt}")
        response = client.chat.completions.create(
            model=f"{GPT_MODEL}",
            messages=[
                {
                    "role": "system",
                    "content": persona_prompt,
                },
                {"role": "user", "content": user_prompt},
            ],
        )
        logging.debug("--Fun Facts Response--")
        logging.debug(f"{response}")

        # Directly access the response object
        if response.choices:
            facts_text = response.choices[0].message.content
            facts = facts_text.strip().split("\n")

            user_prompt = create_related_topics_prompt(topic)

            response = client.chat.completions.create(
                model=f"{GPT_MODEL}",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides related topics similar to a reference topic.",
                    },
                    {"role": "user", "content": f"{user_prompt}"},
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


@app.route("/get_facts", methods=["POST"])
def get_facts():
    """
    API endpoint to fetch fun facts and related topics for a given topic.

    Expects a JSON payload with keys "topic", "num_fun_facts", and "persona".

    Returns:
    - JSON: A JSON object containing the topic, a list of fun facts, and a list of related topics.
    """
    topic = request.json.get("topic")
    num_fun_facts = request.json.get("num_fun_facts")
    persona = request.json.get("persona")

    with get_db_connection() as conn:
        c = conn.cursor()
        facts, related_topics = fetch_openai_data(topic, num_fun_facts, persona)

        c.execute("SELECT * FROM facts WHERE topic = ?", (topic,))
        row = c.fetchone()
        if row:
            c.execute(
                "UPDATE facts SET facts=?, related_topics=? WHERE topic=?",
                (json.dumps(facts), json.dumps(related_topics), topic),
            )
        else:
            c.execute(
                "INSERT INTO facts (topic, facts, related_topics) VALUES (?, ?, ?)",
                (topic, json.dumps(facts), json.dumps(related_topics)),
            )
            conn.commit()

    return jsonify({"topic": topic, "facts": facts, "related_topics": related_topics})


@app.route("/get_random_topic", methods=["POST"])
def get_random_topic():
    """
    API endpoint to fetch a random topic from a predefined list.

    Returns:
    - JSON: A JSON object containing a randomly selected topic.
    """
    topics = []
    with open(TOPICS_FILE, "r") as f:
        topics = json.load(f)["topics"]
    random_topic = random.choice(topics)

    return jsonify({"random_topic": random_topic})


if __name__ == "__main__":
    with get_db_connection() as conn:
        create_table_if_not_exists(conn)
    app.run(port=FLASK_PORT, debug=True)
