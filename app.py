import os
import json
import logging
import sqlite3
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from prompts import create_fun_facts_prompt, create_related_topics_prompt

# Load environment variables
load_dotenv()

LOG_LEVEL = logging.DEBUG
DATABASE_NAME = os.getenv("DATABASE_NAME", "facts.db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOPIC_ASSOCIATIONS_FILE = os.getenv(
    "TOPIC_ASSOCIATIONS_FILE", "topic_associations.json"
)
PORT = int(os.getenv("PORT", 8000))

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.debug("Logging is configured correctly.")

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_openai_data(topic):
    try:
        client = OpenAI()
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")

        if not OpenAI.api_key:
            raise ValueError(
                "No OpenAI API key set. Please set the OPENAI_API_KEY environment variable."
            )

        prompt = create_fun_facts_prompt(topic)

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


@app.route("/get_facts", methods=["POST"])
def get_facts():
    topic = request.json.get("topic")
    logger.debug(f"Received request for topic: {topic}")

    with get_db_connection() as conn:
        c = conn.cursor()
        facts, related_topics = fetch_openai_data(topic)

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


if __name__ == "__main__":
    with get_db_connection() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS facts (topic TEXT PRIMARY KEY, facts TEXT, related_topics TEXT)"""
        )
        conn.commit()
    app.run(port=PORT, debug=True)
