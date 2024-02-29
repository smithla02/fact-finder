from sqlalchemy import text
import streamlit as st
import json
import logging

# Get the facts_db connection details from secrets if deployed on cloud
facts_db_connection = st.secrets.get("FACTS_DB_URL")

# Check if the connection details exist and get the URL if it does
db_url = facts_db_connection if facts_db_connection else "facts_db"

# Establish the connection
conn = st.connection(db_url, type="sql")


def create_facts_table():
    with conn.session as session:
        session.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS facts (
                topic TEXT,
                persona TEXT,
                facts TEXT,
                related_topics TEXT,
                PRIMARY KEY (topic, persona)
            );
        """
            )
        )
        session.commit()


# Ensure the table is created before any operations are performed
create_facts_table()


def standardize_primary_key(topic, persona):
    return str.lower(topic), str.lower(persona)


def save_facts_to_db(topic, persona, facts, related_topics):
    try:
        with conn.session as session:
            topic, persona = standardize_primary_key(topic, persona)
            # Check if the entry exists
            existing_entry = session.execute(
                text("SELECT * FROM facts WHERE topic = :topic AND persona = :persona"),
                {"topic": topic, "persona": persona},
            ).fetchone()

            if existing_entry:
                # Update existing entry
                session.execute(
                    text(
                        "UPDATE facts SET facts = :facts, related_topics = :related_topics WHERE topic = :topic AND persona = :persona"
                    ),
                    {
                        "topic": topic,
                        "persona": persona,
                        "facts": json.dumps(facts),
                        "related_topics": json.dumps(related_topics),
                    },
                )
            else:
                # Insert new entry
                session.execute(
                    text(
                        "INSERT INTO facts (topic, persona, facts, related_topics) VALUES (:topic, :persona, :facts, :related_topics)"
                    ),
                    {
                        "topic": topic,
                        "persona": persona,
                        "facts": json.dumps(facts),
                        "related_topics": json.dumps(related_topics),
                    },
                )
            session.commit()
    except Exception as e:
        logging.error(f"Error saving facts to database: {e}")


def get_facts_from_db(topic, persona):
    topic, persona = standardize_primary_key(topic, persona)
    with conn.session as session:
        result = session.execute(
            text("SELECT * FROM facts WHERE topic = :topic AND persona = :persona"),
            {"topic": topic, "persona": persona},
        ).fetchone()
        if result:
            return json.loads(result.facts), json.loads(result.related_topics)
        else:
            return None, None
