"""
database.py: Contains functions for database operations such as creating tables and saving/fetching data.
"""

from sqlalchemy import text
import streamlit as st
import json
import logging
from typing import Tuple, Optional

# Database information, such as `url`, will be populated from `secrets.toml` file
conn = st.connection("facts_db", type="sql")


def create_facts_table() -> None:
    """
    Creates the 'facts' table in the database if it does not already exist.
    """
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


def standardize_primary_key(topic: str, persona: str) -> Tuple[str, str]:
    """
    Standardizes the primary key values for consistent database storage.
    """
    return str.lower(topic), str.lower(persona)


def save_facts_to_db(
    topic: str, persona: str, facts: list, related_topics: list
) -> None:
    """
    Saves or updates fun facts and related topics in the database.
    """
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


def get_facts_from_db(
    topic: str, persona: str
) -> Tuple[Optional[list], Optional[list]]:
    """
    Retrieves fun facts and related topics from the database.
    """
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
